# VIP-CSI (Domingo): Research material on compressive sensing

Welcome! In this repository, you will find (almost) all my research on compressive sensing including reference books, Jupyter notebooks, reference papers, RM slides, and progress report slides. I have not included custom algorithms and datasets since they are too large to be uploaded here; you will have to search for them yourself should you encounter them in any of the experiments. If you want to reuse/recreate the research contained herein, you will first have to set up an environment on your computer.

## Windows
- First, make sure that you have a strong, stable internet connection.
- Go to [Python.org](https://python.org/downloads) and search for Python version 3.6.8 and install it using your preferred settings. Make sure pip is installed along with it.
- Open a Git bash terminal and `cd` to some directory on your computer.
- Run the following lines one at a time:
```
git clone https://github.com/kvdomingo/VIP-CSI
cd VIP-CSI
python -m pip install --upgrade pip
python -m pip install virtualenv
python -m venv env
source env/scripts/activate
python -m pip install -f requirements.txt
```

## Linux (Ubuntu)
- Open a terminal and `cd` to your working directory.
- Run the following commands:
```
sudo apt-get update
sudo apt-get install git python3.6
git clone https://github.com/kvdomingo/VIP-CSI
cd VIP-CSI
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
pip3 install -U pip
pip3 install virtualenv
virtualenv env
source env/bin/activate
pip3 install -r requirements.txt
```
