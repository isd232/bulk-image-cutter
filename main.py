import tkinter as tk
from videos_croper import VideoCropperApp
from images_croper import ImageCropperApp


class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Bulk Cropper Tool')
        self.root.geometry('270x150')

        # Creating a label frame for better appearance
        label_frame = tk.LabelFrame(self.root, text="Select an option:", padx=10, pady=10)
        label_frame.pack(padx=10, pady=10)

        # Create buttons to choose between watermarking images and videos
        tk.Button(label_frame, text='Crop Images', command=self.launch_image_cropper).pack(fill='x', pady=5)
        tk.Button(label_frame, text='Crop Videos', command=self.launch_video_cropper).pack(fill='x', pady=5)

    def launch_video_cropper(self):
        new_window = tk.Toplevel(self.root)
        VideoCropperApp(new_window)

    def launch_image_cropper(self):
        new_window = tk.Toplevel(self.root)
        ImageCropperApp(new_window)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
