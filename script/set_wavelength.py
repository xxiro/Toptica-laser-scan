# -*- coding: utf-8 -*-
import numpy as np
import time
from wlm import WavelengthMeter
import argparse
from toptica import laser

if __name__ == '__main__':
    # command line arguments parsing
    parser = argparse.ArgumentParser(description='Reads out wavelength values from the High Finesse Angstrom WS7 wavemeter.')
    parser.add_argument('--debug', dest='debug', action='store_const',
                        const=True, default=False,
                        help='runs the script in debug mode simulating wavelength values')
    parser.add_argument('channels', metavar='ch', type=int, nargs='*',
                        help='channel to get the wavelength, by default all channels from 1 to 8',
                        default=range(1,8))

    args = parser.parse_args()

    wlm = WavelengthMeter(debug=args.debug) 

    dlpro = laser()
    print(dlpro.get_wav_pos(1280.0))	
    dlpro.set_motor(dlpro.get_wav_pos(1280.0))
    print(wlm.power)
    time.sleep(5)    
    
    
    
