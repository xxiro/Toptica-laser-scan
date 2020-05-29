import pickle
import dlpromotor as motor
import os,sys
import numpy as np

class laser():

    def __init__(self):

        laser_parameters = [
            1330,
            1320,
            1310,
            1300,
            ]

        default_values = [0] * len(laser_parameters)
        cwd = os.getcwd()
        main_path=os.path.split(cwd)
        main_path=main_path[0]
        self.pkl_dir = os.path.join(main_path,"toptica laser")

        #load values
        try:            
            self.dict = self.load_obj("DL_1310")
        except:
            #if they don't exist 
            #combine two lists to make a dictionary
            self.dict = dict(zip(laser_parameters, default_values))
            self.save_obj(self.dict,"DL_1310")
        
    # def update_parameter(self, key, val):
    #     """
    #     Updates the corresponding value of a key in the dictionary
    #     """
    #     cwd = os.getcwd()
    #     main_path=os.path.split(cwd)
    #     main_path=main_path[0]
            
    #     if key in self.dict:
    #         self.dict[key] = val
    #         self.save_obj(self.dict,os.path.join(main_path,"toptica laser","DL_1310"))
    #     else:
    #         print("%s does not exist" %key)
    
    def save_obj(self,obj, name ):
        with open(os.path.join(self.pkl_dir, name)+ '.pkl', 'wb+') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
            f.close()

    def load_obj(self,name ):
        while True:
            try:
                with open(os.path.join(self.pkl_dir, name) + '.pkl', 'rb') as f:
                    data=pickle.load(f)
                    break
            except EOFError:
                print("EOFError!!!!!!!")
                pass
        f.close()
        return data
 
    def get_wav_pos(self, wavelength):
        data = self.dict
        try:
            pos = data[wavelength]
        except KeyError:
            all_wav = np.array(list(data.keys()))
            nearest_idx = np.abs(all_wav - wavelength).argmin()
            nearest = all_wav[nearest_idx]
            pos = data[nearest]
        return pos
            
    def set_wavelength(self, wavelength):
        pos = self.get_wav_pos(wavelength)
        motor.set_position(pos)
        
    def set_motor(self, pos):
        motor.set_position(pos)    
        
    
