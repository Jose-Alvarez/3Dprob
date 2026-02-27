# 3Dprob
Multivariate normal probabilities for 3D locations inside a cube.

**Version:** 0.1  
**Author:** Jose A. Alvarez-Gomez  
**License:** GPL-3.0

`3Dprob` is a command-line tool written in Python that computes the probability that a three-dimensional location (with associated errors) lies within a user-defined cube, assuming a multivariate normal distribution with independent components (diagonal covariance matrix). It is useful in geosciences, geodesy, or any field requiring the evaluation of the probability that an uncertain point lies inside a cubic region.

## Features

- Reads data from a file or standard input.
- Computes the joint probability as the product of univariate probabilities in each dimension (independence assumption).
- Handles very small errors by adjusting them to an epsilon value (`1e-6`) to avoid singular matrices.
- Output format is readable and easy to process.
- Verbose mode (`-v`) for debugging information.

## Installation

### Requirements

- Python 3.6 or higher.
- Dependencies: `numpy`, `pandas`, `scipy`.

### Quick Install

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/3Dprob.git
   cd 3Dprob

2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt

## Usage
   ```text
   python 3Dprob.py [-l LIMITS] [-v] [input_file]
   ```

### Arguments

| Argument | Description |
| --- | :--------- |
| ```input_file``` | File containing the data. If not provided, reads from standard input (```stdin```). |
|```-l LIMITS``` | **Required**. Cube limits in the format: ```x_min,x_max,y_min,y_max,z_min,z_max``` (real numbers). |
| ```-v``` | Verbose mode. Shows additional information (e.g., warnings about near-zero errors). |

### Input File Format

The file must contain at least 6 columns (it may have more) with the following coordinates and errors:
   ```text
   # lon e_lon lat e_lat dep e_dep [others...]
   ```
- Columns can be separated by spaces, tabs, or commas.
- Lines starting with # are interpreted as comments. The first comment line is used to name the columns. If there are no comments, default names are assigned (col0, col1, ...).

#### Example (```data.txt```):
   ```text
   # lon e_lon lat e_lat dep e_dep
   -3.5 0.2 40.1 0.3 12.0 1.5
   -3.6 0.1 40.2 0.2 11.8 1.2
   ...
   ```

#### Example Run
   ```bash
   python 3Dprob.py -l "-4,-3,39,41,10,15" -v data.txt > results.txt
   ```
This reads ```data.txt```, computes the probability that each point lies inside the cube defined by:
- x (lon) from -4 to -3
- y (lat) from 39 to 41
- z (dep) from 10 to 15

and saves the results in ```results.txt```.
### Output

The program writes to standard output a file with the same original columns plus an additional column named ```p``` containing the computed probability. The first line starts with ```#``` and contains the column names.

#### Example output:
```text

# lon e_lon lat e_lat dep e_dep p
-3.5 0.2 40.1 0.3 12.0 1.5 0.789
-3.6 0.1 40.2 0.2 11.8 1.2 0.921
...
```

## Probability Calculation

For each row, with coordinates ```(x, y, z)``` and errors ```(ex, ey, ez)```, a three-dimensional normal distribution is assumed with mean ```(x, y, z)``` and diagonal covariance matrix ```diag(ex², ey², ez²)```. Because the components are independent, the joint probability that the point lies inside the cube ```[x_min, x_max] × [y_min, y_max] × [z_min, z_max]``` is the product of the marginal probabilities:
```text
p = P(x_min ≤ X ≤ x_max) · P(y_min ≤ Y ≤ y_max) · P(z_min ≤ Z ≤ z_max)
```
Each marginal probability is computed using the standard normal cumulative distribution function:
```text
P(a ≤ X ≤ b) = Φ((b - μ)/σ) - Φ((a - μ)/σ)
```
where ```Φ``` is the CDF of the standard normal distribution.

### Important Notes
- Independence between coordinates is assumed. If your data have correlations, this program is not suitable (you would need a full covariance matrix).
- Errors are interpreted as standard deviations (not variances). The program squares them to form the covariance matrix.
- The cube must be well-defined: x_min < x_max, etc. This is not explicitly checked.
