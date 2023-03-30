import librosa
from keyfinder import Tonal_Fragment
import os
import glob
import csv

key_emotions = {
    "C major": "Happy",
    "C# major": "Energetic",
    "D major": "Triumphant",
    "D# major": "Romantic",
    "E major": "Powerful",
    "F major": "Joyful",
    "F# major": "Majestic",
    "G major": "Positive",
    "G# major": "Passionate",
    "A major": "Hopeful",
    "A# major": "Dramatic",
    "B major": "Cheerful",
    "C minor": "Sad",
    "C# minor": "Melancholic",
    "D minor": "Powerful",
    "D# minor": "Emotional",
    "E minor": "Mysterious",
    "F minor": "Intense",
    "F# minor": "Brooding",
    "G minor": "Dramatic",
    "G# minor": "Dark",
    "A minor": "Serious",
    "A# minor": "Melancholic",
    "B minor": "Emotional",
    "A# minor": "Melancholic"
}


directory = "/Users/joaosantos/Desktop/music/musical-key-finder/MP3New"  # replace with the actual directory path
extension = "*.mp3"
path = os.path.join(directory, extension)
mp3_files = glob.glob(path)

def get_emotion(audio_path):
    y, sr = librosa.load(audio_path)
    y_harmonic, y_percussive = librosa.effects.hpss(y)

    unebarque_fsharp_maj = Tonal_Fragment(y_harmonic, sr, tend=22)

    return key_emotions[unebarque_fsharp_maj.return_key()]


def run():
    with open("output.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["File Name", "Emotion"])
            
        for file_path in mp3_files:
            file_name = os.path.basename(file_path)
            emotion = get_emotion(file_path)

            writer.writerow([file_name, emotion])

run()