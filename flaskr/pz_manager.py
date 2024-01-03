import paramiko
import os

from dotenv import load_dotenv



# Load environment variables from the root directory
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

SERVER_PORT = 16261

class PZManager:
    def __init__(self, server_ip):
        self.server_ip = server_ip
        self.server_port = SERVER_PORT

    def connect_to_ec2(ip_address, key_file, username):
        key = paramiko.RSAKey.from_private_key_file(key_file)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        print("Connecting to the server...")
        client.connect(hostname=ip_address, username=username, pkey=key)

        return client

    def run_command(client, command):
        stdin, stdout, stderr = client.exec_command(command)
        print(stdout.read().decode())
        print(stderr.read().decode())
        stdin.close()