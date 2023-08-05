import logging
import argparse
import sc_lpgbt, roc
import lpgbt_ic, lpgbt_i2c
import util
import yaml
import sc_transactor_interface

def testROC():
    cfg = { 'broadcast_address' : 2 }
    transport_ec = lpgbt_ic.lpgbt_ec(name='ec',cfg=cfg)
    transport_ec.setLoggingLevel('INFO')
    
    # east LPGBT
    cfg = { 'address' : 0x72 }
    trg_lpgbt_C = sc_lpgbt.sc_lpgbt(name='E_lpgbt',cfg=cfg)
    trg_lpgbt_C.setLoggingLevel('INFO')
    trg_lpgbt_C.set_transport(transport_ec)
    trg_gpio_pins = [ 1 for i in range(16) ] #all gpio set as output
    trg_lpgbt_C.init_gpio(trg_gpio_pins)

    cfg = { 'bus' : 0 }
    transport_i2c_e_lpgbt = lpgbt_i2c.lpgbt_i2c(name='e_lpgbt.i2c.m0',cfg=cfg)
    transport_i2c_e_lpgbt.setLoggingLevel('INFO')
    transport_i2c_e_lpgbt.set_carrier(trg_lpgbt_C)
    master_cfg =  { 'clk_freq'           : 3, # { 0: 100 kHz, 1: 200 kHz, 2: 400 kHz, 3: 1 MHz }
                    'scl_drive'          : False,
                    'scl_pullup'         : False,
                    'scl_drive_strength' : 0,
                    'sda_pullup'         : False,
                    'sda_drive_strength' : 0
    }
    transport_i2c_e_lpgbt.configure(cfg=master_cfg)
    
    pwr_enable     = trg_lpgbt_C.get_gpio_pin(0)
    hard_reset_pin = trg_lpgbt_C.get_gpio_pin(3)
    soft_reset_pin = trg_lpgbt_C.get_gpio_pin(6)
    
    from time import sleep
    pwr_enable.up()
    #sleep(2)   
    #pwr_enable.up()
    #sleep(2)   
    soft_reset_pin.up()
    hard_reset_pin.down()
    sleep(2)   
    hard_reset_pin.up()
    
    aroc = roc.roc(name = 'roc_s0', cfg={'address':0x18})
    aroc.reset_done = True
    aroc.set_transport(transport_i2c_e_lpgbt)
    aroc.setLoggingLevel('DEBUG')

    with open('configs/V3LDHexaboard-poweron-default.yaml') as fin:
        cfg = yaml.safe_load(fin)
        cfg = cfg['roc_s0']
    powerOnDefault = aroc.read(cfg)
    with open("./power-on-default.yaml",'w') as fout:
        yaml.dump(powerOnDefault,fout)
    
    with open('configs/init_roc.yaml') as fin:
        cfg = yaml.safe_load(fin)
    aroc.configure(cfg,read_back=False)

    afterInit = aroc.read()

    with open("./after-init.yaml",'w') as fout:
        yaml.dump(afterInit,fout)
    # print(yaml.dump(aroc.read(from_cache=True)))
    # print(aroc.read_reg(196,10))
    # print(yaml.dump(aroc.read()))

if __name__ == '__main__':
    testROC()
