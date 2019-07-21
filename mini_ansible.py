import os
import sys
sys.path.insert(0,"./common")

from fabric_common import RemoteShell
from fabric.network import ssh
from fabric.context_managers import *
from datetime import datetime
from ConfigParser import SafeConfigParser


class MiniAnsible():

    def __init__(self,conf_file="mini_ansible.conf"):
        self.ip = None
        self.username = None
        self.password = None
        self.command_list = None
        self.private_key = None
        self.local_path = None
        self.remote_path = None
        self.conf_file = os.path.abspath(conf_file)
        self.log_directory = "logs"
        if not os.path.isfile(self.conf_file):
            self.DoError("No such file found : %s" % conf_file, "red")
        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)
        ssh.util.log_to_file(self.log_directory+"/mini_ansible.log", 10)


    def DoError (self,Error) :
        sys.exit(Error)

    def parse_and_execute (self, force=False):
        """."""
        config = SafeConfigParser()
        try:
            config.read(self.conf_file)
        except configparser.DuplicateSectionError as e:
            print(e)
            sys.exit(1)
        except configparser.DuplicateOptionError as e:
            print(e)
            sys.exit(1)
        except configparser.ParsingError as e:
            print(colored('Parsing error in mini_ansible.conf', 'red'))
            print(e)
            sys.exit(1)
        sections = config.sections();
        for section in sections:
            self.__init__()
            print("-----------------> " + section)
            for key,value in config.items(section):
                if key == "ip":
                    self.ip = value
                if key == "username":
                    self.username = value
                if key == "password":
                    self.password = value
                if key == "command":
                    self.command_list = value.split("\n")
                if key == "private_key":
                    self.private_key = value
                if key == "local_path":
                    self.local_path = value
                if key == "remote_path":
                    self.remote_path = value
            if self.username and self.ip:
                if self.private_key:
                    if self.local_path and self.remote_path:
                        self.send_file_remote(self.local_path,self.remote_path,self.ip,self.username,private_key=self.private_key)
                        print("File sent succesfully : " + self.remote_path + "/" + str(self.local_path.split("/")[-1]))
                    if self.command_list:
                        self.execute_command_list_remotely(self.command_list,self.ip,self.username,private_key=self.private_key)
                    elif not self.local_path and not self.remote_path:
                        print("local_path or remote_path or command_list field are not found for " + str(section))
                if self.password:
                    if self.local_path and self.remote_path:
                        self.send_file_remote(self.local_path,self.remote_path,self.ip,self.username,password=self.password)
                        print("File sent succesfully : " + self.remote_path + "/" + str(self.local_path.split("/")[-1]))
                    if self.command_list:
                        self.execute_command_list_remotely(self.command_list,self.ip,self.username,password=self.password)
                    elif not self.local_path and not self.remote_path:
                        print("local_path or remote_path or command_list field are not found for " + str(section))
                if not self.private_key and not self.password:
                    print("private_key or password field are not found for " + str(section))
            else:
                print("username or ip field are not found for "+ str(section))


    def execute_command_list_remotely(self,command_list,ip,user,password=None,private_key=None):
        try:
            if private_key:
                ssh_connect_remote = RemoteShell(hostname=ip,user=user,private_key=private_key)
            else:
                ssh_connect_remote = RemoteShell(hostname=ip,user=user,password=password)
            for actual_command in command_list:
                print("IP / DNS : " + ip )
                print("Command : " + actual_command )
                f_obj = ssh_connect_remote.run(cmd=actual_command)
                status, res = ssh_connect_remote.return_status_message_fabric(f_obj)
                if status:
                    print("Output : " + str(res))
                else:
                    print("Output : Failed to execute the above command")
                    print("Error for your reference : " + str(res))
                print("\n")
            del ssh_connect_remote
        except Exception as e:
            self.DoError("Exception in execute_command_list_remotely :"+str(e) )

    def send_file_remote(self,local_path,remote_path,ip,user,password=None,private_key=None):
        try:
            if private_key:
                ssh_connect_remote = RemoteShell(hostname=ip,user=user,private_key=private_key)
            else:
                ssh_connect_remote = RemoteShell(hostname=ip,user=user,password=password)
            ssh_connect_remote.file_send(local_path,remote_path)
            del ssh_connect_remote
        except Exception as e:
            self.DoError("Exception in send_file_remote :"+str(e) )



def main():
    obj = MiniAnsible()
    try:
        obj.parse_and_execute()
    except Exception as e:
        obj.DoError(str(e))

if __name__ == "__main__":
    main()
