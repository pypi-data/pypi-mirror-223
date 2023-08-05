from swampObject import Chip,Transport
import json
import logging

import functools
import time
import util

def memoize(fn):
    """ Readable memoize decorator. """

    fn.cache = {}
    @functools.wraps(fn)
    def inner(inst, *key):
        if key not in fn.cache:
            fn.cache[key] = fn(inst, *key)
        return fn.cache[key]
    return inner

def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        print(f"Elapsed time: {elapsed_time:0.4f} seconds")
        return value
    return wrapper_timer

def register_from_param_values(
    param_dict, value_key="default_value", prev_param_value=0
):
    """
    Convert parameter values (from config dictionary) into register value.
    Here, all of the parameters share the same register's address.

    :param param_dict: Dictionary with parameter mask, shift and value
    :type param_dict: dict
    :param value_key: Key of param_dict that contains the parameter's value
    :type value_key: str
    :param prev_param_value: Previous value of register
    :type prev_param_value: int
    :return The register value composed of all parameters
    :rtype int
    """
    reg_value = prev_param_value
    for par, rdict in param_dict.items():
        param_val = int(rdict[value_key]) & int(rdict["param_mask"])
        param_val <<= int(rdict["param_shift"])
        reg_value |= param_val
    return reg_value


def register_from_new_value(
    cached_val,
    aligned_val,
    mask,
    shift,
):
    """
    Convert register's cached value into a new value, given a new aligned value.

    :param cached_val: Cache value of register
    :type cached_val: int
    :param aligned_val: New value that register would have if only a a given parameter had been modified. This value already aligns the new parameter value given its masks and shifts.
    :type aligned_val: int
    :param mask: Mask of modified parameter
    :type mask: int
    :param shift: Shift of modified parameter
    :type shift: int
    :return The new register value
    :rtype: int
    """
    return (cached_val & (~(mask << shift))) | aligned_val


