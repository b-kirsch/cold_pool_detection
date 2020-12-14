#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Algorithm to detect and analyze passages of convective cold pools 
from time series data of air temperature and rainfall.   

Contact:
Bastian Kirsch (bastian.kirsch@uni-hamburg.de)
Meteorologisches Institut, Universität Hamburg, Germany

Last revision:
14 December 2020
"""

import numpy as np
import pandas as pd

d_tt           = -2    # Threshold for temperature drop (K)
d_time         = 20    # Time interval of temperature drop (min)

time_pre       = 30    # Time periods before and 
time_post      = 60    # after detected cold-pool passage defining the event (min) 

d_tt_p         = -0.5  # Threshold for initial temperature drop (K) defining
                       # time of cold-pool passage

data_avail_cp  = 1.0   # Minimum relative data availability required during a
                       # cold-pool event to be considered as valid (concerning
                       # both detecting and calculation of perturbation)
data_avail_all = 0.9   # Warning threshold for relative availability of all data


class cp_detection:
    
    def __init__(self,dtdata,ttdata,rrdata,
                 d_tt=d_tt,d_time=d_time,time_pre=time_pre,
                 time_post=time_post,d_tt_p=d_tt_p,
                 data_avail_cp=data_avail_cp,
                 data_avail_all=data_avail_all,
                 warn_avail_cp=True,warn_avail_all=True):
        
        # Check if dtdata is a datetime object and contains a regular time grid
        check_dt   = isinstance(dtdata,pd.DatetimeIndex)
        check_tres = False
        
        if check_dt: 
            dt_freq  = dtdata.inferred_freq 
            check_dt = True
            if dt_freq == None: 
                print('No regular datetime array detected!')
            else:    
                tres = (dtdata[1]-dtdata[0]).seconds/60 
                check_tres = True
        else:
            print('dtdata is not a DatetimeIndex object!')
        
        # Convert ttdata and rrdata into numpy arrays if pd.Series is provided    
        if isinstance(ttdata,pd.Series): ttdata = ttdata.to_numpy(float)
        if isinstance(rrdata,pd.Series): rrdata = rrdata.to_numpy(float)  
        
        # Check if length of provided data arrays is consistent
        self.ntime = dtdata.shape[0] if check_dt else -1
        check_len_tt = self._check_data_len(ttdata,'TT')
        check_len_rr = self._check_data_len(rrdata,'RR')
        
        # Perform cold pool detection if all checks are passed
        check_all = check_dt & check_tres & check_len_tt & check_len_rr
        cp_index  = np.array([])
        
        if check_all:
            # Check overall availability of provided data (only warning if failed)
            self.data_avail_cp  = data_avail_cp
            self.data_avail_all = data_avail_all
            self.warn_avail_cp  = warn_avail_cp
            self.warn_avail_all = warn_avail_all
            self._check_data_avail(ttdata,self.data_avail_all,self.warn_avail_all,'TT')
            self._check_data_avail(rrdata,self.data_avail_all,self.warn_avail_all,'RR')
            
            ntt        = int(d_time/tres)
            self.npre  = int(time_pre/tres)
            self.npost = int(time_post/tres)
            icp_prev   = -99999
            
            # Search for temperature drops of d_tt K within ttt minutes
            with np.errstate(invalid='ignore'):
                t_ttlim = np.where((ttdata[ntt:]-ttdata[:-ntt]) <= d_tt)[0]
            
            for t in t_ttlim:   
                # Filter out cold pool less than time_post minutes after 
                # previous cold pool
                if (t-icp_prev <= self.npost): continue 
            
                # Define time of cold-pool passage
                slc_p = slice(t,t+ntt+1)
                tt_p  = ttdata[slc_p.start]+d_tt_p
                with np.errstate(invalid='ignore'):
                    icp = np.where(ttdata[slc_p] <= tt_p)[0][0]+slc_p.start-1
                    
                # Filter out too short or nan-containing periods
                slc_post = self._index_cp(icp,'post')
                slc_all  = self._index_cp(icp,'all')
                if (slc_all.start < 0) or (slc_all.stop > self.ntime): continue
                check_avail_tt = self._check_data_avail(ttdata[slc_all],
                                                        self.data_avail_cp,False)
                check_avail_rr = self._check_data_avail(rrdata[slc_all],
                                                        self.data_avail_cp,False)
                if not check_avail_tt or not check_avail_rr: continue
            
                # Filter out events without rainfall after cold-pool passage
                if np.sum(rrdata[slc_post]) == 0: continue
                
                # Save time index of cold-pool begin
                cp_index = np.append(cp_index,icp)
                icp_prev = icp    
                
        self.dtdata      = dtdata
        self.ttdata      = ttdata
        self.rrdata      = rrdata        
        self.cp_index    = cp_index.astype(int)  
        self.cp_datetime = dtdata[self.cp_index] if check_dt else self.cp_index
        self.ncp         = len(cp_index)
 
    #--------------------------------------------------------------------------
    #Internal functions
    
    # Return index slices of defined cold-pool event periods
    def _index_cp(self,index_cp,period):
        ipre  = index_cp-self.npre
        ipost = index_cp+self.npost+1
        if period == 'pre' : return slice(ipre,index_cp+1)
        if period == 'post': return slice(index_cp+1,ipost)
        if period == 'all' : return slice(ipre,ipost)
    
    # Check length of data arrays for consistency        
    def _check_data_len(self,indata,varstr):
        try:
            len_indata = indata.shape[0]
        except AttributeError:
            len_indata = 0
        if len_indata == self.ntime:
            return True
        else:
            print(varstr+' data array does not have the same length as datetime array!')
            return False  
    
    # Check data availability
    def _check_data_avail(self,indata,threshold,warn,warnstr='event'):
        data_avail = np.sum(np.isfinite(indata))/indata.shape[0]
        if data_avail >= threshold: 
            return True
        else:
            if warn: 
                print('*** WARNING: Availability of '+warnstr+\
                      ' data is below {:2.0f} %'.format(threshold*100)+\
                      ' ({:2.1f} %) ***'.format(data_avail*100))
            return False
    
    # Perform different calculations on cold-pool-event data (pd.DataFrame) 
    def _calc_val(self,eventdata,funcstr):
        funcavail = ['median','mean','max','min','sum','first','last']
        if funcstr not in funcavail:
            print('Function '+funcstr+' is not available! Pick one of '+\
                  str(funcavail))
            return pd.DataFrame()
        
        if funcstr == 'median': return eventdata.median()
        if funcstr == 'mean'  : return eventdata.mean()
        if funcstr == 'max'   : return eventdata.max()
        if funcstr == 'min'   : return eventdata.min()
        if funcstr == 'sum'   : return eventdata.sum()
        if funcstr == 'first' : return eventdata.iloc[0]
        if funcstr == 'last'  : return eventdata.iloc[-1]
    
    # Apply given function on data of pre-cold-pool-passage period
    def _pre_val(self,eventdata,funcstr):
        if eventdata.empty: return eventdata
        slc_pre = self._index_cp(0,'pre')
        return self._calc_val(eventdata.loc[:slc_pre.stop-1],funcstr)
    
    # Apply given function on data of post-cold-pool-passage period
    def _post_val(self,eventdata,funcstr):
        if eventdata.empty: return eventdata
        slc_post = self._index_cp(0,'post')
        return self._calc_val(eventdata.loc[slc_post.start:],funcstr)
    
    # Apply given function on data of entire cold-pool-event period
    def _all_val(self,eventdata,funcstr):
        if eventdata.empty: return eventdata
        return self._calc_val(eventdata,funcstr)
    
    #--------------------------------------------------------------------------
    # External functions
    
    # Return number of detected cold-pool events
    def number(self):
        return self.ncp
    
    # Return indices of detected cold-pool events
    def indices(self):
        return self.cp_index
    
    # Return datetimes of detected cold-pool events
    def datetimes(self):
        return self.cp_datetime
    
    # Return time series data of provided parameter during detected 
    # cold-pool events
    def var_time(self,indata):
        if isinstance(indata,pd.Series): indata = indata.to_numpy(float)
        check_len = self._check_data_len(indata,'Provided')
        if not check_len: return pd.DataFrame()
        self._check_data_avail(indata,self.data_avail_all,self.warn_avail_all,
                               'provided')
        event_index = np.arange(-self.npre,self.npost+1)

        
        outdata = pd.DataFrame(index=event_index)
        for cp,icp in enumerate(self.cp_index):
            slc_all = self._index_cp(icp,'all')
            check_avail = self._check_data_avail(indata[slc_all],
                                                 self.data_avail_cp,
                                                 self.warn_avail_cp)
            outdata[self.cp_datetime[cp]] = indata[slc_all] if check_avail else np.nan
            
        return outdata  
    
    # Return perturbations of provided parameter during detected 
    # cold-pool events given by the differences between the values
    # calculated for the pre and post-cold-pool-passage periods
    # according to the provided function strings
    def var_pert(self,indata,prefunc,postfunc):
        pre_val  = self._pre_val(self.var_time(indata),prefunc)
        post_val = self._post_val(self.var_time(indata),postfunc)
        return post_val - pre_val
    
    # Return certian values of provided parameter during detected 
    # cold-pool events for given periods and function string
    def var_val(self,indata,period,funcstr):
        periods = ['pre','post','all']
        if period not in periods:
            print('Period '+period+' is not available! Pick one of '+\
                  str(periods))
            return pd.DataFrame()
        
        if period == 'pre': 
            return self._pre_val(self.var_time(indata),funcstr)
        if period == 'post': 
            return self._post_val(self.var_time(indata),funcstr)
        if period == 'all': 
            return self._all_val(self.var_time(indata),funcstr)
        
    # Return temperature perturbations during detected cold-pool events
    def tt_pert(self):
        return self.var_pert(self.ttdata,prefunc='median',postfunc='min')
    
    # Return median temperature values during pre-cold-pool-passage periods
    def tt_pre(self):
        return self._pre_val(self.var_time(self.ttdata),'median')
    
    # Return temperature time series data during detected cold-pool events
    def tt_time(self):
        return self.var_time(self.ttdata)
    
    # Return rainfall accumulations during detected cold-pool events
    def rr_sum(self):
        return self._all_val(self.var_time(self.rrdata),'sum')
    
    # Return maximum rainfall rate during detected cold-pool events
    def rr_max(self):
        return self._all_val(self.var_time(self.rrdata),'max')
    
    # Return rainfall time series data during detected cold-pool events
    def rr_time(self):
        return self.var_time(self.rrdata)
    
    # Return air pressure perturbations during detected cold-pool events
    def pp_pert(self,ppdata):
        return self.var_pert(ppdata,prefunc='median',postfunc='max')
    
    # Return wind speed perturbations during detected cold-pool events
    def ff_pert(self,ffdata):
        return self.var_pert(ffdata,prefunc='median',postfunc='max')
    