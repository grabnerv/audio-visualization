import librosa
import tkinter as tk
import pygame

# Replace filename with path to your song.
filename = "./Songs/Body Pump - Lady Bee Remix.mp3"
print("\nAnalyzing song...\n")

# Uses Librosa to find beat hits of song.
# Stores the beat hits in numpy array "beat_times" as an offset (in seconds) from the start of the song.
y, sr = librosa.load(filename)

tempo, beatFrames = librosa.beat.beat_track(y = y, sr = sr, hop_length=512)

print('Tempo = {:.2f} bpm'.format(tempo))

beat_times = librosa.frames_to_time(beatFrames, sr = sr)
print("Number of beat hits:", len(beat_times), "\n")
delay = int((beat_times[1] - beat_times[0]) * 1000)

# Uses pygame to access and play music file
def play_music():
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

# Function flash_light() flashes a "light" (small Tkinter GUI) between two colors at each beat hit.
# Delay between hits is calculated by subtracting two adjacent array indices,
# multiplying by 1000 to convert to milliseconds, and then casting to an integer to eliminate remaining decimal places.
def flash_light():
    flash_count = len(beat_times)
    first_value = 0

    # Recursively calls toggle_light() until there are no more values in beat_times.
    def toggle_light():
        nonlocal flash_count
        nonlocal first_value
        delay = int((beat_times[first_value] - beat_times[first_value - 1]) * 1000)
        
        # Produces weird first value due to how beat_times is being accessed.
        if(first_value != 0): print("delay:", delay, "ms") 

        first_value += 1
        current_color = light.cget("background")
        next_color = "gray" if current_color == "white" else "white"
        light.config(background=next_color)
        flash_count -= 1

        if flash_count > 0:
            light.after(delay, toggle_light)
        else:
            start_button.config(state=tk.NORMAL)  # Enable button after flashing completes

    start_button.config(state=tk.DISABLED)  # Disable button during flashing
    toggle_light()

# Tkinter stuff...
root = tk.Tk()
root.title("Light toggle")

light = tk.Label(root, width=20, height=10, background='gray')
light.pack(pady=20)

# Calls both flash_light() and play_music().
start_button = tk.Button(root, text="Toggle Light", command=lambda:(flash_light(), play_music()))
start_button.pack()

root.mainloop()