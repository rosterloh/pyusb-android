#!/usr/bin/python
# accessory.py
# License GPLv2
# (c) Manuel Di Cerbo, Nexus-Computing GmbH

import usb.core
import usb.util
import fcntl
import struct
import time
import threading
import os
import sys
import socket

from attribs import *

ACCESSORY_VID = 0x18D1
ACCESSORY_PID = (0x2D00, 0x2D01, 0x2D04, 0x2D05)

NETLINK_KOBJECT_UEVENT = 15

def main():

    if len(sys.argv) >= 2:
        parts = sys.argv[1].split('/')
        accessory_task(int(parts[0],16))
        return	

    while True:
        print("no arguments given, starting in daemon mode")
        try:
            sock = socket.socket(
                socket.AF_NETLINK,
                socket.SOCK_RAW,
                NETLINK_KOBJECT_UEVENT
            )

            sock.bind((os.getpid(), -1))
            vid = 0
            while True:
                data = sock.recv(512)
                try:
                    vid = parse_uevent(data)
                    if vid != None:
                        break
                except ValueError:
                    print("unable to parse uevent")

            sock.close()
            accessory_task(vid)
        except ValueError as e:
            print(e)

        print("accessory task finished")

def parse_uevent(data):
        lines = data.split('\0')
        keys = []
        for line in lines:
            val = line.split('=')
            if len(val) == 2:
                keys.append((val[0], val[1]))

        attributes = dict(keys)
        if 'ACTION' in attributes and 'PRODUCT' in attributes:
            if attributes['ACTION'] == 'add':
                parts = attributes['PRODUCT'].split('/')
                return int(parts[0], 16)

        return None

def accessory_task(vid):
    dev = usb.core.find(idVendor=vid)

    if dev is None:
        raise ValueError("No compatible device not found")

    print("compatible device found")

    if dev.idProduct in ACCESSORY_PID:
        print("device is in accessory mode")
    else:
        print("device is not in accessory mode yet,  VID %04X" % vid)

        accessory(dev)

        dev = usb.core.find(idVendor=ACCESSORY_VID)

        if dev is None:
            raise ValueError("No compatible device not found")

        if dev.idProduct in ACCESSORY_PID:
            print("device is in accessory mode")
        else:
            raise ValueError("")
    
    tries = 5
    while True:
        try:
            if tries <= 0:
                break

            dev.set_configuration()
            break
        except:
            print("unable to set configuration, retrying")
            tries -= 1
            time.sleep(1)

    # even if the Android device is already in accessory mode
    # setting the configuration will result in the
    # UsbManager starting an "accessory connected" intent
    # and hence a small delay is required before communication
    # works properly
    time.sleep(1)

    dev = usb.core.find(idVendor = ACCESSORY_VID);

    if dev is None:
        dev = usb.core.find(idVendor = vid);

    if dev is None:
        raise ValueError("device set to accessory mode but VID %04X not found" % vid)

    cfg = dev.get_active_configuration()
    if_num = cfg[(0,0)].bInterfaceNumber
    intf = usb.util.find_descriptor(cfg, bInterfaceNumber = if_num)

    ep_out = usb.util.find_descriptor(
        intf,
        custom_match = \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_OUT
    )

    ep_in = usb.util.find_descriptor(
        intf,
        custom_match = \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_IN
    )


    writer_thread = threading.Thread(target = writer, args = (ep_out, ))
    writer_thread.start()

    length = -1
    while True:
        try:
            data = ep_in.read(size = 1, timeout = 0)
            print("read value %d" % data[0])
        except usb.core.USBError as e:
            print("failed to send IN transfer")
            print(e)
            break

    writer_thread.join()
    print("exiting application")

def writer (ep_out):
    while True:
        try:
            length = ep_out.write([0], timeout = 0)
            print("%d bytes written" % length)
            time.sleep(0.5)
        except usb.core.USBError:
            print("error in writer thread")
            break


def accessory(dev):
    version = dev.ctrl_transfer(
                usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_IN,
                51, 0, 0, 2)

    print("version is: %d" % struct.unpack('<H',version))

    assert dev.ctrl_transfer(
            usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_OUT,
            52, 0, 0, MANUFACTURER) == len(MANUFACTURER)

    assert dev.ctrl_transfer(
            usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_OUT,
            52, 0, 1, MODEL_NAME) == len(MODEL_NAME)


    assert dev.ctrl_transfer(
            usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_OUT,
            52, 0, 2, DESCRIPTION) == len(DESCRIPTION)

    assert dev.ctrl_transfer(
            usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_OUT,
            52, 0, 3, VERSION) == len(VERSION)

    assert dev.ctrl_transfer(
            usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_OUT,
            52, 0, 4, URL) == len(URL)

    assert dev.ctrl_transfer(
            usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_OUT,
            52, 0, 5, SERIAL_NUMBER) == len(SERIAL_NUMBER)

    dev.ctrl_transfer(
            usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_OUT,
            53, 0, 0, None)

    time.sleep(1)

if __name__ == "__main__":
    pid_file = '/root/program.pid'
    fp = open(pid_file, 'w')
    try:
        fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        sys.exit(0)

    main()