class econ(Chip):
    @timer
    def __init__( self, name : str="", cfg : dict={} ):
        super().__init__(name,cfg)
        """
        :param base_address: Base address of the ECON to read and write to
        :type base_address: int
        :param name: Name of the ECON
        :type name: str
        :param reset_pin: i2c pin responsible for resetting the ECON
        :type reset_pin: object
        :param path_to_translatemap: Path to the json file containing a dictionary structure of
            all possible parameters (and the translation into register addresses/size)
        :type path_to_translatemap: str
        :param path_to_validatemap: Path to the json file containing a dictionary structure of
            validation parameters (register bounds and access)
        :type path_to_validatemap: str
        :param path_to_csvmap: Optional, path to the csv file containing the full map of registers
            (useful for translating back into a human readable format)
        :type path_to_csvmap: str
        :param path_to_defaultmap: Optional, path to the csv file containing the default values of all possible i2c addresses. If this is not None, the cache will use these values it to reset, instead of reading register addresses from hardware.
        :type path_to_defaultmap: str
        :param use_cache: Specifies whether to use cache
        :type use_cache: bool
        :param update_all_hits: Specifies whether a value will be written even if its value already matches the values read from hardware. To be used if use_cache==False.
        :type update_all_hits: bool
        """
        self.base_address=cfg['address']
        self.path_to_translatemap=cfg['path_to_translatemap']
        self.path_to_validatemap=cfg['path_to_validatemap']
        self.path_to_reg_definition = cfg['path_to_defaultmap']
        self.path_to_table = self.path_to_validatemap.replace("_validate.json", ".csv")

        self.use_cache = cfg['use_cache']
        self.update_all_hits = cfg['update_all_hits']

        # Set ECON to reset during init
        # self.reset_pin.write(0)

        # read in source of truth of the ECON configuration (with reference json files)
        self.translation_dict = {}
        self.validation_config = {}
        with open(self.path_to_translatemap, "r") as f:
            self.translation_dict = json.load(f)
        with open(self.path_to_validatemap, "r") as f:
            self.validation_config = json.load(f)

        self.cache = {}
        if self.use_cache:
            # construct a dictionary that allows us to read all readable parameters
            value_dict = {}
            config = self.translation_dict
            for block in config.keys():
                value_dict[block] = {}
                for key, kitem in config[block].items():
                    if "access" in kitem.keys():
                        if kitem["access"] != "wo":
                            value_dict[block][key] = None
                    else:
                        value_dict[block][key] = {}
                        for parameter, kitem in config[block][key].items():
                            if "access" in kitem.keys():
                                if kitem["access"] != "wo":
                                    value_dict[block][key][parameter] = None
                            else:
                                value_dict[block][key][parameter] = {}
                                for ikey, kitem in config[block][key][
                                    parameter
                                ].items():
                                    if "access" in kitem.keys():
                                        if kitem["access"] != "wo":
                                            value_dict[block][key][parameter][
                                                ikey
                                            ] = None
            self.value_dict = value_dict
            self.reset_cache(from_hardware=False)


        self.logger.debug("Initialization complete")

    def _validate(
        self,
        config: dict,
        reference: dict = None,
        read=False,
        log_message_written=False,
    ):
        """
        Expand configuration with lists into a full dictionary compatible with the reference.
        It converts all int keys into strings.

        Also, checks if the configuration given in config only contains
        valid keys and values within the specified range.

        :param config: The configuration that is to be expanded (in the case of
                       a recursive call, the relevant subsection is normally passed in)
        :type config: dict
        :param reference: The reference that the configuration is expected to match.
                          this is needed as the function is recursive and so needs
                          to pass the correct section of the total reference configuration
                          to the function call checking the sub-section, this parameter
                          defaults to the full reference so the user should not specify it
        :type config: dict
        :param read: Specifies if the configuration is for reading or writing
        :type read: bool, optional
        """
        if not log_message_written:
            self.logger.debug("Validating configuration dictionary")

        if reference is None:
            reference = self.validation_config

        expanded_config = config.copy()
        for key, val in config.items():
            strkey = str(key)
            if strkey in reference:
                if isinstance(val, dict) and isinstance(reference[strkey], dict):
                    expanded_config[key] = self._validate(
                        config[key],
                        reference[strkey],
                        log_message_written=True,
                        read=read,
                    )
                elif isinstance(val, list) and isinstance(reference[strkey], dict):
                    param_ids = []
                    for k in reference[strkey].keys():
                        try:
                            param_ids.append(int(k))
                        except:
                            pass
                    if len(val) == len(param_ids):
                        self.logger.debug(
                            "Expanding list in configuration dictionary"
                        )
                        expanded_config[key] = {i: v for i, v in enumerate(val)}
                    else:
                        raise KeyError(
                            f"invalid list length for {key}: {len(val)} instead of {len(param_ids)}"
                        )
                else:
                    if isinstance(reference[strkey], tuple) or isinstance(
                        reference[strkey], list
                    ):
                        if isinstance(val, int):
                            if read and reference[strkey][2] == "wo":
                                raise ValueError(
                                    f"{key} is {val} and block is Write Only "
                                )
                            elif (not read) and reference[strkey][2] == "ro":
                                raise ValueError(
                                    f"{key} is {val} and block is Read Only "
                                )
                            else:
                                if (
                                    val < reference[strkey][0]
                                    or val > reference[strkey][1]
                                ):
                                    raise ValueError(
                                        f"{key} is {val} and outside of bounds "
                                        f"[{reference[strkey][0]},"
                                        f"{reference[strkey][1]}]"
                                    )
                        elif val is None and read:
                            if reference[strkey][2] == "wo":
                                raise ValueError(
                                    f"{key} is {val} and block is Write Only "
                                )
                        else:
                            raise KeyError(
                                f"key in reference but dict is invalid for {key}"
                            )
                    else:
                        raise KeyError(
                            f"invalid validation dict {key} with reference value ",
                            reference[strkey],
                        )
            else:
                raise KeyError(f"invalid key {key}")

        return expanded_config

    def _translate(
        self, valid_config: dict, translation_dictionary=None, first_call=True
    ) -> list:
        """
        Translate valid config into list of output registers.

        :param valid_config: The valid configuration to be translated.
        :type valid_config: dict
        :param translation_dictionary: The dictionary to be used during translation.
        :type translation_dictionary: dict
        :param first_call: Boolean to print out debugging in the first call of function.
        :type first_call: bool, optional
        """
        # do this to avoid weird referencing and static variable behaviour
        output_regs = []
        if first_call:
            self.logger.debug("Translating configuration dictionary")

        if translation_dictionary is None:
            translation_dictionary = self.translation_dict
        for key, val in valid_config.items():
            strkey = str(key)
            if isinstance(val, dict):
                output_regs += self._translate(
                    val, translation_dictionary[strkey], first_call=False
                )
            else:
                param_registers = translation_dictionary[strkey]
                aligned_val = (val & param_registers["param_mask"]) << param_registers[
                    "param_shift"
                ]
                output_regs.append(
                    (
                        param_registers["address"],
                        aligned_val,
                        param_registers["param_mask"],
                        param_registers["param_shift"],
                        param_registers["size_byte"],
                    )
                )
        return output_regs

    def _translate_read(
        self,
        valid_config,
        translation_dictionary=None,
        curr_key=[],
        param_reg_pairs=[],
        written_log_message=False,
    ):
        """
        Translate a valid configuration dictionary into a list of parameter keys and properties of the form: [(key, (address,mask,shift,size)),...]

        :param valid_config: The valid configuration to be read.
        :type valid_config: dict
        :param translation_dictionary: The dictionary to be used during translation. If none, use the default.
        :type translation_dictionary: bool, optional
        :param curr_key: Level down keys to be used to append to the parameter key.
        :type curr_key: list, optional
        :param param_reg_pairs: Pairs of parameter key and properties to append.
        :type param_reg_pairs: list, optional
        :param written_log_message: Boolean to print out debugging in the first call of function.
        "type written_log_message: bool, optional
        """
        if not written_log_message:
            self.logger.debug("Translating Read Config")
        if translation_dictionary is None:
            translation_dictionary = self.translation_dict
        for key, val in valid_config.items():
            strkey = str(key)
            if isinstance(val, dict):
                level_down_key = curr_key.copy()
                level_down_key.append(key)
                self._translate_read(
                    val,
                    translation_dictionary[strkey],
                    curr_key=level_down_key,
                    param_reg_pairs=param_reg_pairs,
                    written_log_message=True,
                )
            else:
                new_key = curr_key.copy()
                new_key.append(key)
                param_registers = translation_dictionary[strkey]
                registers = (
                    param_registers["address"],
                    param_registers["param_mask"],
                    param_registers["param_shift"],
                    param_registers["size_byte"],
                )
                param_reg_pairs.append((new_key, registers))
        if not written_log_message:
            self.logger.debug("Parameters translated %s" % param_reg_pairs)
        return param_reg_pairs

    def _cache(self, changed_registers: list) -> list:
        """
        Update list of register values that need to change depending on register values on cache.

        :param changed_registers: List of parameters (reg address, value, mask, shift, size) to be updated.
        :type changed_registers: list
        :return: List of registers (address, value, size) to be written
        :rtype: list
        """
        dict_write_registers = {}
        write_registers = []
        for reg in changed_registers:
            reg_address, aligned_val, param_mask, param_shift, size_byte = reg
            self.logger.debug(f"Caching register {reg_address}")
            cached_val = self.cache[reg_address]
            new_val = register_from_new_value(
                cached_val, aligned_val, param_mask, param_shift
            )
            if new_val != cached_val:
                self.logger.debug("Cache miss")
                dict_write_registers[reg_address] = (new_val, size_byte)
                # update cache
                self.cache[reg_address] = new_val
            else:
                self.logger.debug("Cache hit")
        if dict_write_registers:
            write_registers = [
                (key, *value) for key, value in dict_write_registers.items()
            ]

        return write_registers

    def _nocache(self, changed_registers: list) -> list:
        """
        Update list of register values that need to change depending on list of register values read from hardware.

        :param changed_registers: List of registers (address, value, mask, shift, size) to be updated.
        :type changed_registers: list
        :return: List of registers (address, value, size) to be written
        :rytpe: list
        """
        read_values = {}
        for reg in changed_registers:
            reg_address, _, _, _, size_byte = reg
            if reg_address not in read_values:
                reg_address=(reg_address>>8)&0xFF | (reg_address&0xFF)<<8,
                read_content = self.transport.read_regs(
                        address=self.base_address,
                        reg_address_width=2,
                        reg_address=reg_address,
                        read_len=size_byte
                )
                read_content = int.from_bytes(read_content, "little")
                read_values[reg_address] = read_content

        dict_write_registers = {}
        write_registers = []
        for reg in changed_registers:
            reg_address, aligned_val, param_mask, param_shift, size_byte = reg
            read_val = read_values[reg_address]
            # check if register_address was requested to change by another parameter
            if reg_address in dict_write_registers:
                new_val = register_from_new_value(
                    dict_write_registers[reg_address][0],
                    aligned_val,
                    param_mask,
                    param_shift,
                )
            else:
                new_val = register_from_new_value(
                    read_val, aligned_val, param_mask, param_shift
                )

            if self.update_all_hits:
                self.logger.debug(
                    f"Writing register regardless of whether it is the same as the read value"
                )
                dict_write_registers[reg_address] = (new_val, size_byte)
            else:
                if new_val != read_val:
                    dict_write_registers[reg_address] = (new_val, size_byte)
                else:
                    self.logger.debug(
                        "New register value is same as read value"
                    )
        if dict_write_registers:
            write_registers = [
                (key, *value) for key, value in dict_write_registers.items()
            ]
        return write_registers

    def configure(self, cfg: dict, read_back: bool=False):
        """
        Writes to ECON registers

        :param cfg: Configuration containing values to write
        :type cfg: dict
        :param read_back: Specifies whether to check written registers
            against cache. Defaults to False
        :type read_back: bool, optional

        :return: The values of parameters read after read_back (if read_back=True, otherwise list is empty)
        :rtype: dict
        """
        self.logger.debug(f'configure with config = {cfg}')
        try:
            configuration = self._validate(cfg)
        except KeyError as err:
            raise KeyError(str(err.args[0]) + f" in ECON {self.name}")
        except ValueError as err:
            raise ValueError(str(err.args[0]) + f" in ECON {self.name}")

        register_updates = self._translate(configuration)

        if self.use_cache:
            # check which registers need to be updated and update cache
            register_writes = self._cache(register_updates)
        else:
            # check which registers need to be updated by reading directly from hardware
            register_writes = self._nocache(register_updates)

        self.logger.debug(
            "Updating configuration in " f"{len(register_writes)} registers"
        )

        for reg in register_writes:
            try:
                reg_address, new_val, size_byte = reg
                reg_address=(reg_address>>8)&0xFF | (reg_address&0xFF)<<8
                self.transport.write_regs(
                    address=self.base_address,
                    reg_address_width=2,
                    reg_address=reg_address,
                    reg_vals=list(new_val.to_bytes(size_byte, "little"))
                )

                if read_back:
                    rback_val = self.transport.read_regs(
                        address=self.base_address,
                        reg_address_width=2,
                        reg_address=reg_address,
                        read_len=size_byte
                    )
                    rback_val = int.from_bytes(rback_val, "little")
                    if rback_val != new_val:
                        raise IOError(
                            f"Read back {rback_val} from {reg_address} "
                            f"does not match written value {new_val}"
                        )
            except IOError as err:
                raise IOError(
                    str(err.args[0]) + f" during write operation to {self.name}"
                )
        self.logger.debug(
            "Configuration written to " f"{len(register_writes)} registers"
        )

        param_readbacks = []
        if read_back:
            param_readbacks = self.read(
                configuration, from_hardware=True, as_parameters=False
            )

        return param_readbacks

    def read(self, cfg: dict={}, from_cache: bool=False):
        """
        Reads register values from cache

        :param cfg: Configuration containing parameters to read
        :type cfg: dict
        :param from_cache: Set to false to skip the hardware read and read directly from cache
        :type from_cache: bool
        :return: The values of parameters read from cache
        :rtype: dict
        """
        self.logger.info(f'read with config = {cfg}')
        try:
            cfg = self._validate(cfg, read=True)
        except KeyError as err:
            raise KeyError(str(err.args[0]) + f" in ECON {self.name}")
        except ValueError as err:
            raise ValueError(str(err.args[0]) + f" in ECON {self.name}")
        self.logger.debug("Configuration to translate %s" % cfg)
        parameters_to_be_read = self._translate_read(cfg, param_reg_pairs=[])

        read_string = f"Reading {len(parameters_to_be_read)} parameters"
        if from_cache==True and self.use_cache==True:
            read_string += " from cache"
        else:
            read_string += " from registers"
        self.logger.debug(read_string)

        parameters = []
        # read the values from the registers
        for param, reg in parameters_to_be_read:
            reg_address, param_mask, param_shift, size_byte = reg
            if from_cache==False:
                read_content = self.transport.read_regs(
                    address=self.base_address,
                    reg_address_width=2,
                    reg_address=(reg_address>>8)&0xFF | (reg_address&0xFF)<<8,
                    read_len=size_byte
                )
                read_content = int.from_bytes(read_content, "little")
            else:
                read_content = self.cache[reg_address]
            if self.use_cache:
                self.cache[reg_address] = read_content
                self.logger.debug("Cache was updated with values read")
            parameter_value = (read_content >> param_shift) & param_mask
            parameters.append((param, parameter_value))

        read_string = f"{len(parameters_to_be_read)} " "parameters read"
        if from_cache==False:
            read_string += " from registers"
        else:
            read_string += " from cache"
        self.logger.debug(read_string)

        # build the dict
        result = {}
        for keylist, value in parameters:
            subdict = util.nested_dict_from_keylist(keylist, value)
            util.update_dict(result, subdict, in_place=True)

        self.logger.info(result)
        return result

    def reset_cache(self, from_hardware=False):
        if from_hardware:
            #self.read(self.value_dict, from_cache=False)
            self.logger.critical('ECON reset_cache from hardware not implemented yet')
            exit(1)
        else:
            # read in source of truth of the ECON configuration
            with open(self.path_to_reg_definition, "r") as f:
                config = {int(k): int(v) for k, v in json.load(f).items()}
                self.cache.update(config)

    def reset(self):
        # self.reset_pin.write(0)
        self.reset_cache()
        # self.reset_pin.write(1)

