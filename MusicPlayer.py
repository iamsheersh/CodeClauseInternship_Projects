import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pygame import mixer
from mutagen.mp3 import MP3



class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("400x400")
        self.root.configure(background="#2f3640")  # Dark blue background

        # Create GUI components
        self.folder_label = tk.Label(root, text="Select a folder:", bg="#2f3640", fg="#fff", font=("Helvetica", 12))
        self.folder_label.pack(pady=10)

        self.folder_entry = tk.Entry(root, width=30, bg="#4f5b66", fg="#fff", font=("Helvetica", 12))  # Dark gray background
        self.folder_entry.pack(pady=10)

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_folder, bg="#34a853", fg="#fff", font=("Helvetica", 12))  # Green button
        self.browse_button.pack(pady=10)

        self.controls_frame = tk.Frame(root, bg="#2f3640")
        self.controls_frame.pack(pady=10)

        self.play_button = tk.Button(self.controls_frame, text="Play", command=self.play_music, bg="#34a853", fg="#fff", font=("Helvetica", 12))  # Green button
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(self.controls_frame, text="Pause", command=self.pause_music, bg="#f7dc6f", fg="#fff", font=("Helvetica", 12))  # Yellow button
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(self.controls_frame, text="Stop", command=self.stop_music, bg="#e74c3c", fg="#fff", font=("Helvetica", 12))  # Red button
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.song_listbox_label = tk.Label(root, text="Songs:", bg="#2f3640", fg="#fff", font=("Helvetica", 12))
        self.song_listbox_label.pack(pady=10)

        self.song_listbox = tk.Listbox(root, width=30, height=10, bg="#4f5b66", fg="#fff", font=("Helvetica", 12))  # Dark gray background
        self.song_listbox.pack(pady=10)

        self.song_label = tk.Label(root, text="", bg="#2f3640", fg="#fff", font=("Helvetica", 12))
        self.song_label.pack(pady=10)

        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate", style="Horizontal.TProgressbar")
        self.progress_bar.pack(pady=10)

        self.time_label = tk.Label(root, text="", bg="#2f3640", fg="#fff", font=("Helvetica", 12))
        self.time_label.pack(pady=10)

        # Initialize variables
        self.folder_path = ""
        self.music_files = []
        self.current_song = 0
        self.playing = False

        # Style for progress bar
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Horizontal.TProgressbar", foreground="#34a853", background="#4f5b66")

        # Initialize pygame mixer
        mixer.init()

    def browse_folder(self):
        self.folder_path = filedialog.askdirectory()
        self.folder_entry.delete(0, tk.END)
        self.folder_entry.insert(0, self.folder_path)
        self.music_files = [os.path.join(self.folder_path, file) for file in os.listdir(self.folder_path) if file.endswith(('.mp3', '.wav'))]
        self.update_song_listbox()

    def update_song_listbox(self):
        self.song_listbox.delete(0, tk.END)
        for file in self.music_files:
            self.song_listbox.insert(tk.END, os.path.basename(file))

    def play_music(self):
        if not self.playing:
            self.playing = True
            self.play_button.config(text="Play")
            self.pause_button.config(text="Pause")
            self.stop_button.config(text="Stop")
            self.play_song()

    def pause_music(self):
        if self.playing:
            self.playing = False
            self.pause_button.config(text="Resume")
            mixer.music.pause()

    def stop_music(self):
        self.playing = False
        self.pause_button.config(text="Pause")
        mixer.music.stop()

    def play_song(self):
        if self.music_files:
            song_path = self.music_files[self.current_song]
            mixer.music.load(song_path)
            mixer.music.play()
            self.update_song_info(song_path)
            self.update_progress_bar()
            self.next_song_after_current_song_ends()
        else:
            messagebox.showerror("Error", "No music files found in the selected folder.")

    def update_song_info(self, song_path):
        audio = MP3(song_path)
        self.song_label.config(text=f"Title: {audio.tags['TIT2'].text[0]}\nArtist: {audio.tags['TPE1'].text[0]}\nDuration: {audio.info.length:.2f} seconds")
        self.time_label.config(text="00:00 / 00:00")

    def update_progress_bar(self):
        if self.playing:
            current_time = mixer.music.get_pos() / 1000
            song_duration = MP3(self.music_files[self.current_song]).info.length
            self.progress_bar.config(value=current_time / song_duration * 100)
            self.time_label.config(text=f"{int(current_time // 60):02d}:{int(current_time % 60):02d} / {int(song_duration // 60):02d}:{int(song_duration % 60):02d}")
            self.root.after(1000, self.update_progress_bar)
        else:
            self.progress_bar.config(value=0)

    def next_song_after_current_song_ends(self):
        if self.playing:
            self.root.after(int(MP3(self.music_files[self.current_song]).info.length * 1000), self.next_song)

    def next_song(self):
        self.current_song += 1
        if self.current_song >= len(self.music_files):
            self.current_song = 0
        self.play_song()

root = tk.Tk()
music_player = MusicPlayer(root)
root.geometry("400x600")
root.mainloop()
