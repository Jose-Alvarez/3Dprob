# 3Dprob
Multivariate normal probabilities for 3D locations inside a cube.

markdown

# 3Dprob

**Version:** 0.1  
**Author:** Jose A. Alvarez-Gomez  
**License:** GPL-3.0

`3Dprob` is a command-line tool written in Python that computes the probability that a three-dimensional location (with associated errors) lies within a user-defined cube, assuming a multivariate normal distribution with independent components (diagonal covariance matrix). It is useful in geosciences, geodesy, or any field requiring the evaluation of the probability that an uncertain point lies inside a cubic region.

## ✨ Features

- Reads data from a file or standard input.
- Computes the joint probability as the product of univariate probabilities in each dimension (independence assumption).
- Handles very small errors by adjusting them to an epsilon value (`1e-6`) to avoid singular matrices.
- Output format is readable and easy to process.
- Verbose mode (`-v`) for debugging information.

## 📥 Installation

### Requirements

- Python 3.6 or higher.
- Dependencies: `numpy`, `pandas`, `scipy`.

### Quick Install

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/3Dprob.git
   cd 3Dprob
