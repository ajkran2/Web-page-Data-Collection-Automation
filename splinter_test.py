# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 19:23:18 2017

@author: Ashton
"""
"""
Need to install: selenium (from cmd/terminal: pip install selenium)
Also need to install: chromedriver (see link from error when trying to run line 18)

.csv file of all sensor readings will be downloaded in default directory
( ..\Downloads\ on my Windows machine )
"""

def download_all_omnisense():
    
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.chrome.options import Options
    import os
    import numpy as np
    import datetime as date
    import time
    
    #    options = webdriver.ChromeOptions()
#    options.add_argument("download.default_directory="+os.getcwd())
    # EDIT PATH TO BE YOUR CHROMEDRIVER PATH
    driver = webdriver.Chrome('C:\\Users\Ashton\Downloads\chromedriver_win32\chromedriver.exe')
    
    driver.get('https://www.omnisense.com/user_login.asp')
    
    login = driver.find_element_by_name("userId")
    password = driver.find_element_by_name("userPass")
    
    login.send_keys("AKrajnovich")
    password.send_keys("Mines254178")
    password.send_keys(Keys.RETURN)
    
    # Navigate to downloads screen
    downloads = driver.find_element_by_link_text('Downloads')
    downloads.click()
    main_window = driver.current_window_handle # For returning for new sensors
    
    # Select date range (Past 24 hrs)
    dates = driver.find_element_by_name('dnldFrDate')
    date = date.datetime.strftime(date.datetime.now()-date.timedelta(1) ,'%m/%d/%Y')
    datepass = date.replace('/','_')
    dates.send_keys(Keys.CONTROL+'a')
    dates.send_keys(Keys.DELETE)
    dates.send_keys(date)
   
    # Select hourly averaging
    select = Select(driver.find_element_by_name('averaging'))
    select.select_by_value('H')
    
    # Loop thru all Sensor IDs...
    sensors = Select(driver.find_element_by_name('sensorId'))
    allsensors = sensors.options
    for i in range(1,len(allsensors)-1):
        sensors.select_by_index(i)
        sensor = sensors.first_selected_option.text
        sensor = sensor.replace(' ', '')
        sensor = sensor.replace(':', '')
        # Activate download prep(default download all data)    
        download = driver.find_element_by_name("btnAct")
        # Open in new tab
        download.send_keys(Keys.CONTROL+Keys.RETURN)
        #driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
        time.sleep(1)
        driver.switch_to_window(driver.window_handles[1])
        
        time.sleep(5)
        
        # Act on download button 
        dl = driver.find_element_by_id("downloadbutton")
        dl.click()   
        time.sleep(5)
        
        # Close current tab
        driver.close()
        #driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
        driver.switch_to_window(main_window)
        
        # Read and collect data for current sensor
        array = read_all_omnisense(sensor,datepass)
#        if array == []:
#            continue
#        else:
#            nparray = np.array(array)
#            nparray = np.transpose(nparray)
            
            # Write data for current sensor to a file
#            curr_file = os.getcwd()+'\\DATA'+sensor+'.txt'
#            with open(curr_file,'w') as f:
#                for j in range(len(nparray[:])):
#                    for i in range(len(nparray[0])):          
#                        f.write(nparray[j][i] + ' ')
#                    f.write('\n')
            
            
    # Close master window
    driver.quit()
    
    #
    #driver.quit()
    
def read_all_omnisense(sensor,datepass):
    import numpy as np
    import os
    import glob
    
    # Scan files in W.D. and get most recently modified (ie. new downloaded data)
    files = glob.glob('C:\\Users\Ashton\Downloads\*')
    latest = max(files, key=os.path.getctime)
    filename = os.getcwd()+'\\C12_'+datepass+'\\DATA'+sensor+'.txt'
        
    
    # Overwrite file with no commas and save to WD
    read = latest
    with open(read, 'r') as f:
        nocommas = f.read()
    f.close()
    
    nocommas = nocommas.replace(',',' ')
    with open(read, 'w') as f:
        f.write(nocommas)
    f.close()
    
    with open(read) as f: 
        for x in range(3):
            next(f)
        array = [[x for x in line.split(' ')] for line in f]
    nparray = np.array(array) 
    f.close()
    length = int(len(nparray))
    #nparray = nparray.reshape((length,10))
    
    if array == []:
        return(array)
    else:
        with open(filename,'w') as f:
            for j in range(len(array)):
                for i in range(len(array[0])):          
                    f.write(array[j][i] + ' ')
                f.write('\n')
        return(array)
        
        #return(sensorId,port,read_date,temperature_f,humidity,gpp,dew_point_f,wood_pct,t_diff_f,battery_voltage)
        
        
download_all_omnisense()