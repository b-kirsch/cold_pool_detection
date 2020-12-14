# cold_pool_detection

## Description
Algorithm to detect and analyze passages of convective cold pools 
from time series data of air temperature and rainfall. Cold-pool passages
are detected from rapid temperature drops associated with non-zero rainfall. 
A cold-pool event is defined as a time period prior to the time of detected 
cold-pool passage and after it. Characteristic values within these pre-
and post-passage periods are used to calculate the perturbation strength
for given parameters. The characteristics of any additionally provided 
variables during one or both of these periods of the cold-pool events 
(*pre, post, all*) can be analyzed by applying typcial operations 
(*median, mean, max, min, sum, first, last*) to these data. Furthermore, the 
underlying time series data itself can be written to output for further 
analyses.

## Usage
### Required Input 
* `dtdata` (DatetimeIndex): Time data with regular grid (resolution of 10 min or smaller is recommended)     
* `ttdata` (1-d array or pandas.Series): Air temperature data (in °C or K) of same length as `dtdata`     
* `rrdata` (1-d array or pandas.Series): Rainfall amount data of same length as `dtdata`   
            
### Parameters
* `d_tt` (float): Threshold for temperature drop in K (*default: -2*)
* `d_time` (integer): Time interval of temperature drop in min (*default: 20*)
* `time_pre` (integer): Length of pre-passage time period in min (*default: 30*)
* `time_post` (integer): Length of post-passage time period in min (*default: 60*)
* `d_tt_p` (float): Threshold for initial temperature drop in K defining time of cold-pool passage (*default: -0.5*)
* `data_avail_cp` (float): Minimum relative fraction of data availability required during a cold-pool event to be considered as valid, concerning both detection and calculation of perturbations (*default: 1.0*)
* `data_avail_all` (float): Relative fraction of data availability for input data below which a warning is issued (*default: 0.9*)
* `warn_avail_cp` (bool): Indicates if a warning is issued when a perturbation is not calculated due to a too low event-specific data availability (*default: True*)
* `warn_avail_all` (bool): Indicates if a warning is issued for a too low data availability of input data (*default: True*)

### Optional Input      
* `indata` (1-d array or pandas.Series): Any given variable of same length as `dtdata`
            
### Example
```python
    import cp_detection_timeseries as cpdt
    cp = cpdt.cp_detection(dtdata,ttdata,rrdata)     # Perform cold-pool detection
    cp_number   = cp.number()                        # Integer number of detected cold-pool events
    cp_times    = cp.datetimes()                     # Datetime array of cold-pool passage times
    cp_indices  = cp.indices()                       # Numpy array of cold-pool passage time indices 
    cp_tt_pert  = cp.tt_pert()                       # Pandas dataframe of temperature perturbations indexed by corresponding datetimes                                   
    cp_tt_time  = cp.tt_time()                       # Pandas dataframe of temperature time series during events indexed by timesteps relative to passage time
    cp_pp_pert  = cp.pp_pert(ppdata)                 # Pandas dataframe of air pressure perturbations  
    cp_any_time = cp.var_time(indata)                # Pandas dataframe of time series of any variable during events
    cp_any_pert = cp.var_pert(indata,'median','min') # Pandas dataframe of perturbations of any variable
    cp_any_val  = cp.var_val(indata,'pre','max')     # Pandas dataframe of characteristic value of any variable
```    


## Software Versions
* python 3.8.3
* numpy 1.18.5
* pandas 1.0.5
    

## Contact
Bastian Kirsch (bastian.kirsch@uni-hamburg.de) <br>
Meteorologisches Institut, Universität Hamburg, Germany

Last revision: 14 December 2020
