from PIL import Image
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from pathlib import Path

class SteganographySystem:
    def __init__(self):
        self.delimiter = "$$END$$"
    
    def text_to_binary(self, text):
        """Convert text to binary representation"""
        binary = ''.join(format(ord(char), '08b') for char in text)
        return binary
    
    def binary_to_text(self, binary):
        """Convert binary back to text"""
        text = ''
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            text += chr(int(byte, 2))
        return text
    
    def can_encode(self, image, message):
        """Check if the message can fit in the image"""
        message = message + self.delimiter
        required_pixels = len(message) * 8
        width, height = image.size
        available_pixels = width * height * 3
        return required_pixels <= available_pixels
    
    def encode(self, image_path, message, output_path):
        """Hide a message in an image using LSB steganography"""
        try:
            # Verify input image exists
            if not os.path.exists(image_path):
                raise FileNotFoundError("Input image not found")
            
            # Ensure output directory exists
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                try:
                    os.makedirs(output_dir)
                except Exception as e:
                    raise Exception(f"Cannot create output directory: {str(e)}")
            
            # Check write permissions
            try:
                output_dir = output_dir if output_dir else '.'
                test_file = os.path.join(output_dir, 'test_write.tmp')
                with open(test_file, 'w') as f:
                    f.write('test')
                os.remove(test_file)
            except Exception:
                raise Exception("No write permission in the output directory")
            
            # Open and process the image
            img = Image.open(image_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            message += self.delimiter
            if not self.can_encode(img, message):
                raise ValueError("Message too large for this image")
            
            binary_message = self.text_to_binary(message)
            data = np.array(img, dtype=np.uint8)
            height, width, channels = data.shape
            
            binary_array = np.array([int(bit) for bit in binary_message], dtype=np.uint8)
            if len(binary_array) % 8 != 0:
                padding = 8 - (len(binary_array) % 8)
                binary_array = np.pad(binary_array, (0, padding), 'constant')
            
            max_bits = min(len(binary_array), height * width * channels)
            flat_data = data.ravel()
            flat_data[:max_bits] &= 254
            flat_data[:max_bits] |= binary_array[:max_bits]
            modified_data = flat_data.reshape(data.shape)
            
            # Save the image with proper error handling
            encoded_img = Image.fromarray(modified_data)
            try:
                encoded_img.save(output_path, 'PNG')
            except Exception as e:
                raise Exception(f"Failed to save image: {str(e)}")
            
            return True
            
        except Exception as e:
            raise Exception(f"Encoding error: {str(e)}")
    
    def decode(self, image_path):
        """Extract hidden message from an image"""
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError("Image file not found")
            
            img = Image.open(image_path)
            data = np.array(img)
            binary_message = ''
            flat_data = data.ravel()
            
            for pixel in flat_data:
                binary_message += str(pixel & 1)
                if len(binary_message) % 8 == 0:
                    text_chunk = self.binary_to_text(binary_message[-8:])
                    if binary_message[-8*len(self.delimiter):] == self.text_to_binary(self.delimiter):
                        return self.binary_to_text(binary_message[:-8*len(self.delimiter)])
            
            raise ValueError("No hidden message found")
            
        except Exception as e:
            raise Exception(f"Decoding error: {str(e)}")

def main():
    # Create and keep a reference to the root window
    root = tk.Tk()
    root.withdraw()  # Hide the main window but keep it active
    
    while True:
        choice = input("\nChoose an option:\n1. Encode a message\n2. Decode a message\n3. Exit\n> ")
        
        if choice == '3':
            break
            
        if choice == '1':
            # Force the dialog to stay on top
            root.lift()
            root.attributes('-topmost', True)
            
            print("\nSelect the input image file...")
            image_path = filedialog.askopenfilename(
                parent=root,
                title="Select Input Image",
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
            )
            
            if not image_path:
                print("No file selected. Try again.")
                continue
            
            message = input("Enter the message to encode: ")
            
            # Get default directory from input image
            default_dir = os.path.dirname(image_path)
            default_name = "encoded_image.png"
            default_path = os.path.join(default_dir, default_name)
            
            print("\nSelect where to save the encoded image...")
            output_path = filedialog.asksaveasfilename(
                parent=root,
                title="Save Encoded Image As",
                defaultextension=".png",
                initialdir=default_dir,
                initialfile=default_name,
                filetypes=[("PNG files", "*.png")]
            )
            
            if not output_path:
                print("No output location selected. Try again.")
                continue
            
            try:
                stego = SteganographySystem()
                success = stego.encode(image_path, message, output_path)
                if success:
                    print(f"\nSuccess! Message encoded into '{output_path}'")
            except Exception as e:
                print(f"\nError: {str(e)}")
        
        elif choice == '2':
            # Force the dialog to stay on top
            root.lift()
            root.attributes('-topmost', True)
            
            print("\nSelect the encoded image file...")
            image_path = filedialog.askopenfilename(
                parent=root,
                title="Select Encoded Image",
                filetypes=[("PNG files", "*.png")]
            )
            
            if not image_path:
                print("No file selected. Try again.")
                continue
            
            try:
                stego = SteganographySystem()
                message = stego.decode(image_path)
                print(f"\nDecoded message: {message}")
            except Exception as e:
                print(f"\nError: {str(e)}")
        else:
            print("\nInvalid choice. Please try again.")
    
    # Destroy the root window when done
    root.destroy()

if __name__ == "__main__":
    main()