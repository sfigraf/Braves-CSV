###Gets latest video clips from either parent directory (or already combined clips folder if needed)
#also deletes oldest files in already_combined_files directory if the amount of files in that directory is over 15
from moviepy.editor import *
import os
from openfile import openfile
from stopwatch import stopwatch
import shutil

from dateparser import parse


def get_clips(directory):
    #takes a directory and returns a dictionary of clips and their pitch rank within that directory
    
    directory = "./" +directory
    clip_dict = {}
    for name in os.listdir(directory):            
        if name.endswith(".mp4") and "_" not in name:
        #get pitchrank of the clip
            rank = name[0:2]
            rank = int(float(rank))
            
            if rank == None:
                print("Not adding", name, "to dated clips.")
            else:
                clip_dict.update ( {name: rank})
        
    #if the length is under 15, go to already-combined_clips
    #when using moviepy, if the clip isn't found in the first directory, look in already_combined_clips
    
    if len(clip_dict) < 15:
        #if the length is under 15, go back and check pprevious clips to see if we can combine any there
        original_length = len(clip_dict)
        if os.path.isdir(directory+"/"+"already_combined_clips"):
            for name in os.listdir(directory+"/"+"already_combined_clips"):
                
                rank = name[0:2]
                rank = int(float(rank))
                rank = rank + original_length
                clip_dict.update ( {name: rank})

        else:
            print("Only ",len(clip_dict), " clips are available for combining in .", directory)
    
    return clip_dict




def latest_clips(clip_dict, directory):
    #takes a dictionary of clip names and dates and the parent directory the clips were obtained from (already_combined_clips may be inside this main directory) 
    #returns the 15 most latest clips in the dictionary
    #deletes old video clips if there are more than 15
    #it was made a bit redundant because I made it so only 15 new clips are downloaded at a time, but it's still useful, especially its file deletion functionality 
    
    for key, value in dict(clip_dict).items(): #using dict creates a copy, which allows you to iterate over the dictionary without a runtime error
        #removes already combined video from dictionary
        if value == None:
            print("Not adding", key, "to dated clips.")
            del clip_dict[key]

        #TypeError: 'NoneType' object is not iterable solved because I wasn't returning an object with get_clips
        
        while len(clip_dict) > 15:
            #needs to iterate through each value in dictionary, otherwise while loop goes forever
            for key, value in dict(clip_dict).items():
                if value == max(clip_dict.values()):
                    if os.path.isfile("./"+directory+"/"+key) == True:
                        #if it's in the directory folder (aka just downloaded) and it's not needed in the dictionary, delete it
                        
                        print("Deleting old clip from ",directory, ": ", key)
                        os.remove("./"+directory+"/"+key)
                        
                    elif os.path.isfile("./" + directory + "/already_combined_clips/" + key) == True:
                        #if it's not in the directory folder, check already_combined_clips and remove it from there
                        print("Deleting old clip from already_combined_clips folder within ", directory, ": ", key)
                        os.remove("./" + directory + "/already_combined_clips/" + key)
            
                    #delete from the dictionary
                    del clip_dict[key]  
    
    return clip_dict



def get_video_clips(directory, clip_dict):
    #gets video clips from a folder my referencing clip_dict and prepares them for combining
    directory = "./" +directory
    #list that is fed into VideoFileClip one at a time
    moviepy_clips = []
    
    clips_to_move = [] #this is for later moving the files into the "already combined" directory
    
    for key, value in clip_dict.items(): 
        #first search general directory
        if os.path.isfile("./"+directory+"/"+key) == True:
            moviepy_clip = VideoFileClip(directory + "/" + key, fps_source = "fps") #adding fps_source = "fps" corrected it so that clips don't speed up in the final product. or maybe is was the os error. Running it now to see
            moviepy_clips.append(moviepy_clip)
            clips_to_move.append(key)
        #if clip isn't in general directory, look in the "already combined clips"    
        elif os.path.isfile("./"+directory+"/"+key) == False:
            print("Finding next most recent clips in already_combined_clips")
            moviepy_clip = VideoFileClip(directory + "/already_combined_clips/" + key, fps_source = "fps") #adding fps_source = "fps" corrected it so that clips don't speed up in the final product. or maybe is was the os error. Running it now to see
            moviepy_clips.append(moviepy_clip)
    if len(clip_dict) < 15:
        print("Only ",len(clip_dict), " clips are available for combining.")
    elif len(clip_dict) == 15:
        print("15 clips (max allowed) found for combining in ", directory)            
    
    return moviepy_clips, clips_to_move


def prepare_video_clips(directory):
    #function that puts it all together
    clip_dict = get_clips(directory)
    recent_clips = latest_clips(clip_dict, directory)
    moviepy_clips, clips_to_move = get_video_clips(directory, recent_clips)
    return moviepy_clips, clips_to_move


#if _WaitForSingleObject(self._handle, 0) == _WAIT_OBJECT_0:
#OSError: [WinError 6] The handle is invalid
#this error solved because I was trying to run __init__ and prepare_video_clips("42111_CB") wasn't commented out in this script.