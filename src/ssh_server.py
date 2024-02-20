import socket
import paramiko
from src.logging import logger

from src.server_base import ServerBase
from src.ssh_server_interface import SshServerInterface
from src.shell import Shell
from src.client import Client

from src.cmg import Cmg


class SshServer(ServerBase):
    def __init__(self, host_key_file, host_key_file_password=None):
        super(SshServer, self).__init__()

        self._host_key = paramiko.RSAKey.from_private_key_file(host_key_file, host_key_file_password)

    def connection_function(self, client: Client):
        logger.info(f'a new client tries to connect')
        try:
            # create the SSH transport object
            session = paramiko.Transport(client.socket)
            session.add_server_key(self._host_key)
            #session.is_alive()


            # create the server
            server = SshServerInterface(client=client)
            cmg = Cmg()

            # start the SSH server
            try:
                session.start_server(server=server)
                # print(session.session_id)
                # session_id_string = codecs.encode(session.session_id, "hex")
                # print(session_id_string.decode())
            except paramiko.SSHException:
                return

            # create the channel and get the stdio
            channel = session.accept()
            # we use rwU to make sure we can use readline() on the stdio
            stdio = channel.makefile('rwU')

            # create the client shell and start it
            # cmdloop() will block execution of this thread.
            logger.info("open shell")
            self.client_shell = Shell(cmg, client, session, stdio, stdio)
            self.client_shell.cmdloop()
            logger.info("close shell")


            # After execution continues, we can close the session
            # since the only way execution will continue from
            # cmdloop() is if we explicitly return True from it,
            # which we do with the bye command.
            # channel.close()
            # self.client_shell.stop_commandloop()
            session.close()
        except:
            pass
