"""
A program that is meant to be able to gradually increase the tempo for a
metronome after the specified amount of measures in the json config file
"""
import time
import json


#Variable initilisation
piece = "mountain_king.json"

if not piece.endswith(".json"):
    piece = piece + ".json"


piece_directory = "pieces/"
full_piece = piece_directory + piece


#load the JSON file
with open(full_piece, 'r') as file:
    data = json.load(file)


bpm = 60
beat = 0
measure = 1
time_signature = data["time signature"][0]

if data["time signature"][1] != 4:
    raise ValueError("Cannot have a base other than 4 in the time signature.")

def on_beat():
    global beat
    global measure
    global bpm
    if beat == time_signature:
        measure += 1
        beat = 1
    else:
        beat += 1
    json_measure = str(measure) + "-" + str(beat)
    if json_measure in data["tempo changes"]:
        bpm = data["tempo changes"][json_measure]
    print("Tempo: {}\nM: {}\nB: {}\n==========".format(bpm, measure, beat))


while True:
    time.sleep(60/bpm)
    on_beat()