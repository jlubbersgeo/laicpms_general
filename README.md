# LA-ICP-MS Data Processing

Raw data output from LA-ICP-MS is in the form of counts per second (cps). When integrated over a certain period of time (e.g., the width of an analysis peak), we get a total number of counts for a given analyte per spot analysis. This total number of counts is a function of many things, but namely: the number of analytes being analyzed, the dwell time of the ICP-MS on each analyte, and the total analysis time. While important to understand the so-called “ins and outs” of LA-ICP-MS, to help maximize the quality of data output from the instrument, they are not requisite for calculating concentrations from raw data. 

This repository is a collection of scripts that will help a LA-ICP-MS user do the following:
- preprocess data from a ThermoFisher iCAP RQ ICP-MS and Agilent 8900 QQQ so that it is in a form that is ready for data reduction
  - ```make_lasertram_ready_gui_agilent```, ```make_lasertram_ready_gui_thermo```, ```multifilier``` scripts
- show hard coded Jupyter notebook examples of how to calculate concentrations after peak intervals are chosen for a given spot analysis
  - ```lasercalc_python.ipynb```

This repository is a work in progress and will be periodically updated. For more information on our open-source laser ablation processing tools please see the [LaserTRAM-DB](https://github.com/jlubbersgeo/laserTRAM-DB) repository. 

please contact Jordan Lubbers with any questions

## Use

### Preprocessing
To prepocess your data for [```LaserTRAM-DB```](https://github.com/jlubbersgeo/laserTRAM-DB) it is recommended that you create a virtual environment (we prefer Anaconda). Once you have this virtual environment set up you will not have to do it again for ```LaserTRAM-DB```.
```
conda create -n lasertram-db python=3.7.7
conda activate lasertram-db
git clone https://github.com/jlubbersgeo/laicpms_general
cd /path/to/laicpms_general
conda install --file requirements.txt
python multifiler.py
```

The ```multifiler.py``` script will create a GUI based on which type of mass spec your data are from and then combine all the requisite csv files into one spreadsheet such that it can be loaded into ```LaserTRAM-DB```. 

### LaserCalc
the ```lasercalc_python.ipynb``` notebook contains much of the code that is in ```LaserTRAM-DB``` for calculating concentrations from data that has been normalized to an internal standard. If you are "python savvy" you may wish to go this route for determining concentrations, however it is almost always easier to use the GUI in this regard. This was created so as to enhance transparency with the software. We believe that how geochemists obtain numbers from their instruments should not be a black box, but rather a well documented and well informed series of decisions. Let this notebook help with that. 


*Happy Processing!*<br>
-Jordan
