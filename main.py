import tkinter as tk
from videos_croper import VideoCropperApp
from images_croper import ImageCropperApp


class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Media Cropping Tool')

        # Create buttons to choose between video and image cropping
        tk.Button(root, text='Crop Video', command=self.launch_video_cropper).pack(pady=20)
        tk.Button(root, text='Crop Image', command=self.launch_image_cropper).pack(pady=20)

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
