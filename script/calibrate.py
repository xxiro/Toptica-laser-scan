# -*- coding: utf-8 -*-

import argparse,time
from wlm import WavelengthMeter
from toptica import laser
import numpy as np
import matplotlib.pyplot as plt

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
    lase_range = range(548000,741000+1,100)
    wav_actual = np.zeros(len(lase_range))
    pow_actual = np.zeros(len(lase_range))
    print("move to starting position")
    dlpro.set_motor(548000)
    time.sleep(5)
    
    print("Scan starting...")
    for i in range(len(lase_range)):
        dlpro.set_motor(lase_range[i])
        wav_actual[i] = round(wlm.wavelength,3)
        pow_actual[i] = wlm.power
        
    wav_pos_dict = dict(zip(wav_actual, lase_range))
    wav_pow_dict = dict(zip(wav_actual, pow_actual))
    
    dlpro.save_obj(wav_pos_dict,"DL_1310")   
    dlpro.save_obj(wav_pow_dict,"DL_1310_power_spectrum")   
    print("Scan finished. Have a nice day!")
    
    
    plt.rcParams.update({'font.size': 20})

    fig, axs = plt.subplots(1, 1, constrained_layout=True,figsize=(20,10))
    
    axs.set_ylabel('power (uW)')
    axs.set_xlabel('wavelength (nm)')
    
    axs.plot(wav_actual,pow_actual)