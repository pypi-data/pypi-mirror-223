# scReadSim <img src="./docs/source/_static/logo_scReadSim.png?raw=true" align="right" width="150"/>
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/screadsim/badge/?version=latest)](https://screadsim.readthedocs.io/en/latest/?badge=latest)

A single-cell RNA-seq and ATAC-seq read simulator.

<!-- ## Update Log
**June 18th**
- Update UMI module and upload to PyPI.

**May 4th**
- Update random error module.

**April 20th**
- Update read length generation.

**March. 31st**
- Update documentation of functions.


**March. 30th**
- Set up documentation framework.
- Update demo data.


**March. 11st**
- Update INPUT moldue.
- Update test script for scATAC-seq INPUT module using demo data.

**March. 10th**
- Update BAM generation and synthetic count matrix traning.
- Update test script for scRNA-seq module and scATAC-seq module using demo data.

**Feb. 10th**
- Update synthetic count matrix generation functions. 

**Feb. 7th**
- Update scRNA-seq module
- Local installation tested.

**Feb. 3rd**
- Test scATAC-seq module.
- Local installation tested.

**Feb. 2nd**
- Upload scATAC-seq module. -->

## Quick Install
Install scReadSim (most updated version) from Github
```bash
pip install git+https://github.com/JSB-UCLA/scReadSim.git
```
or install from PyPI
```bash
pip install scReadSim
```


## About
Single-cell sequencing technologies emerged and diversified rapidly in the past few years, along with the successful development of many computational tools. Realistic simulators can help researchers benchmark computational tools. However, few simulators can generate single-cell multi-omics data, and none can generate reads directly. To fill in this gap, we propose scReadSim, a simulator for single-cell multi-omics reads. Trained on real data, scReadSim generates synthetic sequencing reads in BAM or FASTQ formats. We deployed scReadSim on a sci-ATAC-seq dataset and a single-cell multimodal dataset to show the resemblance between synthetic data and real data at the read and count levels. Moreover, we show that scReadSim allows user-specified ground truths of accessible chromatin regions for single-cell chromatin accessibility data generation. In addition, scReadSim is flexible for allowing varying throughputs and library sizes as input parameters to guide experimental design.

## Website
For tutorials and other details, check [our website](http://screadsim.readthedocs.io/).

## License
This pacakge is licensed under the terms
of the **MIT License**.

