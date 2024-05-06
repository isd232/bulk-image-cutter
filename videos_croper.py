import tkinter as tk
from tkinter import filedialog, messagebox, Label
from PIL import Image, ImageTk
from moviepy.editor import VideoFileClip
import os
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s) - %(message)s')


class VideoCropperApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Bulk Video Cropper Tool')
        self.setup_ui()
        #self.center_window(460, 200)

    def setup_ui(self):
        tk.Label(self.root, text='Directory:').grid(row=0, column=0)
        self.directory_entry = tk.Entry(self.root, width=50)
        self.directory_entry.grid(row=0, column=1)
        tk.Button(self.root, text='Browse', command=self.load_directory).grid(row=0, column=2)

        tk.Label(self.root, text='Output Directory:').grid(row=1, column=0)
        self.output_directory_entry = tk.Entry(self.root, width=50)
        self.output_directory_entry.grid(row=1, column=1)

        tk.Label(self.root, text='Top:').grid(row=2, column=0)
        self.top_entry = tk.Entry(self.root)
        self.top_entry.grid(row=2, column=1)

        tk.Label(self.root, text='Right:').grid(row=3, column=0)
        self.right_entry = tk.Entry(self.root)
        self.right_entry.grid(row=3, column=1)

        tk.Label(self.root, text='Bottom:').grid(row=4, column=0)
        self.bottom_entry = tk.Entry(self.root)
        self.bottom_entry.grid(row=4, column=1)

        tk.Label(self.root, text='Left:').grid(row=5, column=0)
        self.left_entry = tk.Entry(self.root)
        self.left_entry.grid(row=5, column=1)

        self.preview_label = Label(self.root)
        self.preview_label.grid(row=6, column=0, columnspan=3)
        tk.Button(self.root, text='Preview', command=self.preview_crop).grid(row=7, column=0)
        tk.Button(self.root, text='Crop All Videos', command=self.crop_all_videos).grid(row=7, column=1)

    def load_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory_entry.delete(0, tk.END)
            self.directory_entry.insert(0, directory)
            output_directory = os.path.join(directory, "Cropped_Videos")
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
            self.output_directory_entry.delete(0, tk.END)
            self.output_directory_entry.insert(0, output_directory)

    def preview_crop(self):
        try:
            top = int(self.top_entry.get())
            right = int(self.right_entry.get())
            bottom = int(self.bottom_entry.get())
            left = int(self.left_entry.get())

            directory = self.directory_entry.get()
            filenames = [f for f in os.listdir(directory) if f.endswith(".mp4")]
            if not filenames:
                raise ValueError("No MP4 files found in the directory.")
            input_file = os.path.join(directory, filenames[0])
            video = VideoFileClip(input_file)
            frame = video.get_frame(0)

            # Apply cropping to the frame for preview
            pil_image = Image.fromarray(frame)
            w, h = pil_image.size
            cropped_image = pil_image.crop((left, top, w - right, h - bottom))

            # Resize image for display if needed
            base_width = 300
            w_percent = (base_width / float(cropped_image.size[0]))
            h_size = int((float(cropped_image.size[1]) * float(w_percent)))
            resized_image = cropped_image.resize((base_width, h_size), Image.Resampling.LANCZOS)

            tk_image = ImageTk.PhotoImage(resized_image)
            self.preview_label.config(image=tk_image)
            self.preview_label.image = tk_image
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load preview: {e}")

    def center_window(self, width, height):
        # Get Screen Dimension
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Center
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def crop_all_videos(self):
        directory = self.directory_entry.get()
        output_directory = self.output_directory_entry.get()
        top = int(self.top_entry.get())
        right = int(self.right_entry.get())
        bottom = int(self.bottom_entry.get())
        left = int(self.left_entry.get())

        try:
            for filename in os.listdir(directory):
                if filename.endswith(".mp4"):
                    input_file = os.path.join(directory, filename)
                    output_file = os.path.join(output_directory, f"cropped_{filename}")

                    video = VideoFileClip(input_file)
                    w, h = video.size
                    logging.debug(f"Video loaded successfully: {input_file}")

                    cropped_video = video.crop(x1=left, y1=top, x2=w - right, y2=h - bottom)
                    if cropped_video is None:
                        logging.error("Cropping failed.")

                    cropped_video.write_videofile(output_file, codec='libx264', preset='slow',
                                                  ffmpeg_params=['-crf', '17'])
                    logging.debug("Video written successfully.")

            messagebox.showinfo("Success", "All videos have been successfully cropped!")
            self.root.destroy()
        except Exception as e:
            logging.error(f"Error processing videos: {e}")
            messagebox.showerror("Error", f"Error processing videos: {e}")
            self.root.destroy()
