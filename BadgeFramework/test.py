from __future__ import division, absolute_import, print_function
import logging
import sys
import threading
import time

from badge import *
from ble_badge_connection import *
from bluepy import *
from bluepy import btle
from bluepy.btle import UUID, Peripheral, DefaultDelegate, AssignedNumbers ,Scanner
from bluepy.btle import BTLEException


def main():
	device_addr = sys.argv[1]
	print("#####################################")
	print("# Connecting to ", device_addr, " # ")
	connection = BLEBadgeConnection.get_connection_to_badge(device_addr)

	if not connection:
		print("# Could not find badge              #")
		return

	connection.connect()
	badge = OpenBadge(connection)

	print("# connetced                         #")

	for reps in 1, 2:


		time.sleep(0.5)
        print("#####################################")
        print("# Midge test                        #")
        print("# sensor: mic, stereo mode          #")
        print("#-----------------------------------#")

        start_stereo = badge.start_microphone(t=None,mode=0) # start mic in stereo mode

        # check if mic was started in stereo mode
        if (start_stereo.mode==0):
            print("# mic mode:         PASS            #")
            if (start_stereo.pdm_freq == 100 or start_stereo.pdm_freq == 132 or start_stereo.pdm_freq == 167):
                print("# mic freq:         PASS            #")
            else:
                print("# mic freq:         FAIL            #")

            if (start_stereo.gain_l != 0 and start_stereo.gain_r != 0):
                print("# mic gain:         PASS            #")
            else:
                print("# mic gain:         FAIL            #")               
        else:
			print("# mic mode:         FAIL             #")

        time.sleep(5) # reecording time

        mic = badge.get_status()
        # check if mic was enabled 
        if (mic.microphone_status):
			print("# mic enabled:      PASS            #")
        else:
            print("# mic enabled:      FAIL            #")

        badge.stop_microphone() # stop recording
	
        time.sleep(0.5)

        mic = badge.get_status()
        # check if mic was disabled with success
        if (~mic.microphone_status):
            print("# mic disabled:     PASS            #")
        else:
            print("# mic disabled:     PASS            #")

        

        print("#####################################")
        print("# sensor: mic, mono mode            #")
        print("#-----------------------------------#")

        start_mono = badge.start_microphone(t=None,mode=1)

        if (start_mono.mode==1):
            print("# mic mode:         PASS            #")
            if (start_mono.pdm_freq == 100 or start_mono.pdm_freq == 132 or start_mono.pdm_freq == 167):
                print("# mic freq:         PASS            #")
            else:
                print("# mic freq:         FAIL            #")

            if (start_mono.gain_l != 0 and start_mono.gain_r != 0):
                print("# mic gain:         PASS            #")
            else:
                print("# mic gain:         FAIL            #")                
            
        else:
			print("# mic mode:         FAIL            #")

        time.sleep(5) # reecording time

        mic = badge.get_status()
        # check if mic was enabled 
        if (mic.microphone_status):
			print("# mic enabled:      PASS            #")
        else:
            print("# mic enabled:      FAIL            #")

        badge.stop_microphone() # stop recording
	
        time.sleep(0.5)

        mic = badge.get_status()
        # check if mic was disabled with success
        if (~mic.microphone_status):
            print("# mic disabled:     PASS            #")
        else:
            print("# mic disabled:     PASS            #")

        print("#####################################")
        print("# sensor: scan                      #")
        print("#-----------------------------------#")

        badge.start_scan(window_ms = 250, interval_ms = 1000) ## start scan with default parameters
        time.sleep(5) # scan enabled time  

        scan = badge.get_status()
        # check if scan was enabled succesfully
        if (scan.scan_status):
            print("# scan enabled:     PASS            #")
        else:
            print("# scan enabled:     FAIL            #")
        # check if scan was sending data (must have another badge near to pass)
        if (scan.scan_data != 0):
			print("# scan data:        PASS            #")            
        else:
			print("# scan data:        FAIL            #")
	    
        badge.stop_scan() # stop scan

        time.sleep(0.5) # safety wait

        scan = badge.get_status() # get scan status
        # check if scan was disabled succesfully
        if (~scan.scan_status):
			print("# scan disabled:    PASS            #")		
        else:
			print("# scan disabled:    FAIL            #")
        
	    
        print("#####################################")
        print("# sensor: imu                       #")
        print("#-----------------------------------#")
	
        imu_start = badge.start_imu() # start imu
        time.sleep(0.1) # safety wait 
        #check if imu self test was done
        if (imu_start.self_test_done):
            print("# imu self test:    PASS            #")
        else:
            print("# imu self test:    FAIL            #")

        imu = badge.get_status() # get imu status
        time.sleep(0.1) # safety wait 
        imu_data = badge.get_imu_data() # get imu data

        #print(imu_data)
        
        # check if imu sensors are sending data 
        if (imu.imu_status):
            print("# imu enabled:      PASS            #")
            if (~(imu_data.acc_x == 0 and imu_data.acc_y  == 0 and imu_data.acc_z  == 0)):
                print("# imu acc:          PASS            #")
            else:
                print("# imu acc:          FAIL            #")
            if (~(imu_data.mag_x == 0 and imu_data.mag_y  == 0 and imu_data.mag_z  == 0)):
                print("# imu mag:          PASS            #")
            else:
                print("# imu mag:          FAIL            #")
            if (~(imu_data.gyr_x == 0 and imu_data.gyr_y  == 0 and imu_data.gyr_z  == 0)):
                print("# imu gyr:          PASS            #")
            else:
                print("# imu gyr:          FAIL            #")
            if (~(imu_data.rot_x == 0 and imu_data.rot_y  == 0 and imu_data.rot_z  == 0)):
                print("# imu rot:          PASS            #")
            else:
                print("# imu rot:          FAIL            #")

        else:
			print("# imu enabled:      FAIL            #")

        
        time.sleep(5) # imu enabled time
        badge.stop_imu()
        time.sleep(0.5) # safety wait

        imu = badge.get_status()

        if (~imu.imu_status):
			print("# imu disabled:     PASS            #")
			print("#####################################")
        else:
			print("# imu disabled:     FAIL            #")
			print("#####################################")

        errased = badge.sdc_errase_all() # clean sd memory

        if (errased.done_errase):
            print("# memory cleaned:   PASS            #")
            print("#####################################")
        else:
            print("# memory cleaned:   FAIL            #")
            print("#####################################")
        
        connection.disconnect()

if __name__ == "__main__":
	main()