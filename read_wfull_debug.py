import sys

def read_wfull_tmp(filename):
    """
    Reads a WFULLXXXX.tmp file and prints Record 2 bytes as hex - DEBUGGING SCRIPT.
    """
    try:
        with open(filename, 'rb') as f:
            # Skip Record 1 (24 bytes)
            f.seek(24) 

            # Read Record 2 (104 bytes) as hex
            raw_bytes = f.read(104)
            hex_representation = raw_bytes.hex()
            print(f"Record 2 (Hex): {hex_representation}")

        print(f"Successfully read Record 2 (hex) from {filename}")

    except FileNotFoundError:
        print(f"Error: File not found: {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python read_wfull_debug.py <WFULLXXXX.tmp_filename>")
        sys.exit(1)

    filename = sys.argv[1]
    read_wfull_tmp(filename)
