# -*- coding: utf-8 -*-
import numpy as np
import time,argparse
from wlm import WavelengthMeter
from toptica import laser
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
    
    start_wav = 1300
    stop_wav = 1320
    
    dlpro = laser()   
    start_pos = dlpro.get_wav_pos(start_wav)
    stop_pos = dlpro.get_wav_pos(stop_wav)
    
    pos_range = range(start_pos,stop_pos+1)    
    wav_actual = np.zeros(len(pos_range))
    pow_actual = np.zeros(len(pos_range))
    
    print("Scan starting...")
    for i in range(len(pos_range)):
        dlpro.set_motor(pos_range[i])
        time.sleep(5)    
        wav_actual[i] = round(wlm.wavelength,3)
        pow_actual[i] = wlm.power
        
    print("Scan finished. Have a nice day!")
    
    
    plt.rcParams.update({'font.size': 20})

    fig, axs = plt.subplots(1, 1, constrained_layout=True,figsize=(20,10))
    
    axs.set_ylabel('power (uW)')
    axs.set_xlabel('wavelength (nm)')
    
    axs.plot(wav_actual,pow_actual)
