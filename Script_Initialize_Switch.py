import serial
import time
import sys
from time import sleep
from serial.serialutil import Timeout

def send_to_console(ser: serial.Serial, command: str, wait_time: float = 1):
    """
    Fonction pour paramétrer l'envoi des commandes à l'appareil via un port série

    Args:
        ser: Connexion au port série
        command: string, défini la commande qui sera envoyée via le port série
        wait_time: float, temps d'attente après avoir exécuter la commande
    """
    command_to_send = command + "\r"
    ser.write(command_to_send.encode('utf-8'))
    sleep(wait_time)
    print(ser.read(ser.inWaiting()).decode('utf-8'), end="")

def configure_switch():

    print("Configuration Interface VLAN1")
    """     Fonction pour passer les commandes à l'appareil     """
    ser = serial.Serial('COM7', timeout=1)
    print(f"Connexion au port {ser.name}...")

    #Passage en mode configuration
    send_to_console(ser, "enable")
    send_to_console(ser, "conf t")

    # Configuration VLAN1 pour management
    send_to_console(ser, "interface vlan 1")
    send_to_console(ser, "ip address 192.168.10.10 255.255.255.0")
    send_to_console(ser, "no shutdown")
    send_to_console(ser, "exit")

    # Fermeture de la connexion série
    ser.close()

def tftp_transfer():
    
    print("Récupération fichier .tar")
    """     Fonction pour passer les commandes à l'appareil     """
    ser = serial.Serial('COM7', timeout=1)

    print(f"Connexion au port {ser.name}...")

    #Passage en mode configuration
    send_to_console(ser, "end")
    send_to_console(ser, "enable")
    send_to_console(ser, "archive tar /xtract tftp://192.168.10.12/c1000-universalk9-tar.152-7.E6.tar flash: \r\n")

    # Fermeture de la connexion série
    ser.close()

def boot_system():

    print("Boot sur nouveau firmware")  
    """     Fonction pour passer les commandes à l'appareil     """
    ser = serial.Serial('COM7', timeout=1)

    print(f"Connexion au port {ser.name}...")

    send_to_console(ser, "end")
    send_to_console(ser, "enable")
    send_to_console(ser, "conf t")
    send_to_console(ser, "boot system flash:/c1000-universalk9-mz.152-7.E6/c1000-universalk9-mz.152-7.E6.bin")
    send_to_console(ser, "exit")
    send_to_console(ser, "reload")
    send_to_console(ser, "yes")
    send_to_console(ser, "\r\n")

    # Fermeture de la connexion série
    ser.close()

def delete_directory():

    print("Suppression anciens dossiers et fichiers")
    """     Fonction pour passer les commandes à l'appareil     """
    ser = serial.Serial('COM7', timeout=1)
    print(f"Connexion au port {ser.name}...")

    send_to_console(ser, "\r\n")
    send_to_console(ser, "enable")
    send_to_console(ser, "delete /force /recursive flash:/c1000-universalk9-mz.152-7.E4")
    send_to_console(ser, "delete /force flash:/c1000-universalk9-tar.152-7.E4.tar")
    send_to_console(ser, "delete /force flash:/c1000-universalk9-mz.152-7.E6.bin")
    send_to_console(ser, "delete /force flash:/config.text")
    send_to_console(ser, "delete /force flash:/private-config.text")
    send_to_console(ser, "exit")
    send_to_console(ser, "reload")

    # Fermeture de la connexion série
    ser.close()

def timer(seconds):

    for remaining in range(seconds, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} secondes restantes".format(remaining))
        sys.stdout.flush()
        time.sleep(1)

    sys.stdout.write("\rFini !\n")

configure_switch()
tftp_transfer()
timer(480)
boot_system()
timer(75)
delete_directory()