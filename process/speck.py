import time
import qrcode

class SPECK:
    def __init__(self, key):
        """Initialize SPECK-128/64 with a 128-bit key (4 x 32-bit words)"""
        self.word_size = 32
        self.num_rounds = 27
        self.key_schedule(key)

    def key_schedule(self, key):
        """Generate 27 round keys from the initial 128-bit key"""
        l = [0] * (self.num_rounds - 1)
        k = [key[0]]

        # Generate round keys
        for i in range(self.num_rounds - 1):
            l[i] = ((key[i % 4] >> 8) | (key[i % 4] << (self.word_size - 8))) & 0xFFFFFFFF
            l[i] = (l[i] + k[i]) & 0xFFFFFFFF
            l[i] ^= i
            k.append((k[i] << 3) ^ l[i])

        self.round_keys = k

    def encrypt(self, plaintext):
        """Encrypts a 64-bit plaintext block using SPECK"""
        x, y = plaintext & 0xFFFFFFFF, (plaintext >> 32) & 0xFFFFFFFF

        for k in self.round_keys:
            x = ((x >> 8) | (x << (self.word_size - 8))) & 0xFFFFFFFF
            x = (x + y) & 0xFFFFFFFF
            x ^= k
            y = ((y << 3) | (y >> (self.word_size - 3))) & 0xFFFFFFFF
            y ^= x

        return (y << 32) | x
    
    def decrypt(self, ciphertext):
        """Decrypts a 64-bit ciphertext block using SPECK"""
        x, y = ciphertext & 0xFFFFFFFF, (ciphertext >> 32) & 0xFFFFFFFF

        for k in reversed(self.round_keys):
            y ^= x
            y = ((y >> 3) | (y << (self.word_size - 3))) & 0xFFFFFFFF  # Rotate back
            x ^= k
            x = (x - y) & 0xFFFFFFFF
            x = ((x << 8) | (x >> (self.word_size - 8))) & 0xFFFFFFFF  # Rotate left

        return (y << 32) | x

def generate_vid(mid, key):
    """Generate a Virtual Merchant ID (VID) by encrypting MID + Timestamp"""
    timestamp = str(int(time.time()))  # Get current timestamp
    data = mid + timestamp  # Combine MID and timestamp
    plaintext = int.from_bytes(data.encode(), 'big')  # Convert to integer

    speck = SPECK(key)  # Initialize SPECK
    encrypted_vid = speck.encrypt(plaintext)
    return hex(encrypted_vid)  # Convert to hex format

def generate_qr(encrypted_vid, filename="vid_qr.png"):
    """Generate a QR Code containing the encrypted VID"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(encrypted_vid)  # Store encrypted VID inside QR
    qr.make(fit=True)
    
    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)
    print(f"QR Code generated and saved as {filename}")

def decrypt_vid(encrypted_vid, key):
    """Decrypt the Virtual Merchant ID (VID) using SPECK"""
    speck = SPECK(key)  # Initialize SPECK
    decrypted = speck.decrypt(int(encrypted_vid, 16))  # Convert hex to integer

    # Ensure correct byte size
    byte_length = (decrypted.bit_length() + 7) // 8  
    byte_length = max(byte_length, 16)  # Ensure at least 16 bytes

    decrypted_bytes = decrypted.to_bytes(byte_length, 'big')  # Convert integer to bytes

    try:
        decrypted_text = decrypted_bytes.decode('utf-8').rstrip('\x00')  # Remove padding
        if "MID" not in decrypted_text:  # Check if MID is correctly recovered
            print("ERROR: Decryption output does not contain MID, something went wrong!")
            return None
        return decrypted_text
    except UnicodeDecodeError:
        print("ERROR: Decryption failed due to invalid byte conversion!")
        return None

# Example Usage
key = [0x1A2B3C4D, 0x3C4D5E6F, 0x7A8B9C0D, 0xE1F2A3B4]  # 128-bit key (4 x 32-bit words)
mid = "MID123456789"

vid = generate_vid(mid, key)
print(f"Encrypted VID: {vid}")
generate_qr(vid, "vid_qr.png")

# Decrypting the VID
encrypted_vid = vid
decrypted_mid = decrypt_vid(encrypted_vid, key)
if decrypted_mid:
    print(f"Decrypted MID: {decrypted_mid}")
else:
    print("Decryption Failed!")