class dummyTransport(Transport):
    def __init__(self, name : str="", cfg : dict={} ):
        super().__init__(name,cfg)
        self.nwrite=0
        self.nread=0
        self.fout = open('output.txt','w')
        pass
    
    def write_regs(self, address, reg_address_width, reg_address, reg_vals):
        self.nwrite+=1
        self.fout.write(f'writing addr,val : {reg_address},{reg_vals}\n') 

    def read_regs(self, address, reg_address_width, reg_address, read_len):
        self.nread+=1

    def read(self,address):
        self.nread+=1
        self.fout.write(f'reading addr : {address}\n') 
        return 0xca
import yaml
import copy

def main():
    tr  = dummyTransport(name='i2c_w0',cfg={})
    cfg = {
        'address':0x60,
        'path_to_translatemap':'./regmaps/ECONT_I2C_params_regmap_translate.json',
        'path_to_validatemap':'./regmaps/ECONT_I2C_params_regmap_validate.json',
        'path_to_defaultmap':'./regmaps/ECONT_I2C_default_regmap.json',
        'use_cache':True,
        'update_all_hits':False
    }
    myecon_t = econ(name = 'econt', cfg=cfg)
    myecon_t.setLoggingLevel('INFO')
    with open('./configs/econt_test_config.yaml') as fin:
        cfg=yaml.safe_load(fin)
    
    
    myecon_t.set_transport(tr)
    # aroc.read(roc_config)

    myecon_t.configure(cfg)
    myecon_t.read(cfg,True)
    print(tr.nread,tr.nwrite)

    cfg = {
        'address':0x60,
        'path_to_translatemap':'./regmaps/ECOND_1.8.0_I2C_params_regmap_translate.json',
        'path_to_validatemap':'./regmaps/ECOND_1.8.0_I2C_params_regmap_validate.json',
        'path_to_defaultmap':'./regmaps/ECOND_1.8.0_I2C_default_regmap.json',
        'use_cache':True,
        'update_all_hits':False
    }
    myecon_d = econ(name = 'econd', cfg=cfg)
    with open('./configs/econd_test_config.yaml') as fin:
        cfg=yaml.safe_load(fin)
    
    
    myecon_d.set_transport(tr)
    # # aroc.read(roc_config)
    # # print(tr.nread,tr.nwrite)

    myecon_d.configure(cfg)
    # myecon_d.read(cfg,True)

    print( myecon_d.read(cfg=cfg,from_cache=True) )
    
    myecon_d.reset()
    
    #myecon.configure(cfg=cfg,read_back=False)
    # print(yaml.dump(aroc.read(from_cache=True)))

    # print(aroc.read_reg(46,11))

    # print(yaml.dump(aroc.read()))


if __name__ == '__main__':
    main()
        
