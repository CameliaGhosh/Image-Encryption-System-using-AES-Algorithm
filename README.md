# Image-Encryption-System-using-AES-Algorithm

## Overview

This project implements a secure image encryption and decryption system using the Advanced Encryption Standard (AES). The system ensures confidentiality of digital images by converting them into encrypted formats that are unreadable without the correct key.

## Objectives

* Implement AES-based image encryption and decryption
* Ensure secure image transmission over insecure networks
* Analyze encryption strength using statistical measures
* Develop a reliable and efficient security framework

## Technologies Used

* Python
* Flask (Web Interface)
* PyCryptodome (AES Encryption)
* NumPy
* Pillow (Image Processing)

## How It Works

1. Upload an image (JPG/PNG)
2. Image is converted into byte format
3. AES-128 encryption (CBC mode) is applied
4. Encrypted image is generated (random noise appearance)
5. Decryption reconstructs the original image using the same key

## AES Algorithm Details

* Key Size: 128-bit
* Mode: CBC (Cipher Block Chaining)
* Operations:

  * SubBytes
  * ShiftRows
  * MixColumns
  * AddRoundKey

## Security Analysis

The system evaluates encryption strength using:

* Entropy Analysis (ideal ≈ 8)
* Histogram Distribution (uniform after encryption)
* Pixel Correlation (reduced significantly)

## Features

* Secure image encryption & decryption
* Web-based interface using Flask
* High randomness in encrypted output
* Efficient processing time

## Project Structure

├── app.py
├── static/
│   ├── style.css
├── encrypted/
├── decrypted/
├── templates/
│   ├── index.html
│   ├── encrypt.html
│   ├── decrypt.html
│   └── result.html



## Note

This project is developed for academic purposes. Unauthorized use, modification, or distribution is not permitted.

## Authors

* Camelia Ghosh

## References

* NIST AES Standard
* IEEE Papers on Image Encryption
* Cryptography and Network Security by William Stallings
