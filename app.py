import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from video_to_subtitles import process_video

class VideoToSubtitlesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video to Multilingual Transcripts (Auto-detect → English → Telugu)")
        self.root.geometry("450x250")

        # File selection
        self.file_label = tk.Label(root, text="No file selected")
        self.file_label.pack(pady=10)

        self.select_button = tk.Button(root, text="Select MP4 File", command=self.select_file)
        self.select_button.pack()

        # Model selection
        self.model_label = tk.Label(root, text="Whisper Model:")
        self.model_label.pack(pady=5)

        self.model_var = tk.StringVar(value="small")
        self.model_combo = ttk.Combobox(root, textvariable=self.model_var,
                                       values=["tiny", "base", "small", "medium", "large"])
        self.model_combo.pack()

        # Process button
        self.process_button = tk.Button(root, text="Process Video", command=self.process_video, state=tk.DISABLED)
        self.process_button.pack(pady=20)

        self.file_path = None

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
        if file_path:
            self.file_path = file_path
            self.file_label.config(text=os.path.basename(file_path))
            self.process_button.config(state=tk.NORMAL)

    def process_video(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please select a file first")
            return

        model_size = self.model_var.get()
        self.process_button.config(state=tk.DISABLED, text="Processing...")
        self.root.update()

        success = process_video(self.file_path, model_size)

        self.process_button.config(state=tk.NORMAL, text="Process Video")

        if success:
            messagebox.showinfo("Success", "Processing complete! Check the output files in the same directory.")
        else:
            messagebox.showerror("Error", "Processing failed!")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoToSubtitlesApp(root)
    root.mainloop()
