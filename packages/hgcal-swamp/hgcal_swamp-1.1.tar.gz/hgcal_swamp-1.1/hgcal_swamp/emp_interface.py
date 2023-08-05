import uhal
import emp

class emp_interface:
    def __init__(self,
                 connectionFile : str = "file:///home/cmx/rshukla/test_stand/connections.xml",
                 deviceName : str = "x0",
                 emp_channel : int = 13,
                 timeout : int = 10000 ):
        self.connections = connectionFile
        self.device = deviceName
        uhal.setLogLevelTo( uhal.LogLevel.ERROR )
        self.hw = uhal.ConnectionManager(self.connections).getDevice(self.device)
        self.empController = emp.Controller(self.hw)
        self.empController.hw().setTimeoutPeriod(timeout)
        self.empController.getDatapath().selectRegion(emp_channel//4)
        self.empController.getDatapath().selectLink(emp_channel)

    
    def set_EC(self):
        # enable EC mux
        self.hw.getNode("datapath.region.fe_mgt.data_framer.ctrl.ec_ic").write(1)
        self.hw.dispatch()
    
    def set_IC(self):
        # disable EC mux
        self.hw.getNode("datapath.region.fe_mgt.data_framer.ctrl.ec_ic").write(0)
        self.hw.dispatch()
    

    def write_IC(self, reg, val, lpgbt_addr=0x70):
        self.empController.getSCC().reset()
        if not (type(val) == list):
          val = [val]
        #print(f"INFO: writeIC :  reg_add = 0x{reg:04x}, val0 = 0x{val[0]:04x}, val_len = {len(val)}, lpgbt_addr = 0x{lpgbt_addr:02x}  ")		
        self.empController.getSCCIC().icWriteBlock(reg, val, lpgbt_addr)


    def read_IC(self, reg, nread=1, lpgbt_addr=0x70):
        #print(f'reg = {hex(reg)}, nread = {nread}')
        self.empController.getSCC().reset()
        words = []
        if nread == 1:
          lReply = self.empController.getSCCIC().icRead(reg, lpgbt_addr)
        else:
            lReply = []
            ## not pretty but we have seen issues when trying to read more registers in 1 icReadBlock call (limit was found for 24 consecutive registers)
            maxNbrRegPerRead=16
            number_of_IC_read = int( (nread-1)/maxNbrRegPerRead )+1
            #print(number_of_IC_read)
            for iread in range(number_of_IC_read):
                reg_addr = reg + iread * maxNbrRegPerRead
                read_len = maxNbrRegPerRead if iread+1<number_of_IC_read else nread%maxNbrRegPerRead if nread%maxNbrRegPerRead>0 else maxNbrRegPerRead
                lReply.extend( self.empController.getSCCIC().icReadBlock(reg_addr, read_len, lpgbt_addr) )        
            #lReply = self.empController.getSCCIC().icReadBlock(reg, nread, lpgbt_addr)
        
        

        if type(lReply) != list:
          lReply = [lReply]

        for word in lReply:
          words.append(word & 0xFF)
          #print(f" DEBUG: readIC : add_base= 0x{reg:02x} lReply = 0x{word:08x}")
        
        return words 
