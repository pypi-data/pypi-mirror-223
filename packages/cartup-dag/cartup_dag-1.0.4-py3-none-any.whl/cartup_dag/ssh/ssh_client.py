import paramiko
from cartup_dag.config.config import *
from scp import SCPClient


class SSHClient:
    def __init__(self):
        self.sshcon = paramiko.SSHClient()  # will create the object
        self.sshcon.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshcon.connect(SSH_SERVER, username=SSH_USER, key_filename=SSH_CERTIFICATE)
        self.scp = SCPClient(self.sshcon.get_transport())

    def close(self):
        self.sshcon.close()

    def make_remote_dir(self, directory):
        self.sshcon.exec_command("mkdir -p " + directory)

    def execute_remote_command(self, cmd):
        self.sshcon.exec_command(cmd)

    def export_file_directory(self, remote_dir, local_dir, recursive=True):
        try:
            self.scp.put(
                local_dir,
                remote_path=remote_dir,
                recursive=recursive
            )
        except:
            raise Exception("Failed to export directory")
