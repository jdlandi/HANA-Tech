import os
from pillow_heif import register_heif_opener
from PIL import Image

# use the directory you're running the script from
directory = os.getcwd()

# list all the image extensions that PIL supports
img_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".ppm", ".tiff", ".heic"]

# register heif opener
register_heif_opener()

def list_pdf():
    pdf_filenames = [f for f in os.listdir(directory) if f.endswith(".pdf")]
    return ', '.join(pdf_filenames)

def convert_image_to_pdf(filename):
    img = Image.open(filename)

    # if image is not in RGB mode convert it
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # save the image as a pdf
    pdf_filename = os.path.splitext(filename)[0] + '.pdf'
    img.save(pdf_filename, "PDF")

    # close the image file
    img.close()

    # remove the original file
    os.remove(filename)

# iterate over all files in the directory
for filename in os.listdir(directory):
    full_filename = os.path.join(directory, filename)
    # check if the file is an image
    if any(filename.endswith(ext) for ext in img_extensions):
        convert_image_to_pdf(full_filename)
print(list_pdf())
