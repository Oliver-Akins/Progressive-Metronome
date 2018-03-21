"""
A program that is meant to be able to gradually increase the tempo for a
metronome after the specified amount of measures in the json config file
"""





# ENTER PIECE FILE NAME HERE:
piece = "mountain_king.json"
#############################






import time
import json
from pygame import mixer



#Check if they added the file extension
if not piece.endswith(".json"):
    piece = piece + ".json"



# Directory to the piece files.
piece_directory = "pieces/"
full_piece = piece_directory + piece


#load the JSON file
with open(full_piece, 'r') as file:
    data = json.load(file)



# Initialize generic variables
bpm = data["initial tempo"]
beat = 0
measure = 1
time_signature = data["time signature"]
audio_path = "audio/"
mixer.init()


audio_set = {
    "norm": audio_path + data["options"]["audio"]["normal"],
    "acnt": audio_path + data["options"]["audio"]["accented"]
}


#Create function for metronome
def on_beat():
    global beat
    global measure
    global bpm


    #Check if the beat is the same as the time signature
    if beat == time_signature:
        measure += 1
        beat = 1
    else:
        beat += 1


    #Check if we are at a JSON indicated measure-beat combo
    json_measure = str(measure) + "-" + str(beat)
    if json_measure in data["tempo changes"]:
        bpm = data["tempo changes"][json_measure]


    #Check if we are emitting audio frequency
    if data["options"]["interface"]["audio"]:

        #Check if we are playing the beat accented or not
        if beat in data["options"]["accented beats"]:
            mixer.music.load(audio_set["acnt"])
        else:
            mixer.music.load(audio_set["norm"])
        mixer.music.play()
    
    #Check if we are emitting a terminal signal
    if data["options"]["interface"]["visual"]:
        print("Tempo: {}\nM: {}\nB: {}\n==========".format(bpm, measure, beat))



#Loop until the final measure of the song
while measure <= data["total measures"]:
    #Sleep for the required amount of time before intitiating metronome
    time.sleep(60/bpm)
    on_beat()