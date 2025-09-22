# stego_lsb_readable.py
import sys
import struct

# Helpers for 32-bit little-endian values
def read_u32(buf): 
    return struct.unpack("<I", buf)[0]

def write_u32(num): 
    return struct.pack("<I", num)

def embed_message(input_bmp, output_bmp, message):
    # Read BMP into a bytearray (mutable)
    data = bytearray(open(input_bmp, "rb").read())

    # Verify BMP header
    if data[:2] != b"BM":
        raise ValueError("Not a BMP file")

    # Get pixel data offset and bits-per-pixel
    pixel_start = read_u32(data[10:14])
    bpp = struct.unpack("<H", data[28:30])[0]
    if bpp != 24:
        raise ValueError("Only 24-bit BMP images are supported")

    # Prepare payload: [length (4 bytes)] + [UTF-8 message]
    encoded = message.encode("utf-8")
    payload = write_u32(len(encoded)) + encoded

    # Make sure the image has enough pixels
    if len(payload) * 8 > len(data) - pixel_start:
        raise ValueError("Message too large for this image")

    # Hide bits of the payload in the LSB of pixels
    pixel_data = data[pixel_start:]
    bit_index = 0
    for byte in payload:
        for bit in range(8):
            bit_value = (byte >> bit) & 1
            pixel_data[bit_index] = (pixel_data[bit_index] & 0xFE) | bit_value
            bit_index += 1

    # Save modified image
    data[pixel_start:] = pixel_data
    with open(output_bmp, "wb") as f:
        f.write(data)

def extract_message(stego_bmp):
    data = open(stego_bmp, "rb").read()

    # Verify BMP header
    if data[:2] != b"BM":
        raise ValueError("Not a BMP file")

    # Get pixel data offset and bits-per-pixel
    pixel_start = read_u32(data[10:14])
    bpp = struct.unpack("<H", data[28:30])[0]
    if bpp != 24:
        raise ValueError("Only 24-bit BMP images are supported")

    pixel_data = data[pixel_start:]

    # Helper: read N bytes from LSBs starting at bit_ptr
    def read_from_lsb(n_bytes, bit_ptr=0):
        out = bytearray()
        for _ in range(n_bytes):
            value = 0
            for bit in range(8):
                value |= (pixel_data[bit_ptr] & 1) << bit
                bit_ptr += 1
            out.append(value)
        return bytes(out), bit_ptr

    # First 4 bytes = length
    length_bytes, bit_pos = read_from_lsb(4)
    msg_len = read_u32(length_bytes)

    # Next N bytes = message
    msg_bytes, _ = read_from_lsb(msg_len, bit_pos)
    return msg_bytes.decode("utf-8", errors="replace")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  Embed:   python stego_lsb_readable.py embed in.bmp out.bmp \"message\"")
        print("  Extract: python stego_lsb_readable.py extract stego.bmp")
        sys.exit(1)

    mode = sys.argv[1].lower()
    if mode == "embed":
        _, _, in_file, out_file, msg = sys.argv
        embed_message(in_file, out_file, msg)
        print("Message embedded successfully.")
    elif mode == "extract":
        print(extract_message(sys.argv[2]))
    else:
        print("Unknown mode. Use 'embed' or 'extract'.")
