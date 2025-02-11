<h1 style="display: flex; align-items: center;">
  <span>Kaya - Screening Analysis Tool</span>
  <img src="docs/kaya.jpg" alt="Kaya" width="80" style="margin-left: 10px;">
</h1>

> ℹ️ **Important:** This is more or less a test repo., so all the files are not here!

Tools for analyzing frequency-dependent screening in VASP calculations, particularly focused on Auger recombination in perovskite materials.

## Features

- Read and parse VASP WFULL files containing screened Coulomb interaction data
- Extract frequency-dependent W(G,G',q,ω)
- Calculate Auger recombination matrix elements

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
- [Parsing Strategy](docs/parsing_strategy.md)
- [Auger Calculation Strategy](docs/auger_calculation_strategy.md)

## Project Structure

```
kaya/
├── docs/                    # Documentation
│   ├── WFULL_format.md     # WFULL file format description
│   ├── parsing_strategy.md # Detailed parsing methodology
│   └── auger_calculation_strategy.md  # Calculation methodology
├── read_wfull_data.py      # Main script for reading WFULL files
├── read_wfull.py           # Alternative reader implementation
└── read_wfull_debug.py     # Debugging utilities
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
