import os
from PIL import Image

# Get a list of all the files in the current folder
files = os.listdir()

# Filter the list to only include image files
image_files = [f for f in files if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.jpeg')]

# Loop through the image files and convert each one to a PDF
for image_file in image_files:
    # Open the image file using PIL
    image = Image.open(image_file)

    # Create a PDF filename by replacing the file extension with .pdf
    pdf_file = os.path.splitext(image_file)[0] + '.pdf'

    # Save the PDF file
    image.save(pdf_file, 'PDF', resolution=100.0)

    # Print a message to show that the conversion was successful
    print(f'Converted {image_file} to {pdf_file}')
