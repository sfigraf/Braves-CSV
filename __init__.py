###Main program to run 
#best ran from shell: python __init__.py because moviepy's progress bar works best like that
import os
import gc #garbage collector

from openfile import openfile
from get_latest_csv_clips import unique, latest_csv_clips
from downloadvids import downloadcsvvids
from folders import makedirs
from prepare_video_clips import prepare_video_clips
from combinevids import create_combined_video
from yesno import yesno, args
from stopwatch import stopwatch

#file you want to get vids from
FILE = "bravesvideos2.csv"


reader = openfile(FILE)

makedirs(reader)

pitcherlist = unique(reader)

def download_latest_clips(pitcherlist,reader):
    
    for entry in pitcherlist:
        #for each unique entry in pitcherlist, make a dictionary of 15 msot recent clips from csv, and download them
        clip_dict = latest_csv_clips(reader, entry)
        downloadcsvvids(reader, clip_dict)
        

download_latest_clips(pitcherlist,reader)

###combines vids in all folders 
def combine_vids_in_all_folders():
    #iterates through folders/directories within the main directory (".")
    for directory in os.listdir("."): #os.walk generates filenames in a directory tree.
        #if it's a directory (not a file), look inside
        if os.path.isdir("./"+directory) == True:
            #if there aren't any new files to add to the final clip, the folder is up to date
            num_vids_to_be_combined = len([name for name in os.listdir(directory) if name.endswith(".mp4")])
            #if there's only one video in the directory, it doesn't need to be combined
            if num_vids_to_be_combined == 1:
                print("Videos are combined up to date in " + directory + " directory.")
            else:
                if directory == '__pycache__':
                    print('Skipping generated directory:', directory)
                elif directory.startswith('.'):
                    print('Skipping dot file:', directory)    
                else:
                    
                    moviepy_clips, clips_to_move = prepare_video_clips(directory)
                    create_combined_video(directory, moviepy_clips, clips_to_move)
                    gc.collect() #avoids fragmenting memory, avoids memory error that occurs because clip instances aren't being deleted 
 

#args are defined in yesno.py
if yesno("Combine clips in all folders", True, args):
    with stopwatch("Combining all vids...", "Combining all videos"):
        combine_vids_in_all_folders()



