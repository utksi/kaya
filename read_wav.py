#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from pymatgen.io.vasp.outputs import Wavecar

# Specify the k-point and band index
kpoint = [0.5, 0.5, 0.5]
band = 0

# Read the WAVECAR file and get the FFT mesh and phase factors for the k-point and band index
wavecar = Wavecar("WAVECAR")
mesh = wavecar.fft_mesh(kpoint, band)
coefficients = mesh.reshape(-1)
phase_factors = np.exp(-1j * np.dot(mesh.real_space_mesh, kpoint))

# Compute the full wave function
wave_function = phase_factors * coefficients
wave_function = wave_function.reshape(mesh.shape)

# Compute the Coulomb kernel
r = wavecar.real_space_mesh
k = np.linalg.norm(kpoint)
G = wavecar.Gpoints[0]
Coulomb_kernel = np.sum(np.sum(np.sum(np.conj(wave_function) * wave_function / np.sqrt(np.sum((k + G)**2, axis=1)) * np.exp(1j * np.dot(r, k + G)), axis=0), axis=0), axis=0)

# Compute Fermi's golden rule expression
hbar = 1.054571817e-34
eV_to_J = 1.6021766208e-19
omega = 0.1 * eV_to_J / hbar
k_B = 1.38064852e-23
T = 300
prefactor = 2 * np.pi / hbar * omega * Coulomb_kernel
gamma = prefactor * np.sqrt(2 * np.pi * k_B * T / hbar)
