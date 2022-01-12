#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 15:19:09 2021

@author: jordanlubbers

This script will take a folder of .csv files from the an Agilent 8900 QQQ, 
strip the metadata at the top, and place all of the raw counts per second data 
in one spreadsheet with a column that denotes the individual sample that each 
row (e.g., cycle throughthe mass range) belongs to.

It uses tkinter to do this in the form of a GUI where the user only has to 
input the name of the output file in the text input area, press the button,
and go find their folder with all the individual, raw .csv files. 


This works well as an imported module where one can do something like this:

import make_lasertram_ready_gui_agilent as ltg

ltg.make_lasertram_ready()

^^this will run the script and open the tkinter dialog window and only needs
to be done once. 


"""

import pandas as pd
import glob as glob
import os
from tkinter import filedialog
import tkinter as tk
from dateutil.parser import parse
import re

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
        
        
            
        def extract_metadata(file):
            # import data
            # extract sample name
            # extract timestamp
            # extract data and make headers ready for lasertram
            
            df = pd.read_csv(file, sep = '\t', header = None)
            
            sample = df.iloc[0,0].split('\\')[-1].split('.')[0].replace('_','-')
            
            timestamp = parse(df.iloc[2,0].split(' ')[7] + ' ' + df.iloc[2,0].split(' ')[8])
            
            data = pd.DataFrame([sub.split(",") for sub in df.iloc[3:-1,0]])
            
            header = data.iloc[0,:]
            data = data[1:]
            data.columns = header
            newcols = []
            for s in data.columns.tolist():
                l = re.findall('(\d+|[A-Za-z]+)', s)
                if 'Time' in l:
                    newcols.append(l[0])
                else:

                    newcols.append(l[1]+l[0])
            data.columns = newcols
            
            return [timestamp, file, sample, data]

        def make_LTspot_ready_cooper(inpath, name):
            
            infiles = glob.glob('{}/*.csv'.format(inpath))

            metadata = []

            for file in infiles:
                # file, timestamp, sample, data
                metadata.append(extract_metadata(file))
                
            # sort the metadata by timestamp
            # take sorted metadata make dataframe with SampleLabel column and 
            # append to blank all_data dataframe to make one large dataframe
            # with properly ordered data


            all_data = pd.DataFrame()
            suffix = 'LT_ready.xlsx'
            # outpath = os.path.dirname(infiles[0]) + '/' + name + '_' + suffix
            outpath = '{}\{}_{}'.format(os.path.dirname(infiles[0]),name,suffix)


            for data in sorted(metadata):

                sample_data = data[3]
                sample_data.insert(0,'SampleLabel',data[2])
                sample_data.insert(0,'timestamp',data[0])



                all_data = all_data.append(sample_data)
            
            all_data['Time'] = all_data['Time'].astype('float64')*1000
                
                
            #blank dataframe for the blank sheet that is required
            df_blank = pd.DataFrame()

            # Create a Pandas Excel writer using XlsxWriter as the engine.
            #{'strings_to_numbers': True} remvoes 'numbers saved as text error in excel'
            writer = pd.ExcelWriter(outpath, engine='xlsxwriter',
            engine_kwargs={'options': {'strings_to_numbers': True}}
            )

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
    
            
        make_LTspot_ready_cooper(files_in_folder,filename)
            
            
            
            
    
    process_button = tk.Button(text = 'preprocess data', command = preprocess_data, height = 2,fg = 'green',font =  '{} 12 bold'.format(myfont))
    
    canvas1.create_window(200, 80, window = process_button)
    
    
    
    canvas1.pack()
    
    root.mainloop()





