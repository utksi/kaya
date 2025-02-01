# WFULL File Format Documentation

## Overview

The `WFULLxxxx.tmp` files contain the screened Coulomb interaction W(G,G',q,ω) calculated by VASP for GW calculations. Each file contains the data for:
- One q-point (specified by xxxx in filename)
- One frequency point ω (specified by NOMEGA_DUMP in INCAR)

## Binary Format (WFULLxxxx.tmp)

The file is written in Fortran unformatted binary format with the following structure:

1. **Dimensions** (2 integers):
   ```fortran
   WRITE(IU) NP, NP  ! NP = Number of G-vectors
   ```

2. **HEAD Matrix** (3×3 complex matrix = 18 real numbers):
   ```fortran
   WRITE(IU) WPOT%HEAD(:,:,NOMEGA)
   ```
   This represents W(G→0,G'→0,q,ω), the long-wavelength limit of the screened interaction:
   ```
   HEAD = [ε⁻¹₍ₓₓ₎(q,ω)  ε⁻¹₍ₓᵧ₎(q,ω)  ε⁻¹₍ₓᵧ₎(q,ω)]
         [ε⁻¹₍ᵧₓ₎(q,ω)  ε⁻¹₍ᵧᵧ₎(q,ω)  ε⁻¹₍ᵧᵣ₎(q,ω)]
         [ε⁻¹₍ᵣₓ₎(q,ω)  ε⁻¹₍ᵣᵧ₎(q,ω)  ε⁻¹₍ᵣᵣ₎(q,ω)]
   ```
   Where ε⁻¹ᵢⱼ is the inverse dielectric matrix in the long-wavelength limit.

3. **WING Matrix** (NP×3 complex matrix):
   ```fortran
   WRITE(IU) WPOT%WING(1:NP,:,NOMEGA)
   ```
   Represents W(G,G'→0,q,ω), coupling between finite G and G'→0:
   ```
   WING = [W(G₁,x,q,ω)  W(G₁,y,q,ω)  W(G₁,z,q,ω)]
         [W(G₂,x,q,ω)  W(G₂,y,q,ω)  W(G₂,z,q,ω)]
         [   ...          ...           ...      ]
         [W(Gₙ,x,q,ω)  W(Gₙ,y,q,ω)  W(Gₙ,z,q,ω)]
   ```

4. **CWING Matrix** (NP×3 complex matrix):
   ```fortran
   WRITE(IU) WPOT%CWING(1:NP,:,NOMEGA)
   ```
   The conjugate WING matrix: W(G→0,G',q,ω)
   ```
   CWING = [W(x,G₁,q,ω)  W(y,G₁,q,ω)  W(z,G₁,q,ω)]
          [W(x,G₂,q,ω)  W(y,G₂,q,ω)  W(z,G₂,q,ω)]
          [   ...          ...           ...      ]
          [W(x,Gₙ,q,ω)  W(y,Gₙ,q,ω)  W(z,Gₙ,q,ω)]
   ```

5. **Full Response Matrix** (NP×NP complex matrix):
   ```fortran
   WRITE(IU) W(1:NP,1:NP)
   ```
   The complete screened interaction W(G,G',q,ω) for all G-vectors:
   ```
   W = [W(G₁,G₁,q,ω)  W(G₁,G₂,q,ω)  ...  W(G₁,Gₙ,q,ω)]
      [W(G₂,G₁,q,ω)  W(G₂,G₂,q,ω)  ...  W(G₂,Gₙ,q,ω)]
      [    ...           ...        ...      ...      ]
      [W(Gₙ,G₁,q,ω)  W(Gₙ,G₂,q,ω)  ...  W(Gₙ,Gₙ,q,ω)]
   ```

## Readable Format (WFULL####_readable.txt)

The Python script converts the binary format into a human-readable text file with the following sections:

1. **File Information**:
   ```
   K-point index: xxxx
   Possible frequency point: ω (eV)
   ```

2. **Dimensions**:
   ```
   ngvector: NP    # Number of G-vectors
   ngvector2: NP   # Should be equal to ngvector
   ```

3. **HEAD Matrix** (18 values):
   ```
   Re[ε⁻¹₍ₓₓ₎]  Re[ε⁻¹₍ₓᵧ₎]  Re[ε⁻¹₍ₓᵣ₎]  Im[ε⁻¹₍ₓₓ₎]  Im[ε⁻¹₍ₓᵧ₎]  Im[ε⁻¹₍ₓᵣ₎]
   Re[ε⁻¹₍ᵧₓ₎]  Re[ε⁻¹₍ᵧᵧ₎]  Re[ε⁻¹₍ᵧᵣ₎]  Im[ε⁻¹₍ᵧₓ₎]  Im[ε⁻¹₍ᵧᵧ₎]  Im[ε⁻¹₍ᵧᵣ₎]
   Re[ε⁻¹₍ᵣₓ₎]  Re[ε⁻¹₍ᵣᵧ₎]  Re[ε⁻¹₍ᵣᵣ₎]  Im[ε⁻¹₍ᵣₓ₎]  Im[ε⁻¹₍ᵣᵧ₎]  Im[ε⁻¹₍ᵣᵣ₎]
   ```

4. **WING Matrix** (NP×3 complex numbers):
   ```
   Re[W(G₁,x)]  Re[W(G₁,y)]  Re[W(G₁,z)]  Im[W(G₁,x)]  Im[W(G₁,y)]  Im[W(G₁,z)]
   Re[W(G₂,x)]  Re[W(G₂,y)]  Re[W(G₂,z)]  Im[W(G₂,x)]  Im[W(G₂,y)]  Im[W(G₂,z)]
   ...
   ```

5. **CWING Matrix** (NP×3 complex numbers):
   ```
   Re[W(x,G₁)]  Re[W(y,G₁)]  Re[W(z,G₁)]  Im[W(x,G₁)]  Im[W(y,G₁)]  Im[W(z,G₁)]
   Re[W(x,G₂)]  Re[W(y,G₂)]  Re[W(z,G₂)]  Im[W(x,G₂)]  Im[W(y,G₂)]  Im[W(z,G₂)]
   ...
   ```

6. **Response Matrix** (NP×NP complex numbers):
   ```
   Re[W(G₁,G₁)]  Re[W(G₁,G₂)]  ...  Im[W(G₁,G₁)]  Im[W(G₁,G₂)]  ...
   Re[W(G₂,G₁)]  Re[W(G₂,G₂)]  ...  Im[W(G₂,G₁)]  Im[W(G₂,G₂)]  ...
   ...
   ```

## Physical Interpretation

- **HEAD Matrix**: Represents the macroscopic dielectric response ε⁻¹(q,ω) in the long-wavelength limit
  - Diagonal elements: Screening along principal axes
  - Off-diagonal elements: Cross-coupling between different directions

- **WING/CWING**: Coupling between macroscopic (G=0) and microscopic (G≠0) components of W
  - Important for calculating local field effects
  - WING and CWING are conjugate pairs due to the Hermiticity of W

- **Response Matrix**: Full microscopic screened interaction
  - Used in GW calculations for quasiparticle energies
  - Includes both long-range and local field effects
