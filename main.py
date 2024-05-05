from tkinter import filedialog, messagebox
from PIL import Image
import tkinter as tk
import os


def crop_images():
    source_folder = filedialog.askdirectory(title='Select Source Folder')
    target_folder = filedialog.askdirectory(title='Create or Select Target Folder')

    # Margins are expected as (top, left, bottom, right)
    margins = tuple(map(int, entry.get().split(',')))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    skipped_files = 0
    processed_files = 0
    for filename in os.listdir(source_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(source_folder, filename)
            img = Image.open(img_path)

            # Compute the new crop coordinates
            left = margins[1]
            top = margins[0]
            right = img.width - margins[3]
            bottom = img.height - margins[2]

            # Ensure the crop coordinates are valid
            if right <= left or bottom <= top:
                skipped_files += 1
                continue

            cropped_image = img.crop((left, top, right, bottom))
            cropped_image.save(os.path.join(target_folder, filename))
            processed_files += 1
    messagebox.showinfo("Cropping Complete",
                        f"Processed {processed_files} images. Skipped {skipped_files} files due to invalid crop "
                        f"dimensions.")


root = tk.Tk()
root.geometry("300x200+100+100")
root.title("Bulk Image Cropper")

frame = tk.Frame(root)
frame.pack(pady=20)

lbl = tk.Label(frame, text="Enter the margins to crop (top, left, bottom, right):")
lbl.pack()

entry = tk.Entry(frame)
entry.pack()

lbl = tk.Label(root, text="After clicking button folder selection will appear:\n1. Select source directory\n2. Select "
                          "target directory (preferably empty)", anchor='w', justify='left')
lbl.pack()

btn = tk.Button(frame, text="Select Folders and Crop Images", command=crop_images)
btn.pack(pady=10)

root.mainloop()
