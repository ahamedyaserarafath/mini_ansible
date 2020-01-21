'''Base class for ssh communication
Example:
 command=RemoteShell(hostname=['192.168.50.99','192.168.42.160'],user='ubuntu')
 print command.run(cmd='ls')'''

from fabric.api import *
import fabric
import socket
import warnings
warnings.filterwarnings("ignore")
hostname = socket.gethostbyname(socket.gethostname())
import re
mpa = dict.fromkeys(range(32))
regex = re.compile("\x03(?:\d{1,2}(?:,\d{1,2})?)?", re.UNICODE)


def print_progress(self, transferred, tobetransferred):
    '''
       Callback function to calculate the percentage progressed
    '''
    progress = (transferred / float(tobetransferred)) * 100
    print(progress)


class RemoteShell(object):

    ''' Custom class with fabric to execute all the remote commands for Remote scripts.'''

    def __init__(self, hostname=None, cmd=None, user=None, pty=True,port=22,password="test@123",private_key=None,parallel=False):
        '''Host and user details are stored for fabric execution
        @param hostname type: List
        @param hostname: List of ip address

        '''
        env.hosts = hostname
        env.user = user
        env.password = password;
        if private_key:
            env.key_filename = private_key
        self.pty = pty
        env.port = 22
        # fabric output would be suppressed
        fabric.state.output['running'] = False
        fabric.state.output['output'] = False
        self.cmd = cmd
        self.parallel = parallel
        env.parallel = parallel
        env.abort_on_prompts = True        

    def _exec_remote_cmd(self):
        ''' Private function to execute the command with the default settings. Not to be used by the external system'''
        try:
            with hide('warnings'), settings(warn_only=True, parallel=self.parallel, capture=True):
                if env.hosts == hostname and env.user == local_hostname:
                    result = local(self.cmd, capture=True)
                else:
                    if self.pty:
                        result = run(self.cmd)
                    else:
                        result = run(self.cmd, pty=self.pty)
                return result, result.succeeded
        except Exception as e:
            print("Exception in communicating with the ip : " +str(env.hosts))
            print("Exception for your reference : " +str(e))
            return '', False

    def run(self, cmd):
        ''' This function to be called with an object to execute the command.
                  @param cmd type: String - command to be executed on the remote shell
                  @param cmd
                  @param parallel:Type boolean default serial execution is set and can be changed to True for parallel execution
                 Example:
                  >command=RemoteShell(hostname=['192.168.50.99','192.168.42.160'],user='ubuntu')
                  >print command.run(cmd='ls')
        '''
        try:
            self.cmd = cmd
            self.result = execute(self._exec_remote_cmd)
            return self.result.keys(), self.result.values()
        except Exception as e:
            print("Exception for your reference : " +str(e))
            raise Exception

    def return_status_message_fabric(self,fabric_obj):
        """The method returns the status and message from a fabric object."""
        try:
            key, value = fabric_obj
            status = list(value)[-1][-1]
            res = list(value)[-1][0]
            return status, res
        except Exception as e:
            print("Exception for your reference : " +str(e))

    def _file_send(self):
        """."""
        try:
            result = put(
                self.localpath,
                self.remotepath,
                mirror_local_mode=True)
            if result.succeeded:
                return 'Success'
            else:
                return 'Failed'
        except Exception as e:
            print("Exception for your reference : " +str(e))

    def file_send(self, localpath, remotepath):
        """."""
        try:
            self.localpath = localpath
            self.remotepath = remotepath
            self.result = execute(self._file_send)
            result = []
            for temp, value in self.result.items():
                result.append(temp + ':' + value + '\n')
            return ''.join(result)
        except Exception as e:
            print('Some problem in sending the file: ' + localpath + ' to ' + env.hosts)
            print("Exception for your reference : " +str(e))
