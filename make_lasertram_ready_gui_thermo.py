
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 15:19:09 2021

@author: jordanlubbers

This script will take a folder of .csv files from the Qtegra software 
associated with a ThermoFisher iCAP RQ ICP-MS, strip the metadata at the top,
and place all of the raw counts per second data in one spreadsheet with a 
column that denotes the individual sample that each row (e.g., cycle through
the mass range) belongs to.

It uses tkinter to do this in the form of a GUI where the user only has to 
input the name of the output file in the text input area, press the button,
and go find their folder with all the individual, raw .csv files. 


This works well as an imported module where one can do something like this:

import make_lasertram_ready_gui_thermo as ltg

ltg.make_lasertram_ready()

^^this will run the script and open the tkinter dialog window and only needs
to be done once. 


"""

import pandas as pd
import glob as glob
import os
import numpy as np
from tkinter import filedialog
import tkinter as tk
from dateutil.parser import parse

myfont = 'Calibri'
def make_lasertram_ready():
    root = tk.Tk()
    root.title('Make data LaserTRAM ready!')
    
    canvas1 = tk.Canvas(root, width = 400, height = 200, relief = 'raised')
    
    canvas1.pack()
    
    
    filename_entry = tk.Entry(root, width = 30, font = myfont)
    filename_entry.insert(0,"Name your file here!")
    filename_label = tk.Label(root, text = 'Filename: ', font = myfont)
    
    
    canvas1.create_window(200,40, window = filename_entry)
    canvas1.create_window(200, 10, window = filename_label)
   
    
    def preprocess_data():
        
        filename = filename_entry.get()
    
        folder_selected = filedialog.askdirectory()
        
        
        #the filepath of the folder with the proper tail to grab all the .csv files from it
        #using glob
        files_in_folder = folder_selected 
        
        
            
        def make_LTspot_ready(file):
            
            #import data
            #remove the top rows. Double check that your header is the specified 
            #amount of rows to be skipped in 'skiprows' argument
            data = pd.read_csv(file,
                               skiprows = 13
        )
            #drop empty column at the end
            data.drop(data.columns[len(data.columns)-1], axis=1, inplace=True)
            
            #remove dwell time row beneath header row
            LT_ready = data.dropna()
            
            return LT_ready
        
        
        def make_LTspot_file(inpath,name):
            
            #all of your file paths from that folder as a list
            infiles = glob.glob('{}/*.csv'.format(inpath))
        
            #finds the sample name in cell A1 in your csv file and saves it 
            #to a list
            samples = []
            timestamps = []
            for i in range(0,len(infiles)):
                #gets the top row in your csv and turns it into a pandas series
                top = pd.read_csv(infiles[i],nrows = 0 )
        
                #since it is only 1 long it is also the column name
                #extract that as a list
                sample = list(top.columns)
        
                #turn that list value to a string
                sample = str(sample[0])
        
        
                #because its a string it can be split
                #split at : removes the time stamp 
                sample = sample.split(':')[0]
        
                #.strip() removes leading and trailing spaces
                sample = sample.strip()
        
        
        
                #replace middle spaces with _ because spaces are bad
                nospace = sample.replace(" ","_")
        
                #append to list
                samples.append(nospace)
        
                #get the timestamp by splitting the string by the previously
                #designated sample. Also drops the colon in front of the date
                timestamp = top.columns.tolist()[0].split(sample)[1:][0][1:]
        
                #use dateutil.parser function 'parse' to turn that string into 
                #a useable date
                timestamps.append(parse(timestamp))
        
        
            # go through and make a list of lists for each file that has its metadata
            # in the form [timestamp,samplename,filepath]
            metadata = []
            for sample,file,timestamp in zip(samples,infiles,timestamps):
                metadata.append([timestamp,sample,file])
        
            #because the timestamp is first we can now sort this list by time
            #put the ordered samplenames and filepaths in their own list
            ordered_samples = []
            ordered_files = []
            for data in sorted(metadata):
                ordered_samples.append(data[1])
                ordered_files.append(data[2])
        
            #now when you strap them together to prep for LaserTRAM spot analyses, things will be 
            #in the correct order
        
           
            suffix = 'LT_ready.xlsx'
            # outpath = os.path.dirname(infiles[0]) + '/' + name + '_' + suffix
            outpath = '{}\{}_{}'.format(os.path.dirname(infiles[0]),name,suffix)
        
            #concatenate all your data
        
            #concatenate all your data
            all_data = pd.DataFrame()
            for file,sample in zip(ordered_files,ordered_samples):
        
                sample_data = make_LTspot_ready(file)
                #insert a column with the header 'sample' and sample name in every row
                sample_data.insert(0,'SampleLabel',sample)
                #add blank row at the end
                sample_data.loc[sample_data.iloc[-1].name + 1,:] = np.nan
        
                #append current iteration
                all_data = all_data.append(sample_data)
        
            #change time units from seconds to milliseconds
            all_data['Time'] = all_data['Time'].multiply(other = 1000)
        
            #blank dataframe for the blank sheet that is required
            df_blank = pd.DataFrame()
        
            # Create a Pandas Excel writer using XlsxWriter as the engine.
            #{'strings_to_numbers': True} remvoes 'numbers saved as text error in excel'
            writer = pd.ExcelWriter(outpath, engine='xlsxwriter',options = {'strings_to_numbers': True})
        
            # Convert the dataframe to an XlsxWriter Excel object.
            all_data.to_excel(writer, sheet_name='Buffer',index = False)
            df_blank.to_excel(writer,sheet_name = 'Sheet1',index = False)
        
            #access XlsxWriter objects from the dataframe writer object
            workbook  = writer.book
            buffer = writer.sheets['Buffer']
            sheet1 = writer.sheets['Sheet1']
            #Close the Pandas Excel writer and output the Excel file.
            writer.save() 
            
            filepath_label = tk.Label(root, text =  "Success!! the following was saved in the same folder as the raw data:",
                                      wraplength = 175,
                                      font = myfont,
                                      
                                      )
            canvas1.create_window(200,140, window = filepath_label,)
            
            filepath_label2 = tk.Label(root, text = '{}{}'.format(filename_entry.get(),suffix),
                                       fg = 'red',
                                       font = '{} 12 bold'.format(myfont)
                                       )
            canvas1.create_window(200,180, window = filepath_label2)
    
            
        make_LTspot_file(files_in_folder,filename)
            
            
            
            
    
    process_button = tk.Button(text = 'preprocess data', command = preprocess_data, height = 2,fg = 'green',font =  '{} 12 bold'.format(myfont))
    
    canvas1.create_window(200, 80, window = process_button)
    
    
    
    canvas1.pack()
    
    root.mainloop()



