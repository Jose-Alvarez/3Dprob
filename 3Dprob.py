#!/usr/bin/env python3

# 3Dprob, multivariate normal probabilities for 3D locations inside a cube.
# Copyright (C) 2024  Jose A. Alvarez-Gomez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Version 0.1
#    First release
#
import sys
import numpy as np
import pandas as pd
import argparse
from io import StringIO
from scipy.stats import norm

# Command line parser
parser = argparse.ArgumentParser(
    description='Computation of multivariate normal probabilities for 3D locations inside a cube.',
    formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument(
    'infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
    help='The expected input file format:\n[lon e_lon lat e_lat dep e_dep [others...]]\n'
)
parser.add_argument(
    '-l', required=True,
    help='Limits of the cube in the format: "x_min,x_max,y_min,y_max,z_min,z_max"\n'
)
parser.add_argument(
    '-v', action='count', default=0,
    help='If present, the program will show additional processing information.\n'
)
# Show help if there are no arguments
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

# Parse arguments
args = parser.parse_args()

# If -l is not given, show help and exit
if args.l is None:
    parser.print_help()
    sys.exit(1)

# Read data and handle non-seekable streams (like pipes)
content = args.infile.read()  # Read all content at once

# Verbose output
if args.v:
    sys.stderr.write(f'Working on input: {args.infile.name}\n')

# Extract column names from the first comment line
columnas = None
lines = content.splitlines()
for line in lines:
    if line.startswith("#"):
        columnas = line[1:].split()  # Remove "#" and split by spaces
        break

# Convert remaining lines to a DataFrame
data = pd.read_csv(
    StringIO(content),  # Usa StringIO desde io en lugar de pandas.compat
    header=None,
    comment='#',
    sep=r'[,\s\t]+',
    engine='python'
)

# If no column names are found, assign default names
if not columnas:
    num_columns = data.shape[1]
    columnas = [f'col{i}' for i in range(num_columns)]
    if args.v:
        sys.stderr.write("Warning: No column names found. Using default names.\n")

data.columns = columnas
#data_restante = data[columnas[6:]]  # Columns beyond the first 6

# Parse cube limits
try:
    limits = list(map(float, args.l.split(',')))
    x_min, x_max, y_min, y_max, z_min, z_max = limits
except ValueError:
    sys.stderr.write("Error: Invalid cube limits format. Expected: x_min,x_max,y_min,y_max,z_min,z_max\n")
    sys.exit(1)

# Extract coordinates and errors
x, ex, y, ey, z, ez = [data[col].astype(float) for col in columnas[:6]]

# Initialize probability array
n_events = data.shape[0]
p = np.zeros(n_events)

# Compute probabilities
epsilon = 1e-6  # Small value to avoid zero errors
for row in range(n_events):
    mu = [x[row], y[row], z[row]]

    # Adjust errors to ensure they are >= epsilon
    ex_adj = max(ex[row], epsilon)
    ey_adj = max(ey[row], epsilon)
    ez_adj = max(ez[row], epsilon)

    Sigma = np.diag([ex_adj**2, ey_adj**2, ez_adj**2])  # Diagonal covariance matrix

    # For each dimension, compute the probability of being inside the interval
    p_x = norm.cdf((x_max - x[row]) / ex_adj) - norm.cdf((x_min - x[row]) / ex_adj)
    p_y = norm.cdf((y_max - y[row]) / ey_adj) - norm.cdf((y_min - y[row]) / ey_adj)
    p_z = norm.cdf((z_max - z[row]) / ez_adj) - norm.cdf((z_min - z[row]) / ez_adj)

    # The total probability is the product of the probability for each coordinate range.
    p[row] = p_x * p_y * p_z

    # Informative message in verbose mode
    if args.v and (ex[row] < epsilon or ey[row] < epsilon or ez[row] < epsilon):
        sys.stderr.write(
            f"Warning: Row {row} has errors close to zero. "
            f"Adjusted to {epsilon} to avoid singularities.\n"
        )


# Create output DataFrame
output = {
    **{col: data[col] for col in columnas},  # Original columns
    'p': p  # Probability column added last
}
out_df = pd.DataFrame(output)

# Save as CSV
sys.stdout.write("#" + " ".join(out_df.columns) + "\n")
out_df.to_csv(sys.stdout, index=False, sep=' ', header=False)
