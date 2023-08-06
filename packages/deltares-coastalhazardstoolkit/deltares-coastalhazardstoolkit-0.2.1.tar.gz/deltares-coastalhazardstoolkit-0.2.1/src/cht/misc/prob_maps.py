# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 13:57:00 2023

@author: roelvink
"""

import xarray as xr
import numpy as np
import cht.misc.fileops as fo

def prob_floodmaps(file_list, variables, prcs, delete=False, output_file_name=None):
    
    out={}
    out_qq={}
    for i,v in enumerate(variables):
        out[v]= []

    for file in file_list:
        dsin = xr.open_dataset(file)
        for i,v in enumerate(variables):
            out[v].append(dsin[v])

        if delete:
            fo.delete_file(file)

    for i,v in enumerate(variables):
        out[v]= xr.concat(out[v], dim = 'ensemble')
        out_qq[v]= out[v].quantile(prcs, dim="ensemble")
        #Prob of exceedence 0.2 0.5 

    for i,v in enumerate(prcs):
        for ii,vv in enumerate(variables):
            dsin[vv+ "_" + str(round(v*100))]= out_qq[vv][i,:] 
        
    try:
        fo.delete_file(output_file_name)
    except:
        pass
    dsin.to_netcdf(path= output_file_name)
    dsin.close()

def merge_nc_his(file_list, variables, prcs=None, delete=False, output_file_name=None):

    if prcs is None:
        prcs = [0.05, 0.5, 0.95]

    nens = len(file_list)

    # Read first file    
    ds = xr.open_dataset(file_list[0])

    # Read time and stations from first file
    time = ds.time
    stations = ds.stations
    ens = range(nens)

    # Make new data array filled with zeros with dimensions time, stations and ens
    for v in variables:

        arr = xr.DataArray(data=np.zeros((len(time), len(stations), nens)),
                           dims=['time', 'stations', 'ensemble'],
                           coords={'time': time, 'station': stations, 'ensemble': ens})   
        ds[v] = arr  

    for iens, file in enumerate(file_list):
        dsin = xr.open_dataset(file)
        for v in variables:
            ds[v][:,:,iens] = dsin[v]

    for v in variables:
        ds[v].fillna(-999.0) 
        arr = ds[v].fillna(-999.0).quantile(prcs, dim="ensemble")
        for ip, p in enumerate(prcs):
            ds[v + "_" + str(round(p*100))] = arr[ip,:,:] 
        
    try:
        fo.delete_file(output_file_name)
    except:
        pass
    ds.to_netcdf(path= output_file_name)
    ds.close()

def merge_nc_map(file_list, variables, prcs=None, delete=False, output_file_name=None):

    if prcs is None:
        prcs = [0.9]

    nens = len(file_list)

    # Read first file    
    ds = xr.open_dataset(file_list[0])

    # Read time and stations from first file
    # time = ds.timemax
    # x = ds.x
    # y = ds.y
    # ens = range(nens)

    # Make new data array filled with zeros with dimensions time, stations and ens
    for v in variables:
        d = np.zeros((len(ds.timemax), np.shape(ds.x)[0], np.shape(ds.x)[1], nens))
        # Create a dataarray with dimensions time, x, y, ens
        arr = xr.DataArray(data=d,
                            dims=('timemax', 'n', 'm', 'ensemble'),
                            coords={'timemax': ds.timemax, 'x': ds.x, 'y': ds.y, 'ensemble': range(nens)})
        ds[v] = arr

    for iens, file in enumerate(file_list):
        dsin = xr.open_dataset(file)
        for v in variables:
            ds[v][:,:,:,iens] = dsin[v]

    for v in variables:
        arr = ds[v].fillna(-999.0).quantile(prcs, dim="ensemble", skipna=False)
        for ip, p in enumerate(prcs):
            ds[v + "_" + str(round(p*100))] = arr[ip,:,:,:]

    # Remove the original variables
    to_drop = ["zs", "zsmax", "cumprcp", "cuminf", "qinf"]
    for v in to_drop:
        if v in ds:
            ds = ds.drop(v)
        
    try:
        fo.delete_file(output_file_name)
    except:
        pass
    ds.to_netcdf(path= output_file_name)
    ds.close()
