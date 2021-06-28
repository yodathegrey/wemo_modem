#!/usr/bin/python3
import socket
import pywemo
import datetime
import logging
import logging.handlers
import time

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

    #TESTING PURPOSES - uncomment line below
    #host="6.6.6.7"

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

            try:
                d.off()
                logger.info("Turning off: {0}".format(MODEM))
            except:
                logger.info("Failed to turn off {0}; ALREADY OFF".format(MODEM))

            time.sleep(10)

            try:
                d.on()
                logger.info("Turning on: {0}".format(MODEM))
                
                #reset performed, flip bit
                reset=1
            except:
                logging.info("Failed to turn on: {0}".format(MODEM))

    if reset==0:
        logger.info('{0} NOT FOUND - RESET NOT PERFORMED'.format(MODEM))

def main():
    logger.info("Script started...")

    #Counter
    i=0
    reset_counter=10

    #Test for internet connectivity
    while i<reset_counter and not internet():
        i+=1
        logger.info("No internet...retrying in 30 seconds.")
        time.sleep(30)

        #logger.info('i={0}'.format(i))

        if i>=reset_counter:
            logger.info("Initiating Wemo connection.")
            wemo_switch()

    logger.info("Script shutting down....")

if __name__ == "__main__":
    main()
