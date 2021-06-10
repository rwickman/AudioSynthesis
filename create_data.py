from scipy.io import wavfile
import math, os
import numpy as np

SAMPLE_RATE = 22050
MIN_SEC = 60

wavs = []
csvs = []


# Get wav filenames
for f_name in os.listdir():
    if ".wav" in f_name:
        wavs.append(f_name)
        csvs.append(f_name.split(".")[0] + ".csv")

list_txt = "list.txt"

with open(list_txt, "w") as list_f:
    cur_clip = 1
    for i, wav in enumerate(wavs):
        # Verify corresponding CSV exists
        if os.path.exists(csvs[i]):
            os.system(f'ffmpeg -y -i {wav} -ar {SAMPLE_RATE} -ac 1 temp_{i}.wav')
            rate, data = wavfile.read(f'temp_{i}.wav')
            
            # Convert to 16 bit
            data = data.astype(np.int16)


            # Read CSV text
            with open(csvs[i]) as f:
                for line in f:
                    s = line.split(",")
                    print("s" ,s)
                    
                    # Derive time for start frame
                    frame_start_s = s[0].split(":")
                    frame_start = round((float(frame_start_s[0]) * MIN_SEC  +  float(frame_start_s[1].strip())) * rate)
                    
                    frame_end_s = s[1].split(":")
                    frame_end = round((float(frame_end_s[0]) * MIN_SEC + float(frame_end_s[1].strip())) * rate)
                    print(frame_start, frame_end, len(data))
                    text = s[2].strip()
                    if "\n" in text:
                        text = text.split("\n")[0]

                    clip = data[frame_start:frame_end]
                    cur_wav = str(cur_clip) + ".wav"
                    wavfile.write("wavs/" + cur_wav, rate, clip)

                    cur_clip_line = "wavs/" + cur_wav + "|" + text + "."
                    if cur_clip > 1:
                        # Add newline behind last line
                         cur_clip_line = "\n" + cur_clip_line
                    list_f.write(cur_clip_line)
                    cur_clip += 1
            
            os.remove(f'temp_{i}.wav')
# t = 4
 
# frame = rate * t
 
# wavfile.write("kermit_clip.wav", rate, data[frame:])