# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 11:38:20 2022

@author: jlubbers
"""

import make_lasertram_ready_gui_agilent as ltga
import make_lasertram_ready_gui_thermo as ltgt


#choose your mass spec brand here!
brand = 'agilent'

if brand == 'thermo':
    ltgt.make_lasertram_ready()
    
elif brand == 'agilent':
    ltga.make_lasertram_ready()
    