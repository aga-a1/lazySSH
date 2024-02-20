from src.ssh_server import SshServer
from src.logging import logger
import time

if __name__ == '__main__':
    # How to Generate your SSH keys
    #
    # Linux:
    # use the command `ssh-keygen -A` in terminal
    # to generate all of your SSH keys. Once the command is run,
    # you can find the RSA key in the following location: ~/.ssh/id_rsa, or /home/username/.ssh/id_rsa
    #
    # Windows 10:
    # Press Windows Key, type 'Manage Optional Features`. If OpenSSH Client & Server is in the list, you're all set.
    # If either is not, click on "Add a feature" and search for `OpenSSH`, click on them to install.
    # Next, open cmd as administrator. Enter the command `ssh-keygen` and follow the on screen prompts.
    # The location of the key will be displayed. Copy that and paste the location here.
    # If you put a password, include it as the second parameter, otherwise don't include it.

    logger.info('Starting SSH Server')

    # server = SshServer('/home/cmg/.ssh/id_rsa')
    server = SshServer('id_rsa')

    # Start the server, you can give it a custom IP address and port, or
    # leave it empty to run on 127.0.0.1:22
    server.start(port=2222)
    while True:  # Todo: this is most probably not a good solution
        # Todo: without this solution the Main Thread Ends before the client thread has been started
        time.sleep(60)
    logger.info("end main")
