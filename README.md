# Kaya

Tools for analyzing frequency-dependent screening in VASP calculations, particularly focused on Auger recombination in perovskite materials.

## Features

- Read and parse VASP WFULL files containing screened Coulomb interaction data
- Extract frequency-dependent W(G,G',q,ω)
- Calculate Auger recombination matrix elements
- Support for halide perovskite materials

## Installation

```bash
git clone https://github.com/yourusername/kaya.git
cd kaya
```

## Usage

### Reading WFULL Files
```bash
python read_wfull_data.py /path/to/wfull/directory
```

This will:
1. Read all WFULLXXXX.tmp files in the directory
2. Create human-readable text files in a 'readable' subdirectory
3. Extract frequency information and matrix elements

## Documentation

- [WFULL File Format](docs/WFULL_format.md)
- [Auger Calculation Strategy](docs/auger_calculation_strategy.md)

## Project Structure

```
kaya/
├── docs/                    # Documentation
│   ├── WFULL_format.md     # WFULL file format description
│   └── auger_calculation_strategy.md  # Calculation methodology
├── read_wfull_data.py      # Main script for reading WFULL files
├── read_wfull.py           # Alternative reader implementation
└── read_wfull_debug.py     # Debugging utilities
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## WFULL File Format and Parsing Algorithm

The project includes tools to parse VASP's WFULL output files (e.g., `WFULLxxxx.tmp`), which contain the frequency-dependent screened Coulomb interaction data essential for GW calculations and for applications such as calculating Auger recombination rates. This section details the file structure, the physical meaning of its components, the related equations, and the algorithm used to read and process these files.

### 1. File Structure

Each `WFULLxxxx.tmp` file is generated in Fortran unformatted sequential I/O format and comprises the following major components:

1. **Header Block (18 values):**
   - **Description:** A 1D array of 18 floating-point numbers read from the first Fortran record in the file.
   - **Physical Meaning:**  
     - **First Value (h₁):** Typically used as a frequency indicator. In many cases, this value represents the frequency point (ω) at which the screened Coulomb interaction is evaluated. In our equations, it indicates the specific point where the dielectric response \( \varepsilon^{-1}(G, G', \omega) \) is computed.
     - **Remaining Values (h₂ to h₁₈):** They encode essential scaling and calibration parameters. Although the precise meaning may vary with the VASP version, these values commonly include:
       - Scale factors applied to the wing parts,
       - Contributions related to the normalization of the dielectric response,
       - Other metadata that help in reconstructing the full response matrix from the raw data.
     - **Usage in Equations:** In the relation
       \[
       W(G, G', \omega) = \varepsilon^{-1}(G, G', \omega)\, v(|G-G'|),
       \]
       the header provides the necessary calibration so that when the matrices (WING, CWING, and Response) are combined, they yield a correctly scaled \( \varepsilon^{-1} \) and hence \( W \).

2. **Matrix Data Blocks:**

   The file contains three main matrices that together represent the screened Coulomb interaction:
   
   - **WING Matrix:**
     - **Shape:** \((\text{ngvector},\, 3)\).
     - **Physical Role:** Contains the so-called "wing" contributions. These represent off-diagonal corrections corresponding to interactions involving a selected subset of reciprocal lattice vectors (G-vectors). In the equation, their role is to supply specific corrections or modifications to the bare Coulomb potential such that when combined with the dielectric response, it correctly captures spatial inhomogeneities.
     - **Data Connection:** When you later reconstruct \( W(G, G', \omega) \), elements from the WING matrix (adjusted by appropriate header values) contribute to the off-diagonal parts of the dielectric matrix.
   
   - **CWing Matrix:**
     - **Shape:** \((\text{ngvector},\, 3)\).
     - **Physical Role:** Often viewed as complementary to the WING matrix, the CWing matrix may represent the complex-conjugate or correction terms that ensure the overall matrix exhibits proper Hermitian (or symmetric) behavior. They are used alongside the WING matrix to refine the screening potential.
     - **Data Connection:** In the screening equation, combining CWing with WING completes the corrections needed to accurately model the off-diagonal screening components.
   
   - **Response Matrix:**
     - **Shape:** A square matrix of size \((\text{ngvector} \times \text{ngvector})\).
     - **Physical Role:** This is the core of the dielectric response data. It effectively represents the inverse dielectric function \( \varepsilon^{-1}(G, G', \omega) \). Under the relationship
       \[
       W(G,G',\omega) = \varepsilon^{-1}(G,G',\omega)\, v(|G-G'|),
       \]
       this matrix, when multiplied with the bare Coulomb potential \( v \), yields the screened interaction.
     - **Data Connection:** The response matrix is built from the computed polarization properties of the system. Its structure directly links to how spatial inhomogeneities and dynamic screening occur in the material, and its elements are scaled according to the header metadata.

3. **Dimensions and Metadata:**
   - Additional information, such as the number of G-vectors (`ngvector`), is included (often derived from the header or associated blocks) so that the script knows how many elements to expect in each matrix.

### 2. Physical Meaning and Equations

#### Screened Coulomb Interaction

The screened Coulomb interaction \( W \) expresses how the material's dielectric properties reduce the bare Coulomb potential \( v \). In real space:
\[
W(r, r', \omega) = \int dr''\, \varepsilon^{-1}(r, r'', \omega)\, v(r'', r').
\]
In reciprocal space, this transforms into:
\[
W(G, G', \omega) = \varepsilon^{-1}(G, G', \omega)\, v(|G-G'|).
\]
Here, the header values calibrate \( \varepsilon^{-1}(G,G',\omega) \) by applying necessary normalization and scaling factors, while the combination of the WING, CWing, and Response matrices reconstructs the full dielectric function.

#### Auger Recombination

For Auger recombination processes, the matrix element for a transition involving wavefunctions \( \psi_1, \psi_2, \psi_3, \psi_4 \) is given by:
\[
M_{\text{Auger}} = \int dr\, dr'\, \psi_1^*(r)\, \psi_2^*(r')\, W(r,r',\Delta E)\, \psi_3(r)\, \psi_4(r').
\]
Here, \(\Delta E\) represents the energy transfer, typically approximated by the bandgap in direct Auger transitions. The detailed construction of \( W(r,r',\Delta E) \) from its reciprocal space components involves the matrices we read (scaled and combined as explained).

The corresponding Auger recombination rate is given by Fermi's Golden Rule:
\[
R_{\text{Auger}} = \frac{2\pi}{\hbar} \sum_{k_1,k_2,k_3,k_4} \left| M_{\text{Auger}} \right|^2 \delta(E_1+E_2-E_3-E_4).
\]

#### Energy Transfer \(\Delta E\)

\(\Delta E\) approximates the difference in energy between involved states (for instance, between conduction and valence band states):
\[
\Delta E \approx E_{\text{conduction}} - E_{\text{valence}}.
\]

### 3. Parsing Algorithm

Our Python script (`read_wfull_data.py`) follows these steps to convert the binary WFULL files into a human-readable format:

1. **Fortran Record Parsing:**
   - **Record Markers:** Each block is wrapped in 4-byte integers indicating the size of the record. The function `read_fortran_record(f, dtype)` reads a record, checks that the beginning and ending sizes match, and then converts the binary data into a NumPy array.
   
2. **Header Processing:**
   - **Extraction:** The script reads the first 18 floating-point values to form the header block. The first value is interpreted as the frequency indicator, while the remaining values provide calibration/scaling data.
   
3. **Determining Matrix Dimensions:**
   - **Dimensions:** The header (or associated metadata) provides the value for `ngvector` which determines the dimensions of the subsequent matrices.
   
4. **Reading Matrix Data:**
   - **WING and CWing Matrices:** The script reads two complex-valued matrices of shape `(ngvector, 3)`. These matrices hold the specific contributions required to account for off-diagonal screening effects as described in our equations.
   - **Response Matrix:** A large square complex matrix of size \((ngvector \times ngvector)\) is read next, which represents the primary dielectric response needed to compute \(W(G,G',\omega)\).
   
5. **Output Generation:**
   - The function `write_human_readable(data, output_file)` formats and writes the parsed data into a text file. It includes:
     - A summary of header values (displaying the frequency indicator and key scaling parameters)
     - Dimension information, such as the number of G-vectors
     - Sample data from the matrices (e.g., a 5×3 block of the WING matrix with both real and imaginary parts) for confirmation and debugging purposes.

This detailed parsing process not only converts the raw binary data into a format amenable to inspection and further analysis but also ensures that the physical content underlying the screened Coulomb interaction is correctly interpreted and scaled according to the VASP-calculated parameters.
