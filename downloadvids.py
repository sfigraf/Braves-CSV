###cntrl + # for commenting out a block of code
# selected shift+tab to move over lines
import os
import csv


import requests
import shutil #for saving download

import datetime
import time
from stopwatch import stopwatch 
from openfile import openfile
from dateparser import parse



   

def downloadvid(url,directory,name):
    #downloads a single video 
    r = requests.get(url, stream=True) #stream = true so that you can access r.raw (raw socket response from server). Got rid of thhe "unverified https request being made" error by taking out the verify = False argument. auth=('usrname', 'password'), is an argument I took out, not needed
    r.raw.decode_content = True #decodes object returned by r. r.iter_content is maybe another option, it decodes encodings automatically apparently. r.raw is a raw stream of bytes, hence why they need decoding
    dest = "./"+directory+"/"+name+".mp4"
    with stopwatch("Downloading video to " + directory + "...", 'download %s bytes' % name):
        with open(dest, 'wb') as f: #wb is writing in binary mode
                shutil.copyfileobj(r.raw, f) #copies contents (r.raw) to the file-like object f


def downloadcsvvids(reader, clip_dict):
    for key, value in dict(clip_dict).items():
        for row in reader:
            if key == row["VIDEO"]:
                url = row["VIDEO"]
                date = str(row["DATE"])
                date = date.replace("/",".") #have to replace / with . for names
                pitch_rank = str(row["PitchRnk"])
        
                directory = str(row["PITCHER_PLAYER_KEY"]) + "_" + str(row["PITCH TYPE"]) 
            
                #name of the file
                #can put date in here too if needed
                name = pitch_rank + "." + url[29:-5]
            
                already_combined_clips_path = "./"+ directory + "/already_combined_clips" +"/"+name+".mp4"
                directory_path = "./"+ directory + "/"+name+".mp4"
                #checks directory to see if it's already been downloaded
                #could also potentially do it with os.walk to search all directories
                if os.path.isfile(already_combined_clips_path) == True or os.path.isfile(directory_path): #if the video is in the "already combined clips" folder or just waiting to be combined, don't download again
                
                    print(name, " already exists in ", directory)
                #if not, download
                
                else:
                    downloadvid(url,directory,name)



    
        

           

