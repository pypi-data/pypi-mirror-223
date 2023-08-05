import util
from swampObject import Transport
from math import ceil
from emp_interface import emp_interface



class lpgbt_ic_emp(Transport):
    def __init__(self, name : str="", cfg : dict={} ):
        super().__init__(name=name, cfg=cfg)
        connectionFile = self.cfg['connectionFile'] if 'connectionFile' in cfg  else "file:///home/cmx/rshukla/test_stand/connections.xml"
        deviceName = self.cfg['deviceName'] if 'deviceName' in cfg else 'x0'
        emp_channel = self.cfg['emp_channel'] if 'emp_channel' in cfg else 13
        timeout = self.cfg['timeout'] if 'timeout' in cfg else 10000
        self.transactor = emp_interface(connectionFile=connectionFile,
                                                  deviceName=deviceName,
                                                  emp_channel=emp_channel,
                                                  timeout=timeout)
        self.transactor.set_IC()
                
    def setLoggingLevel(self,level):
        super().setLoggingLevel(level)

    def write_regs(self, chip_address:int, reg_address_width:int, reg_addr:int, reg_vals:list, protocol="IC"):
        if protocol== "IC":
          self.transactor.set_IC()
        else:
          self.transactor.set_EC()

        ## reg_address_width is not used as the transactor reserves 16 bits for the reg_address
        ## we need to keep it to use same interface as lpgbt_i2c.write_regs function (which might be used to configure lpgbts)
        self.logger.debug("in lpgbt_ic_emp.write_regs")
        n_regs = len(reg_vals)

        # split registers in transactions
        n_transactions = ceil(n_regs/16) # up to 16 registers per transaction
        
        for i in range(n_transactions):
          status = self.transactor.write_IC(reg_addr + i*16, reg_vals[i*16 : (i+1)*16], chip_address)  
        self.logger.debug("lpgbt_ic_emp.write_regs done")
        
    def read_regs(self, chip_address:int, reg_address_width:int, reg_addr:int, read_len:int, protocol="IC"):
        if protocol== "IC":
          self.transactor.set_IC()
        else:
          self.transactor.set_EC()
        ## reg_address_width is not used as the transactor reserves 16 bits for the reg_address
        ## we need to keep it to use same interface as lpgbt_i2c.read_regs function (which might me used to read from lpgbts)
        self.logger.debug("in lpgbt_ic.read_regs")

        # split registers in transactions
        n_transactions = ceil(read_len/16) # up to 16 registers per transaction
        response = []
        for i in range(n_transactions):
          res_temp = []
          if i != n_transactions -1:
            res_temp = self.transactor.read_IC(reg_addr + (i*16), 16, chip_address)
            self.logger.debug(f'n_transaction = {i}, response = {res_temp}')
          else:
            res_temp = self.transactor.read_IC(reg_addr + (i*16), (read_len % 16), chip_address)
            self.logger.debug(f'n_transaction = {i}, response = {res_temp}')
          response.extend(res_temp)
        
        self.logger.debug("lpgbt_ic.read_regs done")
        return response

class lpgbt_ec_emp(lpgbt_ic_emp):        
    def write_regs(self, chip_address:int, reg_address_width:int, reg_addr:int, reg_vals:list):
        self.logger.debug("in lpgbt_ec.write_regs")
        #self.transactor.set_EC()
        super().write_regs(chip_address, reg_address_width, reg_addr, reg_vals, "EC")
        self.logger.debug("lpgbt_ec.write_regs done")
        #default to IC
        #self.transactor.set_IC()
        
    def read_regs(self, chip_address:int, reg_address_width:int, reg_addr:int, read_len:int):
        self.logger.debug("in lpgbt_ec.read_regs")
        #self.transactor.set_EC()
        resp = super().read_regs(chip_address, reg_address_width, reg_addr, read_len, "EC")
        self.logger.debug("lpgbt_ec.read_regs done")
        #default to IC
        #self.transactor.set_IC()
        return resp
