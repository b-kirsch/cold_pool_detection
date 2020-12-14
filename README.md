# cold_pool_detection

## Description
Algorithm to detect and analyze passages of convective cold pools 
from time series data of air temperature and rainfall. Cold-pool passages
are detected from rapid temperature drops (default: -2 K within 20 min) 
associated with non-zero rainfall. A cold-pool event is defined as a
time period prior to the time of detected cold-pool passage
and after it (default: 30 and 60 min). Characteristic values within these pre-
and post-passage periods are used to calculate the perturbation strength
for given parameters. The characteristics of any additionally provided 
variables during one or both of these periods of the cold-pool events 
(*pre, post, all*) can be analyzed by applying typcial operations 
(*median, mean, max, min, sum, first, last*) to these data. Furthermore, the 
underlying time series data itself can be written to output for further 
analyses.

## Usage
### Required Input 
* `dtdata`: pandas DatetimeIndex array with a regular time grid (resolution of 10 min or smaller is recommended)     
* `ttdata`: numpy array or pandas series of same length as `dtdata` containing air temperature data (in °C or K)      
* `rrdata`: numpy array or pandas series of same length as `dtdata` containing data of rainfall amount (not intensity)     
              
### Optional Input      
* `indata`: numpy array or pandas series of same length as `dtdata`
            containing any given variable
              
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
