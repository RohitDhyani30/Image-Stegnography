# Image Steganography System

A Python-based Image Steganography System that hides secret text messages inside images using the Least Significant Bit (LSB) technique.

## Features

- Encode secret messages into images
- Decode hidden messages from encoded images
- GUI file picker using Tkinter
- Supports PNG, JPG, JPEG, BMP, and GIF input images
- Saves encoded images in PNG format
- Error handling for invalid files and oversized messages

---

## Technologies Used

- Python
- NumPy
- Pillow (PIL)
- Tkinter

---

## Project Structure

```bash
project/
│
├── main.py
├── README.md
└── encoded_images/
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/image-steganography-system.git
cd image-steganography-system
```

---

## Install Dependencies

```bash
pip install pillow numpy
```

Tkinter usually comes pre-installed with Python.

---

## How It Works

The project uses the **Least Significant Bit (LSB)** steganography technique.

- Every pixel in an image contains RGB values.
- The least significant bit of each pixel is modified to store binary data.
- The hidden message is converted into binary format before embedding.
- A delimiter (`$$END$$`) is added to identify the end of the hidden message.

---

## Usage

Run the program:

```bash
python main.py
```

You will see:

```text
1. Encode a message
2. Decode a message
3. Exit
```

---

# Encoding Process

1. Select an input image
2. Enter secret message
3. Choose output location
4. Encoded image will be generated

---

# Decoding Process

1. Select encoded image
2. Hidden message will be extracted automatically

---

## Supported Formats

### Input Images
- PNG
- JPG
- JPEG
- BMP
- GIF

### Output Image
- PNG

---

## Example

### Original Message
```text
Hello World
```

### Encoded Image
```text
encoded_image.png
```

### Decoded Output
```text
Hello World
```

---

## Security Note

This project is designed for educational purposes and basic data hiding.  
It does not provide strong encryption or advanced security.

---

## Future Improvements

- Add AES encryption before encoding
- GUI-based full application
- Video steganography
- Audio steganography
- Password-protected decoding
- Drag-and-drop interface

---

## Author

Developed using Python and LSB Image Steganography concepts.

---
