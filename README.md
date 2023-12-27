# PDF Encryptor App

## Overview
This is a simple PDF Encryptor application built using Tkinter for the GUI and pypdf for PDF handling. It allows you to encrypt multiple PDF files in a selected folder using a specified password.

## Features
- Select a folder containing PDF files for encryption.
- Preview PDF files in the selected folder.
- Enter a password or generate a random password.
- Optionally show/hide the entered password.
- Encrypt PDFs and save them in a new folder.

## Prerequisites
- Python 3.x
- Tkinter (usually included in Python installations)
- pypdf library (install using `pip install pypdf`)

## How to Run
1. Clone the repository.
2. Install the required dependencies: `pip install pypdf`.
3. Run the application: `python your_script_name.py`.

## Usage
1. Click on the "Select Folder" button to choose a folder containing PDF files.
2. The PDF files in the selected folder will be displayed in the preview area.
3. Enter a password in the "Enter Password" field or generate a random password using the "Generate Password" button.
4. Optionally, check the "Show Password" checkbox to reveal the entered password.
5. Click the "Encrypt PDFs" button to start the encryption process.
6. Encrypted PDFs will be saved in a new folder named "protected" within the selected folder.

## Limitations
- The PDF encryption process might take some time, depending on the number and size of the PDF files.
