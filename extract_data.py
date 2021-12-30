# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 10:47:30 2021

@author: jnwag
"""
import os
import gzip
import shutil
import fnmatch
topDir = r"C:\Users\jnwag\OneDrive\Documents\project data"

def gunzip(file_path,output_path):
    with gzip.open(file_path,"rb") as f_in, open(output_path,"wb") as f_out:
        shutil.copyfileobj(f_in,f_out)
        
def recurse_and_gunzip(root):
    walker = os.walk(root)
    for root,dirs,files in walker:
        for f in files:
            file_to_open = root+ "\\" + f
            if fnmatch.fnmatch(f,"*.gz"):
                gunzip(file_to_open,file_to_open.replace(".gz",""))
                
                
recurse_and_gunzip(topDir)

