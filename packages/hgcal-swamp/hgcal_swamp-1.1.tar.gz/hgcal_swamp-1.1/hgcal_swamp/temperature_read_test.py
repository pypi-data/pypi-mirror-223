import sc_lpgbt
import vtrx
import lpgbt_io
import pt1000
import yaml
import sc_transactor_interface
from time import sleep


def setup_core(lpgbt, id):
    if id == 'A':
        with open("./configs/setup_daq_lpgbt.yaml") as fin:
            lpgbt_config = yaml.safe_load(fin)['daq_lpgbt']
    elif id == 'B':
        with open("./configs/setup_trg_lpgbt_B.yaml") as fin:
            lpgbt_config = yaml.safe_load(fin)['trg_lpgbt']
    elif id == 'C':
        with open("./configs/setup_trg_lpgbt_C.yaml") as fin:
            lpgbt_config = yaml.safe_load(fin)['trg_lpgbt']
    if id == 'B' or id == 'C':
        lpgbt.write_reg(0x13c, 0x0)
        lpgbt.write_reg(0x13c, 0x7)
        lpgbt.write_reg(0x13c, 0x0)
    lpgbt.configure(lpgbt_config)
    print(yaml.dump(lpgbt.read(lpgbt_config)))


def setup_clocks(lpgbt):
    with open("./configs/setup_clocks_lpgbt.yaml") as fin:
        lpgbt_config = yaml.safe_load(fin)['daq_lpgbt']
        lpgbt.configure(lpgbt_config)
        print(yaml.dump(lpgbt.read(lpgbt_config)))


def setup_inputs(lpgbt, id):
    if id == 'A':
        with open("./configs/setup_inputs_daq_lpgbt.yaml") as fin:
            lpgbt_config = yaml.safe_load(fin)['daq_lpgbt']
    elif id == 'B':
        with open("./configs/setup_inputs_trg_lpgbt_B.yaml") as fin:
            lpgbt_config = yaml.safe_load(fin)['trg_lpgbt']
    elif id == 'C':
        with open("./configs/setup_inputs_trg_lpgbt_C.yaml") as fin:
            lpgbt_config = yaml.safe_load(fin)['trg_lpgbt']
    lpgbt.configure(lpgbt_config)
    lpgbt.read(lpgbt_config)


def setup_outputs(lpgbt):
    with open("./configs/setup_outputs.yaml") as fin:
        lpgbt_config = yaml.safe_load(fin)['daq_lpgbt']
        lpgbt.configure(lpgbt_config)
        lpgbt.read(lpgbt_config)


