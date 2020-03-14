
#if the video is in a row with CH, it goes into the CH directory
#if there isn't a directory called CH, make one
#from downloadvids import openfile #"got rid of "downloadvids is not a module "error because i was trying to go from downloadvids.py
import os
import shutil

#from openfile import openfile

def makedirs(reader):
    ###checks to see if a directory exists for a player and his pitches, makes a directory if not
    for row in reader:
        path = "./"+str(row["PITCHER_PLAYER_KEY"]) + "_" +str(row["PITCH TYPE"])
        #print(path)
        if os.path.exists(path) == False:
            os.mkdir(path)
            print("New directory" + "/"+str(row["PITCHER_PLAYER_KEY"]) + "_" +str(row["PITCH TYPE"]) + " made.")
            

#path = "C://Users//sfigr//Dropbox//Videos"

#shutil.move(f.name, path)

##def move_all(destination):
##    #for dn, dirs, files in os.walk("."):
##    #for dir in dirs:
##    for dir in os.listdir("."):
##        if os.path.isdir(dir):
##        
##            
##            if dir.startswith('.'):
##                print('Skipping dot file:', dir)
##            elif dir.startswith('@') or dir.endswith('~'):
##                print('Skipping temporary file:', dir)
##            elif dir.endswith('.pyc') or dir.endswith('.pyo'):
##                print('Skipping generated file:', dir)
##            elif dir.endswith('.py'): 
##                print('Skipping python script:', dir)
##            elif dir == '__pycache__':
##                print('Skipping generated directory:', dir)
##            elif dir == '.git':
##                print('Skipping .git directory:', dir)
##            
##            
##            else:
##                shutil.move(dir, destination)
##        
##move_all(path)
    #moves 
        
##FILE = "bravesvideos.csv"
##reader = openfile(FILE)
##makedirs(reader)

