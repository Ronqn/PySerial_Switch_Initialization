import serial
import time
import sys
from time import sleep
from serial.serialutil import Timeout

com_port = "COM7"

def send_to_console(ser: serial.Serial, command: str, wait_time: float = 1):
    """
    Function to send the commands to the serial port

    Args:
        ser: Connecting to serial port
        command: string, The command that will be sent to the serial port
        wait_time: float, wait time after executing the command
    """
    command_to_send = command + "\r"
    ser.write(command_to_send.encode('utf-8'))
    sleep(wait_time)
    print(ser.read(ser.inWaiting()).decode('utf-8'), end="")

def configure_switch():

    print("Configure VLAN1")
    ser = serial.Serial(com_port, timeout=1)
    print(f"Connecting to port {ser.name}...")

    #Switch to configuration mode
    send_to_console(ser, "enable")
    send_to_console(ser, "conf t")

    # Configure VLAN1
    send_to_console(ser, "interface vlan 1")
    send_to_console(ser, "ip address 192.168.10.10 255.255.255.0")
    send_to_console(ser, "no shutdown")
    send_to_console(ser, "exit")

    # Close serial connexion 
    ser.close()

def tftp_transfer():
    
    print("Download .tar file")
    ser = serial.Serial(com_port, timeout=1)

    print(f"Connecting to port {ser.name}...")

    #Switch to configuration mode
    send_to_console(ser, "end")
    send_to_console(ser, "enable")

    #Get the new tar file via TFTP and extract it to the flash directory
    send_to_console(ser, "archive tar /xtract tftp://192.168.10.12/c1000-universalk9-tar.152-7.E6.tar flash: \r\n")

    # Close serial connexion
    ser.close()

def boot_system():

    print("Boot the new firmware")  
    ser = serial.Serial(com_port, timeout=1)

    print(f"Connecting to port {ser.name}...")

    #Switch to configuration mode
    send_to_console(ser, "end")
    send_to_console(ser, "enable")
    send_to_console(ser, "conf t")

    #Boot the new system firmware
    send_to_console(ser, "boot system flash:/c1000-universalk9-mz.152-7.E6/c1000-universalk9-mz.152-7.E6.bin")
    send_to_console(ser, "exit")
    send_to_console(ser, "reload")
    send_to_console(ser, "yes")
    send_to_console(ser, "\r\n")

    # Close serial connexion
    ser.close()

def delete_directory():

    print("Delete old firmware files and folders")
    ser = serial.Serial(com_port, timeout=1)
    print(f"Connecting to port {ser.name}...")

    #Switch to enable mode
    send_to_console(ser, "\r\n")
    send_to_console(ser, "enable")

    #Delete the folders and files of the old firmwares
    send_to_console(ser, "delete /force /recursive flash:/c1000-universalk9-mz.152-7.E4")
    send_to_console(ser, "delete /force flash:/c1000-universalk9-tar.152-7.E4.tar")
    send_to_console(ser, "delete /force flash:/c1000-universalk9-mz.152-7.E6.bin")
    send_to_console(ser, "delete /force flash:/config.text")
    send_to_console(ser, "delete /force flash:/private-config.text")
    send_to_console(ser, "exit")

    #Reboot the switch
    send_to_console(ser, "reload")

    # Close serial connexion
    ser.close()

def timer(seconds):

    for remaining in range(seconds, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining".format(remaining))
        sys.stdout.flush()
        time.sleep(1)

    sys.stdout.write("\rDone !\n")

configure_switch()
tftp_transfer()
timer(480)
boot_system()
timer(75)
delete_directory()