def main():
    transactor_interface = sc_transactor_interface.sc_transactor_interface()

    transport_cfg = {
        'name': 'lpgbt_ic',
        'id': 0,
        'configuration': {'broadcast_address': 1}
    }
    transport_ic = lpgbt_io.lpgbt_ic(transport_cfg, transactor_interface)
    transport_ic.setLoggingLevel('INFO')

    daq_lpgbt = sc_lpgbt.sc_lpgbt(0x70, transport_ic)
    daq_lpgbt.setLoggingLevel('INFO')

    setup_core(daq_lpgbt, 'A')
    setup_clocks(daq_lpgbt)
    # all gpio set as input except TRG lpgbt B and C resets
    daq_gpio_pins = [0 if i < 14 else 1 for i in range(16)]
    daq_lpgbt.init_gpio(daq_gpio_pins)

    transport_cfg = {
        "name": "lpgbt_daq_i2c",
        "id": 0,
        "configuration": {
            "bus": 1,
            "lpgbt": daq_lpgbt,
            "master_config": {'clk_freq': 2,  # { 0: 100 kHz, 1: 200 kHz, 2: 400 kHz, 3: 1 MHz }
                              'scl_drive': False,
                              'scl_pullup': False,
                              'scl_drive_strength': 0,
                              'sda_pullup': False,
                              'sda_drive_strength': 0
                              }
        }
    }
    transport_i2c_daq_lpgbt = lpgbt_io.lpgbt_i2c(transport_cfg)
    transport_i2c_daq_lpgbt.setLoggingLevel('INFO')
    a_vtrx = vtrx.vtrx(0x50, transport_i2c_daq_lpgbt)
    a_vtrx.setLoggingLevel('DEBUG')
    vtrx_config = {0x00: 0x07}
    a_vtrx.configure(vtrx_config)
    a_vtrx.read(vtrx_config)

    transport_cfg = {
        'name': 'lpgbt_ec',
        'id': 0,
        'configuration': {'broadcast_address': 2}
    }
    transport_ec = lpgbt_io.lpgbt_ec(transport_cfg, transactor_interface)
    transport_ec.setLoggingLevel('INFO')

    # west LPGBT
    reset_pin_B = daq_lpgbt.get_gpio_pin(14)
    trg_lpgbt_B = sc_lpgbt.sc_lpgbt(0x71, transport_ec, reset_pin_B)
    trg_lpgbt_B.setLoggingLevel('INFO')

    reset_pin_C = daq_lpgbt.get_gpio_pin(15)
    trg_lpgbt_C = sc_lpgbt.sc_lpgbt(0x72, transport_ec, reset_pin_C)
    trg_lpgbt_C.setLoggingLevel('INFO')

    reset_pin_B.up()
    reset_pin_C.up()
    # trg_lpgbt_B.reset()
    # trg_lpgbt_C.reset()
    # trg_lpgbt_B.dump('/tmp/power_on_default_TRG_B_lpgbt.json')
    # trg_lpgbt_C.dump('/tmp/power_on_default_TRG_C_lpgbt.json')

    setup_core(trg_lpgbt_B, 'B')
    setup_core(trg_lpgbt_C, 'C')
    trg_gpio_pins = [1 for i in range(16)]  # all gpio set as output
    trg_lpgbt_B.init_gpio(trg_gpio_pins)
    trg_lpgbt_C.init_gpio(trg_gpio_pins)

    setup_inputs(daq_lpgbt, 'A')
    setup_inputs(trg_lpgbt_B, 'B')
    setup_inputs(trg_lpgbt_C, 'C')

    setup_outputs(daq_lpgbt)

    cfg = {'POWERUP2': 6}
    daq_lpgbt.configure(cfg)
    trg_lpgbt_B.configure(cfg)
    trg_lpgbt_C.configure(cfg)

    daq_adc_channels_cfg = {'VTRx+': {'channel_p': daq_lpgbt.lpgbt.AdcInputSelect.EXT7},
                            'internal_temperature': {'channel_p': daq_lpgbt.lpgbt.AdcInputSelect.TEMP},
                            'WRTD': {'channel_p': daq_lpgbt.lpgbt.AdcInputSelect.EXT0},
                            'ERTD': {'channel_p': daq_lpgbt.lpgbt.AdcInputSelect.EXT3}}

    daq_lpgbt.init_adc_channels(daq_adc_channels_cfg)
    a_vtrx.setup_temperature_read(daq_lpgbt.get_adc_channel('VTRx+'))

    pt1000_west = pt1000.pt1000(daq_lpgbt.get_adc_channel('WRTD'))
    pt1000_east = pt1000.pt1000(daq_lpgbt.get_adc_channel('ERTD'))
    
    trg_adc_channels_cfg = {'internal_temperature': {'channel_p': trg_lpgbt_B.lpgbt.AdcInputSelect.TEMP}}
    trg_lpgbt_B.init_adc_channels(trg_adc_channels_cfg)
    trg_lpgbt_C.init_adc_channels(trg_adc_channels_cfg)


    while (1):
        print("Temperature reading (VTRx+, DAQ-lpGBT, W-lpGBT, E-lpGBT, RTDW, RTDE) = ({}°C, {}°C, {}°C, {}°C, {}°C, {}°C)".format(a_vtrx.read_temperature(),
              daq_lpgbt.read_temperature(), trg_lpgbt_B.read_temperature(), trg_lpgbt_C.read_temperature(), pt1000_west.read_temperature(), pt1000_east.read_temperature()))
        sleep(1)


if __name__ == "__main__":
    main()
