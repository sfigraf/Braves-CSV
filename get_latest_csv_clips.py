#gets latest clips from csv file in preparation for downloading them
from openfile import openfile


def unique(reader):
    #reads the csv and returns all unique pitchers/pitchtypes in it
    #does it by making a list of all the entries, then makes another unique list based of that list
    pitcherlist = []
    list1 = []
    for row in reader:
        
        pitcher_name_type = str(row["PITCHER_PLAYER_KEY"]) + "_" + str(row["PITCH TYPE"])
        list1.append(pitcher_name_type)
    
        for x in list1:
            
            if x not in pitcherlist:
                pitcherlist.append(x)
               
    return pitcherlist

#
def latest_csv_clips(reader, entry):
    #for entry in pitcherlist:
        #for each entry in the list of unique entries, create a dictionary
        #it will have both url and pitch_rank in it
    clip_dict = {}
    for row in reader:
        
        pitcher_name_type = str(row["PITCHER_PLAYER_KEY"]) + "_" + str(row["PITCH TYPE"])
        #if the entry in csv is the same as the entry in the list, find the url and date and put them together in the dictionary
        if pitcher_name_type == entry:
            url = row["VIDEO"]
            #if I go by pitch rank,
            pitch_rank = int(row["PitchRnk"]) #this is how you can be able to see MAX  value
            
            clip_dict.update ( {url: pitch_rank}) #this is a full dictionary
            
    #examine values in dicionary
    #can do while loop
    while len(clip_dict) > 15: 
        
        for key, value in dict(clip_dict).items():
        #if the length of the dicitonary is greater than 15, 
            
            if value == max(clip_dict.values()):
                
                #remove the oldest clips from the dictionary
                del clip_dict[key]
    #now based in the keys in the dictionary, we want to download those entries
    
    return clip_dict 

