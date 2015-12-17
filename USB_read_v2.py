#!/usr/bin/env python
#
# Code by Carlos A Capriotti - 
# Play fair and mention the author name if you use this code somehow.
# 
#
#
# This code is supposed to run from a Mac, logging the readings 
# from an Arduino with specific devices attached.
#
# This code is only half of the solution; 
# the listener and logger. 
# 
#
# On the Arduino side, sensors will 
# measure Electrical micro power
# generation by wind, static solar panels and
# solar tracking panels (single or dual axe) 
#
# This part of the software also implements a simple protocol communication.
#


import io
import re
import serial
import time
import datetime
import os

from serial import Serial
from datetime import date, datetime


usbport = '/dev/tty.usbserial-A40167GP'
usbspeed = 115200
usbtimeout = 1
buffersize = 512
charcount = 0
endofcomm = ['[CommBlockEnd]','[CommBlockData]','[CommBlockInfo]','[CommBlockOFF]']

wspeed = ''		# Wind Speed
motorv = ''		# Generated volts on motor
tempse = ''		# Exterior temperature
fixpv  = ''		# Volts from fixed solar panel
pivpv  = ''		# pivotal angle of tracking panel
eventl = ''		# Event bein logged
ser = ''
maxlogsize = 50000
flushtimer = 60
timer = 0

filename_ts = ''
log_size = [0,0,0,0,0,0]



def timestamp():
   return datetime.now().strftime('%Y-%m-%d-%H.%M') + '.txt'
	# log files are named according the time stamp

def read_ser():
    global wspeed
    global motorv
    global tempse
    global fixpv
    global pivpv
    global eventl
    usbbuffer = ''  
    last_received = ser.readline()
       
    if (last_received.strip() == endofcomm[1]):
        for count in range(5):
            last_received = datetime.now().strftime('%Y-%m-%d,%H:%M:%S,') + ser.readline()
            if count == 0:
	           wspeed.write(last_received)
			   log_size[count] = log_size[count] + len(last_received)
                if log_size[count] > maxlogsize:
                    wspeed.close()
                    filename_ts = timestamp()
                    wspeed = open('log_wspeed_'+filename_ts, 'w')
                    log_size[count] = 0
                    
            elif count == 1:
                motorv.write(last_received)
				log_size[count] = log_size[count] + len(last_received)
                if log_size[count] > maxlogsize:
                    motorv.close()
                    filename_ts = timestamp()
                    motorv = open('log_motorv_'+filename_ts, 'w')
                    log_size[count] = 0
                    
            elif count == 2:
                tempse.write(last_received)
				log_size[count] = log_size[count] + len(last_received)
                if log_size[count] > maxlogsize:
                    tempse.close()
                    filename_ts = timestamp()
                    tempse = open('log_tempse_'+filename_ts, 'w')
                    log_size[count] = 0
                    
            elif count == 3:
                fixpv.write(last_received)
				log_size[count] = log_size[count] + len(last_received)
                if log_size[count] > maxlogsize:
                    fixpv.close()
                    filename_ts = timestamp()
                    fixpv = open('log_fixpv__'+filename_ts, 'w')
                    log_size[count] = 0
                    
            elif count == 4:
                pivpv.write(last_received)
				log_size[count] = log_size[count] + len(last_received)
                if log_size[count] > maxlogsize:
                    pivpv.close()
                    filename_ts = timestamp()
                    pivpv = open('log_pivpv__'+filename_ts, 'w')
                    log_size[count] = 0
            
            
    elif (last_received.strip() == endofcomm[2]):
        last_received = datetime.now().strftime('%Y-%m-%d-%H:%M:%S') + ',' + ser.readline()
        eventl.write(last_received)
        log_size[5] = log_size[5] + len(last_received)
        if log_size[5] > maxlogsize:
           eventl.close()
           filename_ts = timestamp()
           eventl = open('log_eventl_'+filename_ts, 'w')
           log_size[5] = 0
        last_received = ''   
    elif (last_received.strip() == endofcomm[3]):
        eventl.write(datetime.now().strftime('%Y-%m-%d-%H:%M:%S') + ',Arduino,Info,Arduino requested a shutdown of the host application')
        return False # Arduino requested host shutdown.
        

    return True



if __name__ ==  '__main__':

   ser = serial.Serial('/dev/tty.usbserial-A40167GP',115200,timeout=1)
   filename_ts = timestamp() 
   
   wspeed = open('log_wspeed_'+filename_ts, 'w')
   motorv = open('log_motorv_'+filename_ts, 'w')
   tempse = open('log_tempse_'+filename_ts, 'w')
   fixpv  = open('log_fixpv__'+filename_ts, 'w')
   pivpv  = open('log_pivpv__'+filename_ts, 'w')
   eventl = open('log_eventl_'+filename_ts, 'w')
   
   os.system('clear')
   print 'Monitoring the Arduino USB'
   last_minute = int(datetime.now().strftime('%M'))
   while read_ser():
      
      if int(datetime.now().strftime('%M')) != last_minute:
         #print (last_minute == int(datetime.now().strftime('%M')) )
         last_minute = int(datetime.now().strftime('%M'))
         wspeed.flush()
         motorv.flush()
         tempse.flush()
         fixpv.flush()
         pivpv.flush()
         eventl.flush()
         os.fsync(wspeed.fileno())
         os.fsync(motorv.fileno())
         os.fsync(tempse.fileno())
         os.fsync(fixpv.fileno())
         os.fsync(pivpv.fileno())
         os.fsync(eventl.fileno())
      
      
   wspeed.close()
   motorv.close()
   tempse.close()
   fixpv.close()
   pivpv.close()
   eventl.close()




