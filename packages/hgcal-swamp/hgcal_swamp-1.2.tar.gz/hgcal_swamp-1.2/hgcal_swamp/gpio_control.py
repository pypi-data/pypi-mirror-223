import logging
import argparse
import sc_lpgbt, lpgbt_gpio
import util
import yaml
from time import sleep


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-t', dest='lpgbt_target', action='store',choices=['daq', 'trg_w', 'trg_e'],
                        help='lpgbt name to control')

    parser.add_argument('-rw', dest='read_write', action='store',choices=['read', 'write'],default='read',
                        help='read write flag, 0:write , 1:read')

    parser.add_argument('-pin', dest='pin', action='store',type=int,
                        help='gpio pin to read or write')

    parser.add_argument('-dir', dest='direction', action='store',choices=['input','output'],
                        help='direction of gpio pin, only set if rw option is write')

    parser.add_argument('-o', dest='output', action='store',choices=['up','down'],
                        help='value to set to the gpio pin, only set if rw option is write')
    
    parser.add_argument('-p', dest='protocol', action='store',choices=['sct', 'emp'],default='sct',
                        help='IC protocol to use')

    args = parser.parse_args()
    print(args)

    lpgbt_address = 0x70 if args.lpgbt_target=='daq' else 0x71 if args.lpgbt_target=='trg_w' else 0x72

    if args.protocol=='sct':
        import lpgbt_ic
        cfg = { 'broadcast_address' : 1 if lpgbt_address==0x70 else 2 }
        name = 'sct_ic' if lpgbt_address==0x70 else 'sct_ec'
        transport = lpgbt_ic.lpgbt_ic(name=name,cfg=cfg) if lpgbt_address==0x70 else lpgbt_ic.lpgbt_ec(name=name,cfg=cfg)
        transport.setLoggingLevel('INFO')
    else:
        import lpgbt_ic_emp
        cfg = { }
        name = 'emp_ic' if lpgbt_address==0x70 else 'emp_ec'
        transport = lpgbt_ic_emp.lpgbt_ic_emp(name=name,cfg=cfg) if lpgbt_address==0x70 else lpgbt_ic_emp.lpgbt_ec_emp(name=name,cfg=cfg)
        transport.setLoggingLevel('INFO')
        
    cfg = { 'address' : lpgbt_address }
    lpgbt = sc_lpgbt.sc_lpgbt(name='lpgbt',cfg=cfg)
    lpgbt.setLoggingLevel('INFO')
    lpgbt.set_transport(transport)

    cfg = { 'dir' : args.direction, 'pin': args.pin }
    gpio = lpgbt_gpio.lpgbt_gpio_pin(name='name',cfg=cfg)
    gpio.set_carrier(lpgbt)
    
    if args.read_write=='read':
        status = gpio.status()
        print(f'lpgbt {args.lpgbt_target} GPIO pin {args.pin} ouput = {status}')  
    else:
        gpio.set_dir(args.dir)
        if args.output=='up':
            gpio.up()
        else:
            gpio.down()