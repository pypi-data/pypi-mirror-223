import logging
import argparse
import sc_lpgbt, vtrx, roc
import lpgbt_ic, lpgbt_i2c
import util
import yaml
from time import sleep

def setup_core(lpgbt,id):
    if id=='A':
        with open("./configs/setup_daq_lpgbt.yaml") as fin:
            lpgbt_config = yaml.safe_load(fin)['daq_lpgbt']
    elif id=='B':
        with open("./configs/setup_trg_lpgbt_B.yaml") as fin:
            lpgbt_config = yaml.safe_load(fin)['trg_lpgbt']
    elif id=='C':
        with open("./configs/setup_trg_lpgbt_C.yaml") as fin:
            lpgbt_config = yaml.safe_load(fin)['trg_lpgbt']
    if id=='B' or id=='C':
        lpgbt.write_reg(0x13c, 0x0)
        lpgbt.write_reg(0x13c, 0x7)
        lpgbt.write_reg(0x13c, 0x0)
    lpgbt.configure(lpgbt_config)
    print( yaml.dump(lpgbt.read(lpgbt_config)) )

def setup_clocks(lpgbt):
    with open("./configs/setup_clocks_lpgbt.yaml") as fin:
        lpgbt_config = yaml.safe_load(fin)['daq_lpgbt']
        lpgbt.configure(lpgbt_config)
        print(yaml.dump(lpgbt.read(lpgbt_config)))
        
def setup_inputs(lpgbt,id):
    if id=='A':
        with open("./configs/setup_inputs_daq_lpgbt.yaml") as fin:
            lpgbt_config = yaml.safe_load(fin)['daq_lpgbt']
    elif id=='B':
        with open("./configs/setup_inputs_trg_lpgbt_B.yaml") as fin:
            lpgbt_config = yaml.safe_load(fin)['trg_lpgbt']
    elif id=='C':
        with open("./configs/setup_inputs_trg_lpgbt_C.yaml") as fin:
            lpgbt_config = yaml.safe_load(fin)['trg_lpgbt']
    lpgbt.configure(lpgbt_config)
    lpgbt.read(lpgbt_config)

def setup_outputs(lpgbt):
    with open("./configs/setup_outputs.yaml") as fin:
        lpgbt_config = yaml.safe_load(fin)['daq_lpgbt']
        lpgbt.configure(lpgbt_config)
        lpgbt.read(lpgbt_config)


