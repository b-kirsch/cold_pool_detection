# cold_pool_detection

## Description
Algorithm to detect and analyze passages of convective cold pools 
from time series data of air temperature and rainfall. Cold-pool passages
are detected from rapid temperature drops associated with non-zero rainfall. 
A cold-pool event is defined by time periods prior to and after the time of 
detected cold-pool passage. Characteristic values within these pre-
and post-passage periods are used to calculate the perturbation strength
for given parameters. The characteristics of any additionally provided 
variables during one or both of these periods of the cold-pool events 
can be analyzed by applying pre-defined operations to these data. Furthermore, the 
underlying time series data itself can be written to output for further 
analyses.

## Usage

### cp_detection
Performs the cold-pool detection (instance method)
#### Parameters (required):
* `dtdata` (DatetimeIndex): Time data with regular grid (resolution of 10 min or smaller is recommended)     
* `ttdata` (1-d array or pandas.Series): Temperature data of same length as `dtdata`     
* `rrdata` (1-d array or pandas.Series): Rainfall amount data of same length as `dtdata`            
#### Parameters (optional):
* `d_tt` (float): Threshold for temperature drop in K (default: -2)
* `d_time` (integer): Time interval of temperature drop in min (default: 20)
* `time_pre` (integer): Length of pre-passage time period in min (default: 30)
* `time_post` (integer): Length of post-passage time period in min (default: 60)
* `d_tt_p` (float): Threshold for initial temperature drop in K defining time of cold-pool passage (default: -0.5)
* `data_avail_cp` (float): Minimum relative fraction of data availability required during a cold-pool event to be considered as valid, concerning both detection and calculation of perturbations (default: 1.0)
* `data_avail_all` (float): Relative fraction of data availability for input data below which a warning is issued (default: 0.9)
* `warn_avail_cp` (bool): Indicates if a warning is issued when a perturbation is not calculated due to a too low event-specific data availability (default: *True*)
* `warn_avail_all` (bool): Indicates if a warning is issued for a too low data availability of input data (default: *True*)

### number
Returns number of detected cold-pool events 
#### Parameters: 
*None*

### indices
Returns array indices of passage times
#### Parameters 
*None*

### datetimes
Returns Datetime indices of passage times
#### Parameters 
*None*

### tt_pert
Returns pandas.DataFrame of temperature perturbations defined as difference between post-passage minimum and pre-passage median values
#### Parameters 
*None*

### tt_pre
Returns pandas.DataFrame of pre-passage median temperature values
#### Parameters 
*None*

### tt_time
Returns pandas.DataFrame of temperature time series during cold-pool events
#### Parameters 
*None*

### rr_sum
Returns pandas.DataFrame of event-accumulated rainfall amounts
#### Parameters 
*None*

### rr_max
Returns pandas.DataFrame of maximum rainfall values
#### Parameters 
*None*

### rr_time
Returns pandas.DataFrame of rainfall time series during cold-pool events
#### Parameters 
*None*

### pp_pert
Returns pandas.DataFrame of air pressure perturbations defined as difference between post-passage maximum and pre-passage median values
#### Parameters (required)
* `ppdata` (1-d array or pandas.Series): Air pressure data of same length as `dtdata`  

### ff_pert
Returns pandas.DataFrame of wind speed perturbations defined as difference between post-passage maximum and pre-passage median values
#### Parameters (required)
* `ffdata` (1-d array or pandas.Series): Wind speed data of same length as `dtdata`  

### var_pert
Returns pandas.DataFrame of perturbations of given variable as difference between post-passage and pre-passage values
#### Parameters (required)
* `indata` (1-d array or pandas.Series): Data of variable of same length as `dtdata` 
* `prefunc` (string): Operation to be applied on pre-passage data (available operations: *median, mean, max, min, sum, first, last*)
* `postfunc` (string): Operation to be applied on post-passage data

### var_val
Returns pandas.DataFrame of defined values of given variable
#### Parameters (required)
* `indata` (1-d array or pandas.Series): Data of variable of same length as `dtdata` 
* `period` (string): Period of cold-pool event for which values are calculated (available periods: *pre, post, all*)
* `funcstr` (string): Operation to be applied on data (available operations: *median, mean, max, min, sum, first, last*)

### var_time
Returns pandas.DataFrame of time series of given variable during the cold-pool events
#### Parameters (required)
* `indata` (1-d array or pandas.Series): Data of variable of same length as `dtdata`  


## Example
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
