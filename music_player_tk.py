"""
This is a tkinter music player
Handmade by TACO-CAT2
(with a little help from his pal ash...)
you can add a song from anywhere in your OS
This can play, pause, and skip through a playlist
you can add multiple songs to your playlist which can be viewed
under the buttons.
there is also a volume slider that can change the volume
"""


import tkinter as tk
from pygame import mixer
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import PhotoImage as poe
import os

mixer.init()

win = tk.Tk()
win.title("player 2.0")
win.geometry("500x400")
win.songs = []
win.display = []
win.current = None
win.playfirst = True
win.playsecond = False

back_image = poe(file="./images/back.png")
play_image = poe(file="./images/play.png")
pause_image = poe(file="./images/pause.png")
stop_image = poe(file="./images/stop.png")
next_image = poe(file="./images/next.png")

def back_func():
    """button to go to the previous song in the playlist"""
    try:
        playlist.selection_clear(win.current)
        win.current -= 1
        playlist.selection_set(win.current)
        playlist.activate(win.current)
        mixer.music.load(win.songs[win.current])
        win.playfirst = False
        mixer.music.play()
        play_button["image"] = pause_image
    except:
        pass


def play_func():
    """ button to both play the song for the first time,
        after first click it acts as a play pause button"""
    try:
        if win.playfirst:
            win.playfirst = False
            mixer.music.play()
            play_button["image"] = pause_image
        
        elif not win.playfirst:
            if not win.playsecond:
                win.playsecond = True
                mixer.music.pause()
                play_button["image"] = play_image
            else:
                win.playsecond = False
                mixer.music.unpause()
                play_button["image"] = pause_image
            
        
    except:
        pass
    
    
    
def stop_func():
    """ stops (restarts when played) the song"""
    mixer.music.stop()
    play_button["image"] = play_image
    win.playfirst = True
    
    
def next_func():
    """button to go to the next song in the playlist"""
    try:
        playlist.selection_clear(win.current)
        win.current += 1
        playlist.selection_set(win.current)
        playlist.activate(win.current)
        mixer.music.load(win.songs[win.current])
        win.playfirst = False
        mixer.music.play()
        play_button["image"] = pause_image
        
    except:
        pass
        
def add_songs_func():
    """single menubar function to open a file dialoge.
        this adds songs to the playlist from any folder"""
    filetypes = (
        ('All files', '*.*'),
        ('mp3 files', '*.mp3'),
        ('wav files', '*.wav'),
        ('flac files', '*.flac'),
        ('ogg files', '*.ogg')
    )
    
    new_song = fd.askopenfilename(
        title="add song",
        initialdir='.',
        filetypes=filetypes)
    
    if new_song != "":
        win.songs.append(new_song)
        short_name = os.path.split(new_song)[1]
        win.display.append(short_name)
        win.songlist.set(win.display)
    
def playlist_func(event):
    """allows users to select a song"""
    try:
        cursel = playlist.curselection()[0]
        win.current = cursel
        nowp["text"] = f"I am now playing {win.display[cursel]}"
        mixer.music.load(win.songs[cursel])
        win.playfirst = True
        play_button["image"] = play_image
    except:
        pass
    
def vol_changer_func(event):
    """response to changes in the volider and updates
        the mixers volume value"""
    mixer.music.set_volume(vol_val.get() / 100)

menubar = tk.Menu(win)
win["menu"] = menubar

add_songs = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label="add songs",
                    menu=add_songs,
                    underline=4)
add_songs.add_command(
    label='add songs',
    command=add_songs_func)

words_of_wisdom = "Load a song..." 
con_frame = tk.Frame(win)


nowp = tk.Label(con_frame, text=words_of_wisdom,
                font=("", 15), borderwidth=1,
                relief="solid")
back_button = tk.Button(con_frame, image=back_image,
                        command=back_func)
play_button = tk.Button(con_frame, image=play_image,
                        command=play_func)
stop_button = tk.Button(con_frame, image=stop_image,
                        command=stop_func)
next_button = tk.Button(con_frame, image=next_image,
                        command=next_func)

vol_val = tk.IntVar()
volider = tk.Scale(
    con_frame,
    from_=0,
    to=100,
    orient="horizontal",
    variable=vol_val,
    length=300,
    width=25,
    command=vol_changer_func)
volider.set(10)


play_frame = tk.Frame(win)

win.songlist = tk.StringVar(value=win.display)
playlist = tk.Listbox(play_frame,
                      width=40,
                      listvariable=win.songlist,
                      height=6,
                      font=("", 15))
playlist.bind("<<ListboxSelect>>", playlist_func)


con_frame.pack()
nowp.grid(row=0, ipadx=50, ipady=10, columnspan=4)
back_button.grid(row=1, column=0)
play_button.grid(row=1, column=1)
stop_button.grid(row=1, column=2)
next_button.grid(row=1, column=3)
volider.grid(row=2, column=0, columnspan=4)
play_frame.pack()
playlist.pack(expand=True, fill=tk.BOTH)


win.mainloop()