def output_h5(level1b_file,geom_file,output_name):
     """
        input:  two input filenames or h5py.File objects
          level1b_file
          geom_file
        that contain the
        level1b radiances and reflectivities from Laadsweb and the
        full pixel latitude and longitudes
        and one filename:
           outpout_name
        that is the name of the file to write the subsetted data to.
        output:  side effect -- writes an output file with new datasets
          chan1, chan31, latitude, longitude and metadata
      """
### **Writing Modis data to an hdf5 file**

# I want to consolidate channel 1, channel 31, the lats and the lons in a smaller file
# so that I don't have to store all 147 Mbytes of the original L1B file.  In this notebook I'll write out a
# new h5 file following the h5py quick start tutorial: http://docs.h5py.org/en/latest/quick.html.  To do this, I'll start from
# [the satelliteI_h5 notebook](http://nbviewer.ipython.org/github/a301-teaching/classcode/blob/master/notebooks/satelliteI_h5.ipynb) and add a file writing section.

# ## ***Step 1 read and scale the radiances***

# In[33]:

from __future__ import print_function
from IPython import get_ipython
ipython_shell = get_ipython()
import os,site
import glob
import h5py
#
# add the lib folder to the path assuming it is on the same
# level as the notebooks folder
#
libdir=os.path.abspath('C:/GitHub/classcode/lib')
site.addsitedir(libdir)
from modismeta_h5 import parseMeta
from h5dump import dumph5


# the glob function finds a file using a wildcard to save typing (google: python glob wildcard)

# In[34]:

l1b_filename=glob.glob('C:/GitHub/classcode/lib/MOD021KM.A2005199.0215.005.2010155072656.h5')[0]
print("found l1b file {}".format(l1b_filename))
geom_filename=glob.glob('C:/GitHub/classcode/lib/MOD03.A2005199.0215.005.2010154180154.h5')[0]
print("found geom file {}".format(geom_filename))


# In[35]:

l1b_file=h5py.File(l1b_filename)
geom_file=h5py.File(geom_filename)


# **Read the channel 31 radiance data from MODIS_SWATH_Type_L1B/Data Fields/EV_1KM_Emissive**

# In[36]:

print(l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['Band_1KM_Emissive'].shape)
print(l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['Band_1KM_Emissive'][...])
print(l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].shape)


# **note that channel 31 occurs at index value 10**

# In[37]:

index31=10


# **the data is stored as unsigned, 2 byte integers which can hold values from 0 to $2^{16}$ - 1 = 65,535 **

# In[38]:

chan31=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'][index31,:,:]
print(chan31.shape,chan31.dtype)


# In[39]:

chan31[:3,:3]


# ** we need to apply a
# scale and offset to convert to radiance (the netcdf module did this for us automatically**

# $Data = (RawData - offset) \times scale$
# 
# this information is included in the attributes of each variable.
# 
# (see page 36 of the [Modis users guide](http://clouds.eos.ubc.ca/~phil/courses/atsc301/text/modis_users_guide.pdf) )

# In[40]:

scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_scales'][index31]
offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_1KM_Emissive'].attrs['radiance_offsets'][index31]


# In[41]:

chan31=(chan31 - offset)*scale


# In[42]:

get_ipython().magic(u'matplotlib inline')


# **histogram the calibrated radiances and show that they lie between
# 0-10 $W\,m^{-2}\,\mu m^{-1}\,sr^{-1}$ **

# In[43]:

import matplotlib.pyplot as plt
out=plt.hist(chan31.flat)


# **Now do the same for Channel 1**

# From [the Modis users guide](http://clouds.eos.ubc.ca/~phil/courses/atsc301/text/modis_users_guide.pdf) (p. 25, table 3.3.2), we know that the 1 km version of channel 1 is called EV_250_Aggr1km_RefSB and is at index 0, so just get that channel, scale and offset for index 0

# In[44]:

reflective=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_250_Aggr1km_RefSB'][0,:,:]


# In[45]:

scale=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_250_Aggr1km_RefSB'].attrs['radiance_scales']
offset=l1b_file['MODIS_SWATH_Type_L1B']['Data Fields']['EV_250_Aggr1km_RefSB'].attrs['radiance_offsets']
chan1=(reflective - offset[0])*scale[0]


# not sure why these reflectivities are not scaled properly -- can be greater than 1, but shouldn't be this high?

# In[46]:

out=plt.hist(chan1.flat)


# ## **Read MODIS_SWATH_Type_L1B/Geolocation Fields/Longitude**

# In[47]:

the_lon=geom_file['MODIS_Swath_Type_GEO']['Geolocation Fields']['Longitude'][...]
the_lat=geom_file['MODIS_Swath_Type_GEO']['Geolocation Fields']['Latitude'][...]


# # ***Now write these four fields out to a new hdf file***

# In[48]:

out_name="swath_output.h5"
try:
    f.close()
except ValueError:
    pass
f = h5py.File(out_name, "w")
dset = f.create_dataset("lattitude", the_lat.shape, dtype=the_lat.dtype)
dset[...]=the_lat[...]
dset = f.create_dataset("longitude", the_lon.shape, dtype=the_lon.dtype)
dset[...]=the_lon[...]
dset = f.create_dataset("channel1", chan1.shape, dtype=chan1.dtype)
dset[...]=chan1[...]
dset = f.create_dataset("channel31", chan31.shape, dtype=chan31.dtype)
dset[...]=chan31[...]


# ## **Read the metadata from the Level1b file**

# In[ ]:

metadata=parseMeta(l1b_file)
metadata


# **Transfer all the metadata to the new hdf5 file as global attributes**

# In[ ]:

for the_key in metadata.keys():
    f.attrs[the_key]=metadata[the_key]


# In[ ]:

f.close()


# **Now reopen the output file and dump it to make sure it has all our stuff**

# In[ ]:

f=h5py.File(out_name,'r')
dumph5(f)
f.close()

if __name__ == "__main__":
    l1b_file="MYD021....."
    geom_file="MYD03....."
    output_file='test_output.h5'
    output_h5(l1b_file,geom_file,output_file)