def app():
    cfg = { 'broadcast_address' : 1 }
    transport_ic = lpgbt_ic.lpgbt_ic(name='ic',cfg=cfg)
    transport_ic.setLoggingLevel('INFO')

    cfg = { 'address' : 0x70 }
    daq_lpgbt = sc_lpgbt.sc_lpgbt(name='daq_lpgbt',cfg=cfg)
    daq_lpgbt.setLoggingLevel('INFO')
    daq_lpgbt.set_transport(transport_ic)

    transport_cfg = {
        "name" : "lpgbt_daq_i2c",
        "id"  : 0,
        "configuration" : {
            "bus" : 1,
            "lpgbt" : daq_lpgbt,
        }
    }
    cfg = { 'bus' : 1 }
    transport_i2c_daq_lpgbt = lpgbt_i2c.lpgbt_i2c(name='daq_lpgbt.i2c.m1',cfg=cfg)
    transport_i2c_daq_lpgbt.setLoggingLevel('INFO')
    transport_i2c_daq_lpgbt.set_carrier(daq_lpgbt)
    master_cfg =  { 'clk_freq'           : 1, # { 0: 100 kHz, 1: 200 kHz, 2: 400 kHz, 3: 1 MHz }
                    'scl_drive'          : False,
                    'scl_pullup'         : False,
                    'scl_drive_strength' : 0,
                    'sda_pullup'         : False,
                    'sda_drive_strength' : 0
    }
    
    a_vtrx = vtrx.vtrx(name='vtrx',cfg={'address':0x50})
    a_vtrx.setLoggingLevel('DEBUG')
    a_vtrx.set_transport(transport_i2c_daq_lpgbt)

    cfg = { 'broadcast_address' : 2 }
    transport_ec = lpgbt_ic.lpgbt_ec(name='ec',cfg=cfg)
    transport_ec.setLoggingLevel('INFO')

    # west LPGBT
    cfg = { 'address' : 0x71 }
    trg_lpgbt_B = sc_lpgbt.sc_lpgbt(name='W_lpgbt',cfg=cfg)
    trg_lpgbt_B.setLoggingLevel('INFO')
    trg_lpgbt_B.set_transport(transport_ec)
    # east LPGBT
    cfg = { 'address' : 0x72 }
    trg_lpgbt_C = sc_lpgbt.sc_lpgbt(name='E_lpgbt',cfg=cfg)
    trg_lpgbt_C.setLoggingLevel('INFO')
    trg_lpgbt_C.set_transport(transport_ec)

    # daq_gpio_pins = [ 0 if i<14 else 1 for i in range(16) ]  #all gpio set as input except TRG lpgbt B and C resets
    # daq_lpgbt.init_gpio(daq_gpio_pins)


    #trg_lpgbt_B.reset_pin.up()
    #trg_lpgbt_C.reset_pin.up()

    setup_core(daq_lpgbt,'A')
    daq_gpio_pins = [ 0 if i<14 else 1 for i in range(16) ]  #all gpio set as input except TRG lpgbt B and C resets
    daq_lpgbt.init_gpio(daq_gpio_pins)    
    reset_pin_B = daq_lpgbt.get_gpio_pin(14)
    trg_lpgbt_B.set_reset_pin(reset_pin_B)

    reset_pin_C = daq_lpgbt.get_gpio_pin(15)
    trg_lpgbt_C.set_reset_pin(reset_pin_C)
    reset_pin_B.down()
    reset_pin_C.down()
    sleep(.1)
    reset_pin_B.up()
    reset_pin_C.up()
    sleep(1)
    setup_clocks(daq_lpgbt)

    transport_i2c_daq_lpgbt.configure(cfg=master_cfg)
    vtrx_config = { 0x00 : 0x07 }
    a_vtrx.configure(vtrx_config)
    a_vtrx.read(vtrx_config)

    setup_inputs(daq_lpgbt,'A')
    setup_outputs(daq_lpgbt)
    cfg = {'POWERUP2':6}
    daq_lpgbt.configure(cfg)

    cfg = {'POWERUP2':0}
    trg_lpgbt_B.configure(cfg)
    trg_lpgbt_C.configure(cfg)
    setup_core(trg_lpgbt_B,'B')
    setup_core(trg_lpgbt_C,'C')
    setup_inputs(trg_lpgbt_B,'B')
    setup_inputs(trg_lpgbt_C,'C')
    trg_gpio_pins = [ 1 for i in range(16) ] #all gpio set as output
    trg_lpgbt_B.init_gpio(trg_gpio_pins)
    trg_lpgbt_C.init_gpio(trg_gpio_pins)

    cfg = {'POWERUP2':6}
    trg_lpgbt_B.configure(cfg)
    trg_lpgbt_C.configure(cfg)

    cfg = {'POWERUP2':0}
    trg_lpgbt_B.configure(cfg)
    trg_lpgbt_C.configure(cfg)
    setup_core(trg_lpgbt_B,'B')
    setup_core(trg_lpgbt_C,'C')
    setup_inputs(trg_lpgbt_B,'B')
    setup_inputs(trg_lpgbt_C,'C')
    cfg = {'POWERUP2':6}
    trg_lpgbt_B.configure(cfg)
    trg_lpgbt_C.configure(cfg)

    trg_gpio_pins = [ 1 for i in range(16) ] #all gpio set as output
    trg_lpgbt_B.init_gpio(trg_gpio_pins)
    trg_lpgbt_C.init_gpio(trg_gpio_pins)
    
    daq_lpgbt.dump('/tmp/dumpDAQ_lpgbt.json')
    trg_lpgbt_B.dump('/tmp/dumpTRG_B_lpgbt.json')
    trg_lpgbt_C.dump('/tmp/dumpTRG_C_lpgbt.json')
    
    print(f'reset_pin_B.is_up() = {reset_pin_B.is_up()}') 
    print(f'reset_pin_C.is_up() = {reset_pin_C.is_up()}') 

if __name__ == '__main__':
    app()
