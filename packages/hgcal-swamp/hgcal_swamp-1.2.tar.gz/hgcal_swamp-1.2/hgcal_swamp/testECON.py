import logging
import argparse
import sc_lpgbt, econ
import lpgbt_ic, lpgbt_i2c
import util
import yaml
from time import sleep

def testECON():
    cfg = { 'broadcast_address' : 2 }
    transport_ec = lpgbt_ic.lpgbt_ec(name='ec',cfg=cfg)
    transport_ec.setLoggingLevel('INFO')
    
    # west LPGBT
    cfg = { 'address' : 0x71 }
    trg_lpgbt_west = sc_lpgbt.sc_lpgbt(name='lpgbt_trg_w',cfg=cfg)
    trg_lpgbt_west.setLoggingLevel('INFO')
    trg_lpgbt_west.set_transport(transport_ec)
    trg_gpio_pins = [ 1 for i in range(16) ] #all gpio set as output
    trg_lpgbt_west.init_gpio(trg_gpio_pins)

    cfg = { 'bus' : 0 }
    transport_i2c_w_lpgbt = lpgbt_i2c.lpgbt_i2c(name='w_lpgbt.i2c.m0',cfg=cfg)
    transport_i2c_w_lpgbt.setLoggingLevel('DEBUG')
    transport_i2c_w_lpgbt.set_carrier(trg_lpgbt_west)
    master_cfg =  { 'clk_freq'           : 1, # { 0: 100 kHz, 1: 200 kHz, 2: 400 kHz, 3: 1 MHz }
                    'scl_drive'          : False,
                    'scl_pullup'         : False,
                    'scl_drive_strength' : 0,
                    'sda_pullup'         : False,
                    'sda_drive_strength' : 0
    }
    transport_i2c_w_lpgbt.configure(cfg=master_cfg)
    
    hard_reset_pin = trg_lpgbt_west.get_gpio_pin(9)
    soft_reset_pin = trg_lpgbt_west.get_gpio_pin(12)
    
    soft_reset_pin.down()
    hard_reset_pin.down()
    sleep(1)   
    soft_reset_pin.up()
    hard_reset_pin.up()
    
    cfg = {
        'address':0x20,
        'path_to_translatemap':'./regmaps/ECONT_I2C_params_regmap_translate.json',
        'path_to_validatemap':'./regmaps/ECONT_I2C_params_regmap_validate.json',
        'path_to_defaultmap':'./regmaps/ECONT_I2C_default_regmap.json',
        'use_cache':True,
        'update_all_hits':False
    }
    myecon_t = econ.econ(name = 'econt_w0', cfg=cfg)
    myecon_t.setLoggingLevel('DEBUG')
    myecon_t.set_transport(transport_i2c_w_lpgbt)

    with open('configs/econt_test_config.yaml') as fin:
        cfg = yaml.safe_load(fin)
    powerOnDefault = myecon_t.read(cfg)
    with open("./power-on-default.yaml",'w') as fout:
        yaml.dump(powerOnDefault,fout)
    
    myecon_t.configure(cfg,read_back=False)

    afterInit = myecon_t.read(cfg)

    with open("./after-init.yaml",'w') as fout:
        yaml.dump(afterInit,fout)


    cfg = {
        'address':0x60,
        'path_to_translatemap':'./regmaps/ECOND_1.8.0_I2C_params_regmap_translate.json',
        'path_to_validatemap':'./regmaps/ECOND_1.8.0_I2C_params_regmap_validate.json',
        'path_to_defaultmap':'./regmaps/ECOND_1.8.0_I2C_default_regmap.json',
        'use_cache':True,
        'update_all_hits':False
    }
    myecon_d = econ.econ(name = 'econd_w0', cfg=cfg)
    myecon_d.setLoggingLevel('DEBUG')
    myecon_d.set_transport(transport_i2c_w_lpgbt)
    with open('./configs/econd_test_config.yaml') as fin:
        cfg=yaml.safe_load(fin)

    powerOnDefault = myecon_d.read(cfg)
    with open("./power-on-default-econd.yaml",'w') as fout:
        yaml.dump(powerOnDefault,fout)
    
    myecon_d.configure(cfg,read_back=False)

    afterInit = myecon_d.read(cfg)

    with open("./after-init-econd.yaml",'w') as fout:
        yaml.dump(afterInit,fout)

if __name__ == '__main__':
    testECON()
