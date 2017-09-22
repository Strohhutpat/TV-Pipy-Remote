#!/usr/bin/python3
## TV-Pipy-Remote v0.9 ##

#lines with "#" are for debugging in PyCharm

#import RPi.GPIO as GPIO
import sys
import subprocess
import re
import urllib.request
import xml.dom.minidom as dom
from urllib.error import URLError, HTTPError
import time

## Conf ##
## diverse Fernseher können kein CEC Standby ##
## manche können auch kein CEC (Blaubpunkt White Label Schrott) :D ##
tvoncec = 0
tvoffcec = 0
## fallback Steuerung über die original Remote mit Anschluss an GPIO ##
gpioremoteport = 16

print("TV Steuerung")

#GPIO.setmode(GPIO.BOARD)
#GPIO.setwarnings(False)
#GPIO.setup(gpioremoteport, GPIO.OUT)

def remotebefehl(moduscecon, moduscecoff):
    if moduscecon == 1:
        print("cec_on")
        #output = subprocess.check_output(["/bin/echo 'on 0'", "|", "/usr/bin/cec-client -s -d 1"], stdin = subprocess.PIPE);
    elif moduscecoff == 1:
        print("cec_off")
        #output = subprocess.check_output(["/bin/echo 'standby 0'", "|", "/usr/bin/cec-client -s -d 1"], stdin = subprocess.PIPE);
    else:
        time.sleep(1)
        # GPIO.output(gpioremoteport, 1)
        print("gpio on")
        time.sleep(2)
        # GPIO.output(gpioremoteport, 0)
        print("gpio off")


def befehlanaus(anaus, tvstatus):
    print ("Befehl: ", anaus, "Status: ", tvstatus)
    if anaus is 1 and tvstatus is 0:
        print("tv ist aus, einschalten")
        remotebefehl(tvoncec, 0)
    elif anaus is 0 and tvstatus is 1:
        print("tv ist an, ausschalten")
        remotebefehl(0, tvoffcec)
    else:
        print("es bleibt alles so wie es ist")

def remote(schalter):
    if tvoncec == 1:
        #
        print("cec on")
        # output = subprocess.check_output(["/bin/echo 'pow 0'", "|", "/usr/bin/cec-client -s -d 1", "|", "grep 'power status'"], stdin=subprocess.PIPE);
        # state = output[:18]
        state = 'power status: on'
        print("Status: ", state)
        #
        #powerstatuson = (state == b'power status: on\n')
        powerstatuson = (state == 'power status: on')
        #powerstatusoff = (state == b'power status: stan\n')
        powerstatusoff = (state == 'power status: stan')
    else:
        #
        print("ir on")
        # output = subprocess.check_output(["tvservice", "-s"], stdin=subprocess.PIPE);
        # state = output[:14]
        state = "state 0x40001 "
        print("Status: ", state)
        #
        #powerstatuson = (state == b'state 0x12001a' or state == b'state 0x12000a')
        powerstatuson = (state == 'state 0x12001a' or state == 'state 0x12000a')
        #powerstatusoff = (state == b'state 0x120009' or state == b'state 0x40001 ')
        powerstatusoff = (state == 'state 0x120009' or state == 'state 0x40001 ')
    if tvoffcec == 1:
        print("cec off")
    else:
        print("ir off")

    print("pruefen")

    if powerstatusoff:
        #tv ist aus
        status = 0
        befehlanaus(schalter,status)
        #if tvoncec is not 1 and state == b'state 0x40001 ':
        if tvoncec is not 1 and state == 'state 0x40001 ':
            print("tv ist jetzt an, falscher status")
            time.sleep(5)
            #subprocess.check_output(["/sbin/reboot"], stdin=subprocess.PIPE);
    elif powerstatuson:
        # tv ist an
        status = 1
        befehlanaus(schalter,status)
    #elif state == b'state 0x40002 ':
    elif state == 'state 0x40002 ':
        print("tv ist an, falscher status")
        #subprocess.check_output(["/sbin/reboot"], stdin=subprocess.PIPE);
    else:
        print("?")

while True:
    uhrzeit = time.strftime("%H:%M")
    print(uhrzeit)
    try:
        response = urllib.request.urlopen('http://intranet/rap/quickview.php')
    except HTTPError as e:
        # do something
        print('Error code: ', e.code)
        time.sleep(10)
    except URLError as e:
        # do something
        print('Reason: ', e.reason)
        time.sleep(10)
    else:
        tree = dom.parse(response)

        for eintrag in tree.firstChild.childNodes:
            if eintrag.nodeName == "Uhrzeit":
                for knoten in eintrag.childNodes:
                    if knoten.nodeName == "Von":
                        uhrzeitvon = knoten.firstChild.data.strip()
                    elif knoten.nodeName == "Bis":
                        uhrzeitbis = knoten.firstChild.data.strip()
            elif eintrag.nodeName == "Werte":
                for knoten in eintrag.childNodes:
                    if knoten.nodeName == "Ort":
                        print ("Ort: " + knoten.firstChild.data.strip())
                        if knoten.firstChild.data.strip() == "error":
                            print("Achtung kein Ort")
                            sys.exit()
                        else:
                            print("")
                    elif knoten.nodeName == "Anzahl":
                        print ("Anzahl: " + knoten.firstChild.data.strip())
                        anzahl = knoten.firstChild.data.strip()
                    elif knoten.nodeName == "WTag":
                        wtag = knoten.firstChild.data.strip()
                        if wtag is not "6" and wtag is not "7":
                            print ("Woche")
                            woche = "1"
                        else:
                            print ("WE")
                            woche = "0"
                    elif knoten.nodeName == "Datum":
                        print ("Datum: " + knoten.firstChild.data.strip())
        #uhrzeit
        if uhrzeit >= uhrzeitvon and uhrzeit <= uhrzeitbis:
            #einschalten von bis
            #zusammenführung
            if woche is "1" or anzahl >= "1":
                print ("Monitor von: ", uhrzeitvon, " bis ", uhrzeitbis, " einschalten!")
                remote(1)
            elif woche == "0":
                print ("nichts los, aus!")#do
                remote(0)
        else:
            print("nichts los, aus!")  # do
            remote(0)

        break #debug
        #prüfen aller 10min
        #time.sleep(6)

