import logging
import argparse
import sc_lpgbt
import lpgbt_ic
import util
import yaml
from time import sleep


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-t', dest='lpgbt_target', action='store',choices=['daq', 'trg_w', 'trg_e'],
                        help='lpgbt name to control')

    parser.add_argument('-rw', dest='read_write', action='store',choices=['read', 'write'],default='read',
                        help='read write flag, 0:write , 1:read')

    parser.add_argument('-f', dest='config', action='store',
                        help='path to config file')

    parser.add_argument('-reg', dest='reg', action='store',
                        help='lpgbt register name to read or write')
    
    parser.add_argument('-v', dest='val', action='store',type=int,
                        help='value to write in lpgbt register')

    parser.add_argument('-p', dest='protocol', action='store',choices=['sct', 'emp'],default='sct',
                        help='IC protocol to use')

    args = parser.parse_args()
    print(args)

    lpgbt_address = 0x70 if args.lpgbt_target=='daq' else 0x71 if args.lpgbt_target=='trg_w' else 0x72

    if args.protocol=='sct':
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

    config=None
    if args.config is not None:
        with open(args.config) as fin:
            config = yaml.safe_load(fin)
    elif args.reg is not None:
        config = { args.reg : args.val }
    
    if args.read_write=='read':
        if config is not None: 
            read_back = lpgbt.read(config)
            print(read_back)
        else:
            print('lpgbt dump in /tmp/{args.lpgbt_target}.json')
            lpgbt.dump(f'/tmp/{args.lpgbt_target}.json')  
    else:
        lpgbt.configure(config)   
