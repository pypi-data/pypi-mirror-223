# matplotlib-polyroi

[![CC BY 4.0][cc-by-shield]][cc-by]
[![PyPi version](https://badgen.net/pypi/v/matplotlib-polyroi/)](https://pypi.org/project/matplotlib-polyroi)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/tsmbland/matplotlib-polyroi/HEAD?filepath=%2Fscripts/Demonstration.ipynb)
[![run with docker](https://img.shields.io/badge/run%20with-docker-0db7ed?logo=docker)](https://www.docker.com/)
[![run with conda](http://img.shields.io/badge/run%20with-conda-3EB049?logo=anaconda)](https://docs.conda.io/en/latest/)

Module for selecting polygonal ROIs on images, spline fitting and ROI expansion

## Installation

    pip install matplotlib-polyroi


## Instructions

See the [tutorial notebook](https://nbviewer.org/github/tsmbland/matplotlib-polyroi/blob/master/scripts/Demonstration.ipynb) for instructions on usage. To run the notebook interactively you have two options:


#### Option 1: Binder

To run in the cloud, click here: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/tsmbland/matplotlib-polyroi/HEAD?filepath=%2Fscripts/Demonstration.ipynb)

(Please note that it may take several minutes to open the notebook)

#### Option 2: Docker

Step 1: Make sure [Docker](https://www.docker.com/products/docker-desktop/) is installed and open on your machine 

Step 2: Run the Docker container: 

    docker run --rm -p 8888:8888 tsmbland/matplotlib-polyroi

Once the Docker image has finished downloading, this will print two URLs at the bottom for you to copy and paste into your web browser to open up Jupyter (please try both)

Step 3: Navigate to _scripts/Demonstration.ipynb_ to run the notebook

Step 4: When finished, delete the image:

    docker image rm tsmbland/matplotlib-polyroi

#### Option 3: Conda

You can use the environment.yml file to set up a [Conda](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html) environment on your machine from which the notebook can be run

    conda env create -f environment.yml
    conda activate matplotlib-polyroi
    jupyter notebook

## License

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
