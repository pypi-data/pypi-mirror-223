import logging
import argparse
import sc_lpgbt
import lpgbt_ic, roc, lpgbt_i2c
import util
import yaml
import re
from time import sleep


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', dest='site', action='store',choices=['w0','w1','w2','e0','e1','e2'],
                        help='hexaboard site')

    parser.add_argument('-a', dest='roc_addr', action='store',default='0x08',
                        help='HGCROC I2C base address')

    parser.add_argument('-rw', dest='read_write', action='store',choices=['read', 'write'],default='read',
                        help='read write flag, 0:write , 1:read')

    parser.add_argument('-f', dest='config', action='store',
                        help='path to config file')

    parser.add_argument('-of', dest='oconfig', action='store',
                                help='path to output yaml config  file')

    parser.add_argument('-pname', dest='param_name', action='store',
                        help='roc parammeter name to read or write, expected format : block.subblock.paramname')
    
    parser.add_argument('-v', dest='val', action='store',type=int,default=0,
                        help='value to write in roc parameter')

    parser.add_argument('-p', dest='protocol', action='store',choices=['sct', 'emp'],default='sct',
                        help='IC protocol to use')

    args = parser.parse_args()
    print(args)

    lpgbt_address = 0x71 if args.site.find('w')>=0 else 0x72

    if args.protocol=='sct':
        cfg = { 'broadcast_address' : 2 }
        name = 'sct_ec'
        transport = lpgbt_ic.lpgbt_ec(name=name,cfg=cfg)
        transport.setLoggingLevel('INFO')
    else:
        cfg = { }
        name = 'emp_ec'
        import lpgbt_ic_emp
        transport = lpgbt_ic_emp.lpgbt_ec_emp(name=name,cfg=cfg)
        transport.setLoggingLevel('INFO')
        
    cfg = { 'address' : lpgbt_address }
    lpgbt = sc_lpgbt.sc_lpgbt(name='lpgbt',cfg=cfg)
    lpgbt.setLoggingLevel('INFO')
    lpgbt.set_transport(transport)

    bus=re.search('(\d+)',args.site)
    if bus:
        bus=bus.group(0)
        print(f'will use bus {bus} of lpgbt {lpgbt.name}')
    else:
        raise ValueError(
            f"{args.site} does not have a site ID (0,1 or 2) "
        )
    
    cfg = { 'bus' : int(bus) }
    transport_i2c = lpgbt_i2c.lpgbt_i2c(name='lpgbt.i2c',cfg=cfg)
    transport_i2c.setLoggingLevel('INFO')
    transport_i2c.set_carrier(lpgbt)
    master_cfg =  { 'clk_freq'           : 1, # { 0: 100 kHz, 1: 200 kHz, 2: 400 kHz, 3: 1 MHz }
                    'scl_drive'          : False,
                    'scl_pullup'         : False,
                    'scl_drive_strength' : 0,
                    'sda_pullup'         : False,
                    'sda_drive_strength' : 0
    }
    transport_i2c.configure(cfg=master_cfg)

    aroc = roc.roc(name = 'roc', cfg={'address':int(args.roc_addr,16)})
    aroc.set_transport(transport_i2c)
    aroc.setLoggingLevel('INFO')
    
    if args.config is not None:
        with open(args.config) as fin:
            config = yaml.safe_load(fin)
    else:
        block, subblock, pname = args.param_name.split('.')
        config = { block : { subblock : { pname: args.val } } }
    
    if args.read_write=='read':
        read_content = aroc.read(config)
        if args.oconfig is not None:
          with open(args.oconfig, 'w') as outfile:
            yaml.dump(read_content, outfile, default_flow_style=False)
        else:
          print(yaml.dump(read_content))
        #debug_reg = aroc.read_reg(0x6f, 0x05)
        #print(debug_reg)
    else:
        aroc.configure(config)
