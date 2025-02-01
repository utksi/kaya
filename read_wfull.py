import struct
import sys

def read_wfull_tmp(filename):
    """
    Minimal Python script to read and parse only Record 1 of WFULLXXXX.tmp.
    """
    try:
        with open(filename, 'rb') as f:
            # Record 1: RDUM, RISPIN, RTAG (3 Integers) - minimal parsing
            format_rec1 = ">3i"  # Try unpacking as 3 integers (4 bytes each)
            record1_bytes = f.read(12) # Read 12 bytes for Record 1
            reclw, rispin, rtag = struct.unpack(format_rec1, record1_bytes)
            print(f"Record 1: Record Length: {reclw}, Spin Polarization: {rispin}, Format Tag: {rtag}")


        print(f"Successfully read header record 1 (minimal parsing) from {filename}")

    except FileNotFoundError:
        print(f"Error: File not found: {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python read_wfull.py <WFULLXXXX.tmp_filename>")
        sys.exit(1)

    filename = sys.argv[1]
    read_wfull_tmp(filename)
