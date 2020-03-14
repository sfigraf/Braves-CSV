#combine movie clips with moviepy 
#moviepy uses ffmpeg. To get these to run, ou have to download ffmpeg and put its executable (found in the bin folder) in the same directory as this file
#this script gets video clips, checks if they've already been combined (they're in already_combined_clips folder), combines them if needed, then moves them to already_combined_clips folder
from moviepy.editor import *
import os
from openfile import openfile
from stopwatch import stopwatch
from prepare_video_clips import prepare_video_clips
import shutil

from dateparser import parse

#this function moves files to already_combined_clips
def move_clips(directory, video_clip_names):
    
    #if there's already a combined video in the list, remove it so it stays in the same directory
    if directory+".mp4" in video_clip_names:
        video_clip_names.remove(directory+".mp4")
    elif directory + "_1.mp4" in video_clip_names:
        video_clip_names.remove(directory+"_1.mp4")
     
    path = "./"+directory + "/already_combined_clips"
    
    if os.path.exists(path) == False:
        os.mkdir(path)
        print("New directory already_combined_clips made in ", directory, " directory.")
    
    for clip in video_clip_names:
        os.replace(directory + "/"+str(clip), path + "/" + str(clip)) #get permission error sometimes when trying to move the clips
        #shutil.move(directory + "/"+str(clip), path + "/" + str(clip))
    print("Clips moved to already_combined_clips folder within the", directory, " directory.")
    
    

    

def create_combined_video(directory, moviepy_clips, clips_to_move):
    
    
   
     
    with stopwatch("Concatenating Video Clips from %s" % directory, 'concatenated %s directory' % directory):
        #w = max([r[0] for r in sizes])
        #ValueError: max() arg is an empty sequence.
        #this error was occurring because I was skipping "get_video_clips" if there weren't any clips to add to the final clip, but I was calling that within "get_video_clips"
        #so if I jsut move that logic to the combine_vid_in_all_folders, I won't be trying to feed an empty list to this function
        video = concatenate_videoclips(moviepy_clips, method = "compose")
        
    with stopwatch("Writing combined video of %s..." % directory, 'exported concatenated %s video' % directory):
        #libx264 is default for .mp4. If i didn't add this argument it would use this codec anyway
        video.write_videofile("./" + directory + "/" + directory + ".mp4", preset = "fast", verbose = False, threads = 4,codec = 'libx264') #ultrafast setting quickest, but makes a large video file. might need to add an argument for fps = 58 if video clips speed up in final clip, but it's fine for now. 58 comes from average fps in inidivual clips, found in clip properties
       #second directory was unique filename: (either pitcher_pitch or pitcher_pitch_1)
    
    #this closes all clips in the list and gets around the PermissionError: [WinError 32] The process cannot access the file because it is being used by another process:
    #actually it doesn't quite eliminate it; if it persists, try closing IDE, going to problem directory and deleting problem video if needed.
    #it might happen sometimes from trying to combine video but getting interrupted halfway through
    for clip in moviepy_clips:
        clip.close()
    #moves clips that were just added to the video to the "already combined clips" folder
    #maybe could be put in init instead
    move_clips(directory,clips_to_move)
        


#Error: AttributeError: 'NoneType' object has no attribute 'stdout' solved by downgrading moviepy to 1.0.0 (pip install moviepy==1.0.0)
#combine_vids_in_all_folders()
    

