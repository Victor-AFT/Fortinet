import paramiko
from time import sleep
from paramiko import transport
import configparser
from datetime import datetime
import getpass,subprocess
from openpyxl import load_workbook, Workbook
userr = 'admin'
password = '12345'

transport.Transport._preferred_kex = (
        'ecdh-sha2-nistp256',
        'ecdh-sha2-nistp384',
        'ecdh-sha2-nistp521',
        'diffie-hellman-group-exchange-sha256',
        'diffie-hellman-group14-sha256',
        'diffie-hellman-group-exchange-sha1',
        'diffie-hellman-group14-sha1',
        'diffie-hellman-group1-sha1',
)


def check_ping(host):
    try:
        subprocess.check_output(['ping', host])
        return True
    except subprocess.CalledProcessError:
        return False


now = datetime.now()
time2 = now.strftime("%d-%m-%Y")

# os.system("cls")

list_ip=['127.0.0.1']

for ip in list_ip:
        if check_ping(ip):
                #print("ping al host")
                try:
                        client = paramiko.SSHClient()
                        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        client.connect(hostname=ip, port=2322, username=userr, password=password)
                        connection = client.invoke_shell()
                        ################### GET HOSTNAME #########################
                        sleep(1)
                        connection.send(b'\n')  # ENTER
                        sleep(1)
                        config = str(connection.recv(10000).decode(encoding='utf-8').replace(" ",""))
                        nombre_subestacion = config.split("#")[0] + '.txt'
                        g = open(nombre_subestacion, "w", encoding='utf-8')
                        print(config.split("#")[0])
                        sleep(1)
                        ################### GET SYS ARP #########################
                        connection.send(b'get system arp\n')
                        sleep(1)
                        config = str(connection.recv(10000).decode(encoding='utf-8'))
                        g.write(config)
                        sleep(1)
                        connection.send(b'\n')
                        sleep(1)
                        connection.send(b'diagnose user device list\n')
                        sleep(5)
                        config = str(connection.recv(10000).decode(encoding='utf-8'))
                        print(config)
                        g.write(config)
                        sleep(1)
                        connection.send(b'\n')
                        sleep(1)
                        config = str(connection.recv(10000).decode(encoding='utf-8'))
                        print(config)
                        g.write(config)
                        sleep(1)
                        connection.send(b'exit\n')
                        g.close()
                        connection.close()
                        client.close()
                except paramiko.AuthenticationException as auth_ex:
                        print(f"Error de autenticacion: {auth_ex}")
                except paramiko.SSHException as ssh_ex:
                        print(f"Error de ssh: {ssh_ex}")


