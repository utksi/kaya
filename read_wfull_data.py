#!/usr/bin/env python3

import numpy as np
import struct
import os
import sys
from pathlib import Path
import glob

def read_fortran_record_size(f):
    """Read a Fortran record size marker"""
    size_bytes = f.read(4)
    if not size_bytes:
        return None
    return int.from_bytes(size_bytes, byteorder='little')

def read_fortran_record(f, dtype=None):
    """Read a full Fortran record with proper size checking
    
    Args:
        f: File object
        dtype: numpy dtype to interpret the data (if None, just read bytes)
        
    Returns:
        Data read from the record, or None if end of file
    """
    size_start = read_fortran_record_size(f)
    if size_start is None:
        return None
        
    data = f.read(size_start)
    size_end = read_fortran_record_size(f)
    
    if size_start != size_end:
        raise ValueError(f"Fortran record size mismatch: {size_start} != {size_end}")
        
    if dtype is not None:
        return np.frombuffer(data, dtype=dtype)
    return data

def read_wfull_file(filename):
    """
    Read a WFULLXXXX.tmp file containing screened Coulomb interaction data.
    The file contains W(G,G',q) for one k-point at one frequency point.
    Multiple files are needed to get the full W(G,G',q,ω):
    - Different k-points are in different WFULLxxxx.tmp files
    - Different frequencies require different VASP runs with different NOMEGA_DUMP values
    
    Args:
        filename (str): Path to the WFULLXXXX.tmp file
        
    Returns:
        dict: Dictionary containing the parsed data with structure:
            - dimensions: dict with ngvector
            - kpoint_index: Which k-point this file represents (from filename)
            - header: Metadata (18 values), header[0] might be the frequency point
            - wing: Wing matrix (frequency independent)
            - cwing: CWing matrix (frequency independent)
            - response: Full response function matrix W(G,G')
    """
    data = {}
    
    try:
        # Extract k-point index from filename (e.g. WFULL0001.tmp -> 1)
        kpoint_index = int(os.path.basename(filename)[5:9])
        data['kpoint_index'] = kpoint_index
        
        with open(filename, 'rb') as f:
            # First record contains dimensions
            dimensions = read_fortran_record(f, dtype=np.int32)
            if dimensions is None:
                raise ValueError("Could not read dimensions")
                
            ngvector = dimensions[0]
            ngvector2 = dimensions[1]
            
            print(f"File info: ngvector={ngvector}, ngvector2={ngvector2}")
            
            data['dimensions'] = {
                'ngvector': ngvector,
                'ngvector2': ngvector2,
            }
            
            # Read header block (18 doubles)
            header = read_fortran_record(f, dtype=np.float64)
            if header is None:
                raise ValueError("Could not read header")
            print(f"Read header block")
            
            # Read WING matrix (frequency independent)
            wing_data = read_fortran_record(f, dtype=np.complex128)
            if wing_data is None:
                raise ValueError("Could not read WING matrix")
            print(f"Read WING matrix")
            
            # Read CWING matrix (frequency independent)
            cwing_data = read_fortran_record(f, dtype=np.complex128)
            if cwing_data is None:
                raise ValueError("Could not read CWING matrix")
            print(f"Read CWING matrix")
            
            # Read response matrix (W(G,G') at this frequency point)
            response_data = read_fortran_record(f, dtype=np.complex128)
            if response_data is None:
                raise ValueError("Could not read response matrix")
            print(f"Read response matrix")
            
            # Reshape matrices
            try:
                # WING and CWING are frequency independent
                wing = wing_data.reshape((ngvector, 3), order='F')
                cwing = cwing_data.reshape((ngvector, 3), order='F')
                
                # Response matrix is W(G,G') at this frequency point
                response = response_data.reshape((ngvector, ngvector), order='F')
                
                data['header'] = header
                data['wing'] = wing
                data['cwing'] = cwing
                data['response'] = response
                
                # Try to interpret frequency information from header
                # The first value in header might be the frequency point
                data['possible_frequency'] = header[0]
                
            except ValueError as e:
                print(f"Warning: Could not reshape matrices: {e}")
                data['header'] = header
                data['wing'] = wing_data
                data['cwing'] = cwing_data
                data['response'] = response_data
                
    except Exception as e:
        print(f"Error reading file {filename}: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
        
    return data

def write_human_readable(data, output_file):
    """
    Write the parsed data to a human-readable text file
    
    Args:
        data (dict): Dictionary containing the parsed data
        output_file (str): Path to output file
    """
    with open(output_file, 'w') as f:
        # Write header information
        f.write("WFULL File Contents\n")
        f.write("=================\n\n")
        
        f.write("File Information:\n")
        f.write("----------------\n")
        f.write(f"K-point index: {data['kpoint_index']}\n")
        if 'possible_frequency' in data:
            f.write(f"Possible frequency point: {data['possible_frequency']:.6f}\n")
        f.write("\n")
        
        f.write("Dimensions:\n")
        f.write("-----------\n")
        for key, value in data['dimensions'].items():
            f.write(f"{key}: {value}\n")
        f.write("\n")
        
        # Write header data
        f.write("Header Block (18 values):\n")
        f.write("--------------------------\n")
        np.savetxt(f, data['header'].reshape(1, -1), fmt='%12.6f')
        f.write("\nPossible metadata from header:\n")
        f.write(f"First 8 values: {', '.join([f'{x:.6f}' for x in data['header'][:8]])}\n")
        f.write("\n")
        
        # Write data shape information
        f.write("Matrix Shapes:\n")
        f.write("--------------\n")
        f.write(f"WING matrix shape: {data['wing'].shape}\n")
        f.write(f"CWING matrix shape: {data['cwing'].shape}\n")
        f.write(f"Response matrix shape: {data['response'].shape}\n")
        f.write("\n")
        
        # Write a sample of the matrices
        f.write("WING Matrix (first 5x3 block):\n")
        f.write("-----------------------------\n")
        f.write("Real part:\n")
        np.savetxt(f, data['wing'][:5,:].real, fmt='%12.6e')
        f.write("\nImaginary part:\n")
        np.savetxt(f, data['wing'][:5,:].imag, fmt='%12.6e')
        f.write("\n")
        
        f.write("CWING Matrix (first 5x3 block):\n")
        f.write("------------------------------\n")
        f.write("Real part:\n")
        np.savetxt(f, data['cwing'][:5,:].real, fmt='%12.6e')
        f.write("\nImaginary part:\n")
        np.savetxt(f, data['cwing'][:5,:].imag, fmt='%12.6e')
        f.write("\n")
        
        f.write("Response Matrix (first 5x5 block):\n")
        f.write("--------------------------------\n")
        f.write("Real part:\n")
        np.savetxt(f, data['response'][:5,:5].real, fmt='%12.6e')
        f.write("\nImaginary part:\n")
        np.savetxt(f, data['response'][:5,:5].imag, fmt='%12.6e')
        f.write("\n")
        
        # Write statistics for each matrix
        for name, matrix in [('WING', data['wing']), ('CWING', data['cwing']), ('Response', data['response'])]:
            f.write(f"\n{name} Matrix Statistics:\n")
            f.write("-" * (len(name) + 18) + "\n")
            
            # Real part statistics
            real_finite = np.isfinite(matrix.real)
            if np.any(real_finite):
                f.write("Real part:\n")
                f.write(f"Mean value: {np.mean(matrix.real[real_finite]):.6e}\n")
                f.write(f"Standard deviation: {np.std(matrix.real[real_finite]):.6e}\n")
                f.write(f"Minimum value: {np.min(matrix.real[real_finite]):.6e}\n")
                f.write(f"Maximum value: {np.max(matrix.real[real_finite]):.6e}\n")
            else:
                f.write("No finite values found in the real part\n")
                
            # Imaginary part statistics
            imag_finite = np.isfinite(matrix.imag)
            if np.any(imag_finite):
                f.write("\nImaginary part:\n")
                f.write(f"Mean value: {np.mean(matrix.imag[imag_finite]):.6e}\n")
                f.write(f"Standard deviation: {np.std(matrix.imag[imag_finite]):.6e}\n")
                f.write(f"Minimum value: {np.min(matrix.imag[imag_finite]):.6e}\n")
                f.write(f"Maximum value: {np.max(matrix.imag[imag_finite]):.6e}\n")
            else:
                f.write("No finite values found in the imaginary part\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: python read_wfull_data.py <directory containing WFULLXXXX.tmp files>")
        sys.exit(1)
        
    wfull_dir = sys.argv[1]
    if not os.path.exists(wfull_dir):
        print(f"Error: Directory {wfull_dir} not found")
        sys.exit(1)
        
    # Find all WFULL files
    wfull_files = sorted(glob.glob(os.path.join(wfull_dir, "WFULL????.tmp")))
    if not wfull_files:
        print(f"Error: No WFULLXXXX.tmp files found in {wfull_dir}")
        sys.exit(1)
    
    print(f"Found {len(wfull_files)} WFULL files")
    
    # Create output directory
    output_dir = os.path.join(wfull_dir, "readable")
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each file
    for wfull_file in wfull_files:
        print(f"\nProcessing {wfull_file}...")
        data = read_wfull_file(wfull_file)
        if data is None:
            continue
            
        # Write human readable output
        output_file = os.path.join(output_dir, Path(wfull_file).stem + "_readable.txt")
        write_human_readable(data, output_file)
        print(f"Data written to {output_file}")

if __name__ == "__main__":
    main()
