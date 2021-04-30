#!/usr/bin/python3
import socket
import pywemo
import datetime
import logging
import logging.handlers

LOGFILE='/opt/wemo_modem/log_wemo/logwemo.log'

#Setup logger
logger = logging.getLogger('WemoLogger')
logger.setLevel(logging.INFO)

#Setup format
format =  logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#Setup handler
handler = logging.handlers.RotatingFileHandler(LOGFILE, maxBytes=1000000, backupCount=5)
handler.setLevel(logging.INFO)
handler.setFormatter(format)

logger.addHandler(handler)


def internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        logger.info("Connecting to: {0}".format(host))
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        logger.info("Connection success!!!")
        return True
    except socket.error as ex:
        logger.info('Connection failed: {0}'.format(ex))
        return False

def wemo_switch(MODEM="Modem Howe"):
    devices = pywemo.discover_devices()
    logger.info('Discovered Devices: {0}'.format(devices))

    #reset bit
    reset=0
    for d in devices:
        #Test for Modem Device
        if d.name==MODEM:
            logger.info('{0} FOUND'.format(MODEM))
            if d.get_state==1:
                logger.info('Turning {0} off.'.format(MODEM))
                d.off()
                time.sleep(10)
                logger.info('Turning {0} on.'.format(MODEM))
                d.on()
            else:
                logger.info('{0} was found to be offline...turning on.'.format(MODEM))
                d.on()

            #reset performed, flip bit
            reset=1

    if reset==0:
        logger.info('{0} NOT FOUND - RESET NOT PERFORMED'.format(MODEM))

logger.info("Script started...")

#Counter
i=0

#Test for internet connectivity
while not internet():
    i+=1
    logger.info("No internet...retrying in 60 seconds.")
    time.sleep(60)

    if i>=10:
        logger.info("Initiating Wemo connection.")
        wemo_switch()

logger.info("Script shutting down....")
