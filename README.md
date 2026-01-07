# Overview

This repository is used to compare the estimated photophysical parameters of noisy and denoised image sequences from SMLM.

## Prerequisites

- Python >= 3.11 < 3.14
- A Python virtual environment
- Two SMLM image sequences saved as .tif files

## Installation

Create a virtual environment then run:
```shell
git clone https://github.com/Matthewt303/dn-photophys-analysis.git
cd dn-photophys-analysis
python3 -m pip install .
```
## Usage

A script called ```photon-analysis``` should become available which can be used as:

```bash
photon-analysis --image_path /path/to/im_sequence.tif --dn_image_path /path/to/denoised/im_sequence.tif --output_path /path/to/output_folder --pixel_size_um 0.01 --adu 0.45 --gain 1 --offset 100
```

Note that the script has a relatively high memory usage (~32 GB but depends on file sizes) since it carries out simultaneous localisation for two image sequences.

## Parameters

- pixel_size_um, the length of a pixel at the sample plane. Must be in micrometers.
- adu, analog-digital conversion rate.
- offset, camera baseline graycount.
- gain, EMCCD gain. Set to 1 if not using an EMCCD.

## Acknowledgements

The expressions for the PSF and its derivatives are from [Picasso](https://github.com/jungmannlab/picasso) [1].

[1](https://github.com/jungmannlab/picasso) Schnitzbauer, J., Strauss, M., Schlichthaerle, T. et al. Super-resolution microscopy with DNA-PAINT. *Nature Protocols* **12**, 1198–1228 (2017)