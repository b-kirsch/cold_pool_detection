# cold_pool_detection

## Description
Algorithm to detect and analyze passages of convective cold pools 
from time series data of air temperature and rainfall. Cold-pool passages
are detected from rapid temperature drops (default: -2 K within 20 min) 
associated with non-zero rainfall. A cold-pool event is defined by a
time period prior to the time of detected cold-pool passage (default: 30 min) 
and after it (default: 60 min). Characteristic values within these pre-
and post-passage periods are used to calculate the perturbation strength
for given parameters. Several common functions can be applied on one or both
of these periods ('pre','post','all') for any additionally provided variable 
to analyze its characteristics during the cold-pool events. Furthermore, the 
underlying time series data itself can be written to output for further analyses.

## Usage
### Required Input 
* `dtdata`: datetime array containing regular time grid (resolution of at 
            least 10 min is recommended)     
* `ttdata`: numpy array or pandas series of same length as dtdata 
            containing air temperature data         
* `rrdata`: numpy array or pandas series of same length as dtdata 
            containing data of interval-accumulated rainfall amount     
              
### Optional Input      
* `indata`: numpy array or pandas series of same length as dtdata 
            containing any given variable
              
### Example
```python
    import cp_detection_timeseries as cpdt
    cp = cpdt.cp_detection(dtdata,ttdata,rrdata) 
    cp_number   = cp.number()                    
    cp_times    = cp.datetimes()                
    cp_inidces  = cp.indices()                   
    cp_tt_pert  = cp.tt_pert()                                                           
    cp_tt_time  = cp.tt_time()                   
    cp_pp_pert  = cp.pp_pert(ppdata)
    cp_any_time = cp.var_time(idata)
    cp_any_pert = cp.var_pert(indata,'median','min')
    cp_any_val  = cp.var_val(indata,'pre','max')
```    


## Software Versions
* python 3.8.3
* numpy 1.18.5
* pandas 1.0.5
    

## Contact
Bastian Kirsch (bastian.kirsch@uni-hamburg.de)
Meteorologisches Institut, Universität Hamburg, Germany

Last revision: 11 December 2020
