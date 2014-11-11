#!/usr/bin/env python
"""
   class that reads the NASA hdfeos CoreMetadata.0 attribute
   and retrieves the orbitnumber, equator crossing time, 
   image lat/lon corners, etc.
"""

import types
import numpy as np
import h5py
import argparse

class metaParse:
    def __init__(self,metaDat,altrDat):
        import re
        self.metaDat=metaDat
        self.altrDat=altrDat
        #search for the string following the words "VALUE= "
        self.stringObject=\
             re.compile('.*VALUE\s+=\s"(?P<value>.*)"',re.DOTALL)
        #search for a string that looks like 11:22:33
        self.timeObject=\
             re.compile('.*(?P<time>\d{2}\:\d{2}\:\d{2}).*',re.DOTALL)
        #search for a string that looks like 2006-10-02
        self.dateObject=\
             re.compile('.*(?P<date>\d{4}-\d{2}-\d{2}).*',\
                        re.DOTALL)
        #search for a string that looks like "(anything between parens)"
        self.coordObject=re.compile('.*\((?P<coord>.*)\)',re.DOTALL)
        #search for a string that looks like "1234"
        self.orbitObject=\
             re.compile('.*VALUE\s+=\s(?P<orbit>\d+)\n',re.DOTALL)

    def getstring(self,theName):
        theString=self.metaDat.split(theName)
        #should break into three pieces, we want middle
        if len(theString) ==3:
            theString=theString[1]
        else:
            
            altString=self.altrDat.split(theName)
            if len(altString) == 3:
                theString=altString[1]
            else:
                raise "couldn't parse %s" % (theName,)
        return theString
        

    def __call__(self,theName):
        if theName=='CORNERS':
            import string
            #look for the corner coordinates by searching for
            #the GRINGPOINTLATITUDE and GRINGPOINTLONGITUDE keywords
            #and then matching the values inside two round parenthesis
            #using the coord regular expression
            theString= self.getstring('GRINGPOINTLATITUDE')
            theMatch=self.coordObject.match(theString)
            thelats=theMatch.group('coord').split(',')
            thelats=map(string.atof,thelats)
            theString= self.getstring('GRINGPOINTLONGITUDE')
            theMatch=self.coordObject.match(theString)
            thelongs=theMatch.group('coord').split(',')
            thelongs=map(string.atof,thelongs)
            coordlist=[]
            for i in range(len(thelongs)):
                coordlist.append((thelongs[i],thelats[i]))
            value=coordlist
        #regular value
        else:
            theString= self.getstring(theName)
            #orbitnumber doesn't have quotes
            if theName=='ORBITNUMBER':
                theMatch=self.orbitObject.match(theString)
                if theMatch:
                    value=theMatch.group('orbit')
                else:
                    raise "couldn't fine ORBITNUMBER"
            #expect quotes around anything else:
            else:
                theMatch=self.stringObject.match(theString)
                if theMatch:
                    value=theMatch.group('value')
                    theDate=self.dateObject.match(value)
                    if theDate:
                        value=theDate.group('date') + " UCT"
                    else:
                        theTime=self.timeObject.match(value)
                        if theTime:
                            value=theTime.group('time') + " UCT"
                else:
                    raise "couldn't parse %s" % (theName,)
        return value

def parseMeta(filename):
    if type(filename) == types.StringType:
        infile = h5py.File(filename,'r')
    elif isinstance(filename,h5py._hl.files.File):
        infile=filename
    else:
        raise IOError, "need an netcdf filename or Dataset instance"
    metaDat=infile.attrs['CoreMetadata.0_GLOSDS']
    altrDat=infile.attrs['ArchiveMetadata.0_GLOSDS']
    # level-2 files stores GRING data in here

    parseIt=metaParse(metaDat,altrDat)
    outDict={}
    outDict['orbit']=parseIt('ORBITNUMBER')
    outDict['filename']=parseIt('LOCALGRANULEID')
    outDict['stopdate']=parseIt('RANGEENDINGDATE')
    outDict['startdate']=parseIt('RANGEBEGINNINGDATE')
    outDict['starttime']=parseIt('RANGEBEGINNINGTIME')
    outDict['stoptime']=parseIt('RANGEENDINGTIME')
    outDict['equatortime']=parseIt('EQUATORCROSSINGTIME')
    outDict['equatordate']=parseIt('EQUATORCROSSINGDATE')
    outDict['nasaProductionDate']=parseIt('PRODUCTIONDATETIME')
    outDict['daynight']=parseIt('DAYNIGHTFLAG')
    corners=parseIt('CORNERS')
    cornerlats=[]
    cornerlons=[]
    for (lon,lat) in corners:
        cornerlats.append(lat)
        cornerlons.append(lon)
    outDict['cornerlats']=np.array(cornerlats)
    outDict['cornerlons']=np.array(cornerlons)
    return outDict

def dorun(filename=None):
    import sys
    if not filename:
        filename=\
         'MOD021KM.A2006275.0440.005.2008107091833.hdf'
    print parseMeta(filename)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('h5_file',type=str,help='name of h5 file')
    args=parser.parse_args()
    dorun(args.h5_file)
    
