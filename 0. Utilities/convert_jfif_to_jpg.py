import os
from PIL import Image

# Get the current folder path
folder_path = os.getcwd()

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    # Check if the file is a .jfif image
    if filename.endswith('.jfif'):
        # Create the full path for the input image file
        input_path = os.path.join(folder_path, filename)

        # Create the full path for the output .png file with the same filename
        output_path = os.path.join(folder_path, os.path.splitext(filename)[0] + '.png')

        # Open the .jfif image using PIL
        with Image.open(input_path) as img:
            # Save the image as .png
            img.save(output_path, 'PNG')

            # Print a message to show that the conversion was successful
            print(f'Converted {filename} to {os.path.basename(output_path)}')
