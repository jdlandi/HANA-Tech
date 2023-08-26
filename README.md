# HANA-Tech: Intelligent File Naming with AI

Welcome to the HANA-Tech project! This innovative tool employs the power of AI to intelligently name and organize your PDF files, promoting both productivity and efficiency.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup & Usage](#setup--usage)
- [Technical Overview](#technical-overivew)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [Author](#author)

## Overview

HANA-Tech is a solution designed to address the challenges of organizing and naming files with context and precision. The project utilizes Google Cloud Vision to extract content from PDFs, enhancing the naming process to be both contextual and intuitive.

## Features

1. **File Conversion**: Convert non-PDF files into the required PDF format.
2. **Setup Test**: Verify the project's setup and configuration.
3. **OCR Processing**: Extract textual content from PDF files using Google Cloud Vision.
4. **AI-powered Renaming**: Suggest and apply more descriptive filenames based on the content of your PDFs.
5. **Directory Cleanup**: Maintain a clutter-free workspace by deleting temporary text files.

## Prerequisites

Before diving into HANA-Tech, you'll need to set up a few components:

- **Google Cloud Account**: If you haven't registered yet, [sign up here](https://cloud.google.com/).
- **Google Cloud Vision API**: With your Google Cloud Account, [start with the Cloud Vision API](https://cloud.google.com/vision/docs/getting-started).
- **Google Cloud Storage Bucket**: [Create a storage bucket](https://cloud.google.com/storage/docs/creating-buckets) to store your files.
- **Open AI API**: [Create an account](https://openai.com/blog/openai-api) to access the AI model features used in this program. 

## Setup & Usage

### Configuration

Update the `CONFIG.JSON` with your Google Cloud credentials and other required details. Here's a sample configuration:

```json
{
  "OPENAI_KEY" :  "sk-realapikeyhere",
  "OPENAI_ORG" : "org-optional",
  "AI_MODEL": "gpt-4",
  "GCLOUD_WORKER_FILE" :"./work-account.json",
  "GCLOUD_BUCKET" : "hana-storage"
}
```

### Step-by-Step Walkthrough

1. **File Conversion**:
    - Deposit any non-PDF files in the `0. Utilities` directory.
    - Initiate the appropriate conversion script from the `0. Utilities` directory. This action will replace the original file with its PDF version.
    - Relocate the transformed PDFs to the primary project directory.

2. **Test Your Setup**:
    - Run `0.ai_test.py` to confirm the proper configuration.

3. **Run OCR**:
    - Launch `1.run_ocr.py` to process each PDF file, extract text via the Google Cloud Vision API, and save the result as a `.txt` file.

4. **Rename Files**:
    - Initiate `2.ai_file_rename.py`. The script will suggest descriptive filenames for each PDF based on its content. Validate or adjust the suggested names as necessary.

5. **Clean Up**:
    - After renaming and transferring your PDF files to their preferred location, execute `3.directory_cleanup.py` to erase all `.txt` files, ensuring a tidy workspace.

## Technical Overview

HANA-Tech capitalizes on the Google Cloud Vision API for its Optical Character Recognition (OCR) prowess. The project's structure guarantees that every phase, from file conversion to renaming, is modular and straightforward. The `CONFIG.JSON` is vital, serving as the hub for the user's Google Cloud configuration.

## File Structure

- **`0. Utilities`**: Houses utility scripts, predominantly for file conversion.
- **`0.ai_test.py`**: Script to test the project's setup.
- **`1.run_ocr.py`**: Manages OCR processing of PDFs.
- **`2.ai_file_rename.py`**: Overviews the AI-driven file renaming process.
- **`3.directory_cleanup.py`**: Cleans the directory after processing.
- **`CONFIG.JSON`**: Central configuration file.

## Contributing

Although HANA-Tech was crafted for specific needs, collaboration is paramount. If this project resonates with you and you wish to suggest improvements, share feedback, or contribute directly, please don't hesitate to open an issue or submit a pull request.

## Author

[Jay Landi](https://www.linkedin.com/in/jdlandi/) | California Institute of Technology

---

Cheers to a more organized and productive workspace!
