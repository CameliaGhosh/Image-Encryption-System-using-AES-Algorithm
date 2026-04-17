from flask import Flask, render_template, request, send_from_directory
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os
import time
import math
import numpy as np
import matplotlib
# This line is SUPER important for Flask so matplotlib doesn't try to open a GUI window
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
app = Flask(__name__)
os.makedirs("encrypted", exist_ok=True)
os.makedirs("decrypted", exist_ok=True)
os.makedirs("static", exist_ok=True) # Ensure static folder exists for the histogram
# --- Padding Functions ---
def pad(data):
    pad_len = 16 - len(data) % 16
    return data + bytes([pad_len] * pad_len)
def unpad(data):
    return data[:-data[-1]]
# --- Security Analysis Functions ---
def calculate_entropy(data):
    if not data: return 0
    entropy = 0
    for x in range(256):
        p_x = data.count(x) / len(data)
        if p_x > 0:
            entropy += - p_x * math.log2(p_x)
    return round(entropy, 4)
def calculate_correlation(data):
    # Calculate correlation between adjacent bytes
    bytes_arr = np.frombuffer(data, dtype=np.uint8)
    x = bytes_arr[:-1]
    y = bytes_arr[1:]
    # Avoid division by zero if the data is entirely flat (which shouldn't happen in AES)
    if len(x) == 0 or np.std(x) == 0 or np.std(y) == 0:
        return 0     
    correlation_matrix = np.corrcoef(x, y)
    return round(correlation_matrix[0, 1], 4)
def generate_histogram(data, filename):
    plt.figure(figsize=(5, 3))
    plt.hist(list(data), bins=256, range=(0, 256), color='#ff7eb3', alpha=0.8)
    plt.title('Encrypted Data Histogram', fontsize=10)
    plt.xlabel('Byte Value (0-255)', fontsize=8)
    plt.ylabel('Frequency', fontsize=8)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
# --- Home Route ---
@app.route('/')
def home():
    return render_template('index.html')
# --- Encrypt Route ---
@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    if request.method == 'POST':
        file = request.files['image']
        data = file.read()
        padded = pad(data)
        key = get_random_bytes(16)
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(padded)
        timestamp = int(time.time())
        enc_path = f"encrypted/encrypted_{timestamp}.bin"
        key_path = f"encrypted/key_{timestamp}.txt"
        hist_path = f"static/hist_{timestamp}.png" # Save to static so HTML can display it easily
        # Save files
        with open(enc_path, "wb") as f:
            f.write(encrypted)
        with open(key_path, "wb") as f:
            f.write(key + iv)
        # Perform Analysis
        entropy_val = calculate_entropy(encrypted)
        correlation_val = calculate_correlation(encrypted)
        generate_histogram(encrypted, hist_path)
        return render_template(
            "result.html",   # ✅ THIS WAS MISSING
            message="✨ Encryption & Analysis Successful!",
            file=enc_path,
            key=key_path,
            entropy=entropy_val,
            correlation=correlation_val,
            histogram=hist_path
        )
    return render_template('encrypt.html')
@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    if request.method == 'POST':
        file = request.files['image']
        key_file = request.files['key']

        encrypted_data = file.read()
        key_iv = key_file.read()

        key = key_iv[:16]
        iv = key_iv[16:]

        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(encrypted_data)
        decrypted = unpad(decrypted)

        dec_path = "decrypted/decrypted.png"
        with open(dec_path, "wb") as f:
            f.write(decrypted)

        return render_template(
            "result.html",
            message="🌸 Decryption Successful!",
            file=dec_path,
            is_image=True
        )

    return render_template('decrypt.html')
@app.route('/decrypted/<filename>')
def serve_decrypted(filename):
    return send_from_directory('decrypted', filename)

@app.route('/encrypted/<filename>')
def serve_encrypted(filename):
    return send_from_directory('encrypted', filename)
if __name__ == '__main__':
    app.run(debug=True)
