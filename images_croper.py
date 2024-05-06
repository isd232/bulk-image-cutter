import tkinter as tk
from tkinter import filedialog, messagebox, Label
from PIL import Image, ImageTk
import os


class ImageCropperApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Bulk Image Cropper')
        self.setup_ui()
        self.center_window(460, 200)

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
        tk.Button(self.root, text='Crop All Images', command=self.crop_all_images).grid(row=7, column=1)

    def center_window(self, width, height):
        # Get Screen Dimension
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Center
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def load_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory_entry.delete(0, tk.END)
            self.directory_entry.insert(0, directory)
            output_directory = os.path.join(directory, "Cropped_Images")
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
            filenames = [f for f in os.listdir(directory) if f.endswith(('.png', '.jpg', '.jpeg'))]
            if not filenames:
                raise ValueError("No image files found in the directory.")
            input_file = os.path.join(directory, filenames[0])
            img = Image.open(input_file)
            w, h = img.size
            cropped_image = img.crop((left, top, w - right, h - bottom))

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


    def crop_all_images(self):
        directory = self.directory_entry.get()
        output_directory = self.output_directory_entry.get()
        top = int(self.top_entry.get())
        right = int(self.right_entry.get())
        bottom = int(self.bottom_entry.get())
        left = int(self.left_entry.get())

        skipped_files = 0
        processed_files = 0
        try:
            for filename in os.listdir(directory):
                if filename.endswith(('.png', '.jpg', '.jpeg')):
                    img_path = os.path.join(directory, filename)
                    img = Image.open(img_path)
                    w, h = img.size
                    if (w - right) <= left or (h - bottom) <= top:
                        skipped_files += 1
                        continue
                    cropped_image = img.crop((left, top, w - right, h - bottom))
                    cropped_image.save(os.path.join(output_directory, f"cropped_{filename}"))
                    processed_files += 1

            messagebox.showinfo("Success",
                                f"All images have been successfully cropped!\nProcessed: {processed_files}\nSkipped: {skipped_files}")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error processing images: {e}")
            self.root.destroy()
