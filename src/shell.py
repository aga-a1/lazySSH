from cmd import Cmd

import bigtree
from bigtree import dict_to_tree
import src.command_tree

from src.cmg import Cmg

from src.client import Client
from src.logging import logger
import time

from bigtree import list_to_tree
import readchar
import sys


class Shell(Cmd):
    use_rawinput = False

    # Constructor that will allow us to set out own stdin and stdout.
    # If stdin or stdout is None, sys.stdin or sys.stdout will be used
    def __init__(self, cmg: Cmg, client: Client, session, stdin=None, stdout=None):
        # call the base constructor of cmd.Cmd, with our own stdin and stdout
        super(Shell, self).__init__(completekey='tab', stdin=stdin, stdout=stdout)
        self.client = client
        self.session = session
        self.cmg = cmg
        self.intro = cmg.get_intro()
        self.stop_cmdloop = False

        # The prompt property can be overridden, allowing us to use a custom
        # string to be displayed at the beginning of each line. This will not
        # be included in any input that we get.
        # self.prompt = f'{self.client.username}@{self.client.host}> '
        # self.prompt = '*A:CMG901101# '
        self.command_context = ''

        # self.cmd_tree = src.command_tree.CommandTree()

        logger.info(f'User {self.client.username} connected from {self.client.host}:{self.client.port}')

    # def stop_commandloop(self):
    #    self.stop_cmdloop = True

    # These are custom print() functions that will let us utilize the given stdout.
    def print(self, value):
        # make sure the stdout is set.
        # we could add an else which uses the default print(), but I will not
        if self.stdout and not self.stdout.closed:
            self.stdout.write("\r" + value)

    def printchar(self, value):
        # value = 'ß'
        logger.debug('aaa')
        self.stdout.write(value)
        logger.debug('bbb')
        self.stdout.flush()
        logger.debug('ccc')

    def printline(self, value):
        self.print(value + '\n\r')

    def print_screen(self, value):
        line_counter = 1
        lines_of_terminal = 50
        for line in value.split('\n'):
            if line_counter % lines_of_terminal == 0:
                # Todo: \rPress any key to continue (Q to quit)\x00\r\n
                self.print('\rPress any key to continue (Q to quit)\r')
                c = self.stdin.read(1)
                # self.printline(line)
                self.stdout.write(line + '\r\n')
                self.stdout.flush()
            else:
                # self.printline(line)
                self.stdout.write(line + '\r\n')
                self.stdout.flush()

            line_counter = line_counter + 1

    def printcomandline(self, value):
        logger.debug('+++++ printcomandline')
        value = value.strip()
        output = self.cmg.get_prompt() + self.cmg.get_context_as_string() + '# ' + value  # + commands
        logger.info("value: " + repr(value))
        logger.info("output: " + repr(output))
        # self.print(output)
        self.stdout.write(output)
        self.stdout.flush()
        logger.debug('----- printcomandline')

    def cmdloop(self):
        """Repeatedly issue a prompt, accept input, parse an initial prefix
        off the received input, and dispatch to action methods, passing them
        the remainder of the line as argument.
        """
        logger.info(f'entering cmdloop')
        # xxx line = self.prompt
        line = ''
        # self.stdout.write(self.prompt)
        # self.stdout.flush()

        self.preloop()
        if self.use_rawinput and self.completekey:
            try:
                # Todo: import readline here?!
                import readline
                self.old_completer = readline.get_completer()
                readline.set_completer(self.complete)
                readline.parse_and_bind(self.completekey + ": complete")
            except ImportError:
                pass
        try:
            # if intro is not None:
            #    self.intro = intro
            if self.intro:
                self.stdout.write(str(self.intro) + "\n")
                self.printcomandline('')
            self.stop_cmdloop = None
            while not self.stop_cmdloop:
                if self.cmdqueue:
                    line = self.cmdqueue.pop(0)
                else:
                    if self.use_rawinput:
                        try:
                            self.debug("blablabla")
                            line = input(self.prompt)
                        except EOFError:
                            line = 'EOF'
                    else:
                        if not self.session.is_alive():
                            self.stop_cmdloop = True
                        c = self.stdin.read(1)  # reads one byte at a time, similar to getchar()
                        if c == b'\xc3':
                            # 2 byte character
                            logger.debug("character with 2 bytes")
                            d = self.stdin.read(1)
                            e = c+d
                            c = e
                            logger.debug(c)
                            f = str(c.decode("utf-8"))
                            c = f
                            print(type(c))
                        else:
                            # 1 byte character
                            c_as_string = str(c.decode("utf-8"))
                        logger.info(c)
                        logger.info(type(c))
                        logger.info(hex(ord(c)))

                        if c == b'\r':  # Enter Key
                            logger.debug('key: enter')
                            # command = line.strip()
                            # logger.info("1 command: " + command + "---")
                            try:
                                cmd, arg, line = self.parseline(line)
                                # command_list = self.cmd_tree.get_list_of_commands(line)

                                if line == 'show router 6203 bfd session':
                                    logger.debug('enter key: show router 6203 bfd session')
                                    self.printline('')
                                    func = getattr(self, 'do_' + 'show_router_6203')
                                    func(arg)
                                    line = ''
                                    self.printcomandline('\n')
                                elif line == 'show router 100012000 bfd session':
                                    logger.debug('enter key: show router 100012000 bfd session')
                                    self.printline('')
                                    func = getattr(self, 'do_' + 'show_router_100012000')
                                    func(arg)
                                    line = ''
                                    self.printcomandline('\n')
                                elif line == 'show router 9999 bfd session':
                                    logger.debug('enter key: show router 9999 bfd session')
                                    self.printline('')
                                    func = getattr(self, 'do_' + 'show_router_9999_bfd_session')
                                    func(arg)
                                    line = ''
                                    self.printcomandline('\n')
                                elif 'ping router 6207' in line:
                                    logger.debug('enter key: ping router 6207')
                                    self.printline('')
                                    func = getattr(self, 'do_' + 'ping_router_6207')
                                    func(arg)
                                    line = ''
                                    # self.printline('')
                                    self.printcomandline('\n')
                                elif 'ping router' in line:
                                    logger.debug('enter key: ping router')
                                    self.printline('')
                                    func = getattr(self, 'do_' + 'ping')
                                    func(arg)
                                    line = ''
                                    self.printcomandline('\n')
                                elif line == 'quit':
                                    # Todo: is the session really closed
                                    #  because the putty behaviour is different compared to the real CMG
                                    logger.debug('enter key: quit')
                                    self.stop_cmdloop = "q"
                                elif line == '':
                                    logger.debug('enter key: empty line')
                                    self.printline('')
                                    self.printcomandline('')
                                    # print("\033[%d;%dH" % (5, 5))
                                else:
                                    # no command could be found
                                    logger.debug('enter key: else')
                                    line = ''
                                    self.printline('')
                                    self.printcomandline('\n')
                            except Exception as error:
                                print("An exception occurred:", error)
                        # elif c == b'a' or b'b' or b'c' or b'd' or b'e' or b'f' or b'g' or b'h' or b'i' or \
                        #         b'j' or b'k' or b'l' or b'm' or b'n' or b'o' or b'p' or b'q' or b'r' or b's' \
                        #         or b't' or b'u' or b'v' or b'g' or b'x' or b'y' or b'z':
                        #     logger.debug('cmd_loop: a-z')
                        #     self.printchar(c.decode("utf-8"))
                        #     line = line + c.decode("utf-8")
                        elif c_as_string.isprintable():
                            logger.debug('cmd_loop: isprintable()' + ': ' + str(c))
                            self.printchar(c_as_string)
                            line = line + c_as_string
                            logger.debug('line: ' + line)
                        elif c == b'\x7f':  # backspace
                            logger.debug('cmd_loop: backspace')
                            self.printchar(c.decode("utf-8"))
                            logger.info(line)
                        elif c == b'\x03':  # CTRL + C
                            logger.debug('cmd_loop: CTRL + C')
                            self.stop_cmdloop = "q"
                        elif c == b'\t':  # Tab
                            logger.debug('cmd_loop: Tab')
                            command_list = self.cmd_tree.get_list_of_commands(line)
                            command = line.rpartition(' ')[-1]
                            commands_found = []  # counts how often the command has been found in the list
                            for cmd in command_list:
                                if cmd.startswith(command):
                                    commands_found.append(cmd)
                            if len(commands_found) == 1:  # only one command has been found
                                logger.info(commands_found)
                                logger.info("xxx" + commands_found[0])
                                self.command_context = commands_found[0]
                                self.cmd_tree.set_tab_context(commands_found[0])
                                # self.cmd_tree.show(attr_list=["has_context", "has_tab_context"])

                                ancestor_string = self.cmd_tree.get_ancestors_string()
                                line = ancestor_string + commands_found[0] + ' '
                                # line = ancestor_string
                                try:
                                    ancestors_list = self.cmd_tree.get_ancestors_list()
                                    # self.cmg.set_context(ancestors_list)
                                except Exception as error:
                                    print("An exception occurred:", error)
                            elif len(commands_found) > 1:  # more than one command starts with the users imput
                                logger.info(commands_found)
                                self.printline('')
                                for cmd in commands_found:
                                    logger.info(cmd)
                                    self.printline(cmd)
                                    self.stdout.flush()
                            logger.info("command: " + command)
                        elif c == b'':
                            logger.debug('cmd_loop: empty')
                            self.stop_cmdloop = "q"
                        else:
                            logger.debug("cmd_loop: else")
                            # line = line + c.decode("utf-8")
                            line = line + c_as_string
            self.postloop()
        finally:
            if self.use_rawinput and self.completekey:
                try:
                    import readline
                    readline.set_completer(self.old_completer)
                except ImportError:
                    pass

    # To create a command that is executable in our shell, we create functions
    # that are prefixed with do_ and contains the argument arg.
    # For example, if we want the command 'greet', we create do_greet().
    # If we want greet to take a name as well, we pass it as an arg.

    def do_back(self):
        logger.info("do_back")
        x_node = bigtree.find_attr(self.command_tree, "has_context", True)
        x_node.set_attrs({"has_context": False})
        x_node.parent.set_attrs({"has_context": True})

    def do_ping(self, arg):
        logger.info("+++++ do_ping")
        output = '''PING 10.251.74.129 56 data bytes
64 bytes from 10.251.74.129: icmp_seq=1 ttl=64 time=0.500ms.

---- 10.251.74.129 PING Statistics ----
1 packet transmitted, 1 packet received, 0.00% packet loss
round-trip min = 0.500ms, avg = 0.500ms, max = 0.500ms, stddev = 0.000ms'''
        # time.sleep(0.437)
        self.print_screen(output)
        logger.info("----- do_ping")

    def do_ping_router_6207(self, arg):
        logger.info("+++++ do_ping")
        output = '''PING 10.122.171.129 56 data bytes
Request timed out. icmp_seq=1.

---- 10.122.171.129 PING Statistics ----
1 packet transmitted, 0 packets received, 100% packet loss
'''
        time.sleep(1)
        self.print_screen(output)
        logger.info("----- do_ping")

    def do_show_router_9999_bfd_session(self, arg):
        # command: show router 9999 bfd session
        logger.info("+++++ do_show_router_9999_bfd_session")
        logger.info(arg)
        # output = self.cmg.__config_file['show_router_9999_bfd_session']
        output = self.cmg.get_config_file()
        self.print_screen(output)
        logger.info("----- do_show_router_9999_bfd_session")

    def do_show_router_100012000(self, arg):
        logger.info("+++++ do_show_router_100012000")
        logger.info(arg)

        output = ('===============================================================================\n'
                  'Legend:\n'
                  '  Session Id = Interface Name | LSP Name | Prefix | RSVP Sess Name | Service Id\n'
                  '  wp = Working path   pp = Protecting path\n'
                  '===============================================================================\n'
                  'BFD Session\n'
                  '===============================================================================\n'
                  'Session Id                                        State      Tx Pkts    Rx Pkts\n'
                  '  Rem Addr/Info/SdpId:VcId                      Multipl     Tx Intvl   Rx Intvl\n'
                  '  Protocols                                        Type     LAG Port     LAG ID\n'
                  '  Loc Addr\n'
                  '-------------------------------------------------------------------------------\n'
                  'CMG901101_VOVI_LB1NET1AL1                            Up     35854822   29296054\n'
                  '  10.122.142.193                                      3          100        100\n'
                  '  bgp                                               iom          N/A        N/A\n'
                  '  10.122.142.194\n'
                  'CMG901101_VOVI_LB1NET1AL1                            Up     35854842   29296050\n'
                  '  fda1:3fb1:1:20::1                                   3          100        100\n'
                  '  bgp                                               iom          N/A        N/A\n'
                  '  fda1:3fb1:1:20::2\n'
                  'CMG901101_VOVI_LB2NET2AL1                            Up     35854471   29296049\n'
                  '  10.251.111.1                                        3          100        100\n'
                  '  bgp                                               iom          N/A        N/A\n'
                  '  10.251.111.2\n'
                  # 'CMG901101_VOVI_LB2NET2AL1                            Up     35854347   29296036\n'
                  # '  fda1:3fb1:1:21::1                                   3          100        100\n'
                  # '  bgp                                               iom          N/A        N/A\n'
                  # '  fda1:3fb1:1:21::2\n'
                  'CMG901101_VOVI_LB1NET1AL2                            Up     35854773   29298094\n'
                  '  10.122.142.209                                      3          100        100\n'
                  '  bgp                                               iom          N/A        N/A\n'
                  '  10.122.142.210\n'
                  'CMG901101_VOVI_LB1NET1AL2                            Up     35854489   29298091\n'
                  '  fda1:3fb1:1:22::1                                   3          100        100\n'
                  '  bgp                                               iom          N/A        N/A\n'
                  '  fda1:3fb1:1:22::2\n'
                  'CMG901101_VOVI_LB2NET2AL2                            Up     35854822   29298196\n'
                  '  10.251.111.9                                        3          100        100\n'
                  '  bgp                                               iom          N/A        N/A\n'
                  '  10.251.111.10\n'
                  'CMG901101_VOVI_LB2NET2AL2                            Up     35854387   29298096\n'
                  '  fda1:3fb1:1:23::1                                   3          100        100\n'
                  '  bgp                                               iom          N/A        N/A\n'
                  '  fda1:3fb1:1:23::2\n'
                  '-------------------------------------------------------------------------------\n'
                  'No. of BFD sessions: 8\n'
                  '===============================================================================\n')

        #         output = '''===============================================================================
        # Legend:
        #   Session Id = Interface Name | LSP Name | Prefix | RSVP Sess Name | Service Id
        #   wp = Working path   pp = Protecting path
        # ===============================================================================
        # BFD Session
        # ===============================================================================
        # Session Id                                        State      Tx Pkts    Rx Pkts
        #   Rem Addr/Info/SdpId:VcId                      Multipl     Tx Intvl   Rx Intvl
        #   Protocols                                        Type     LAG Port     LAG ID
        #   Loc Addr
        # -------------------------------------------------------------------------------
        # CMG901101_VOVI_LB1NET1AL1                            Up     35854822   29296054
        #   10.122.142.193                                      3          100        100
        #   bgp                                               iom          N/A        N/A
        #   10.122.142.194
        # CMG901101_VOVI_LB1NET1AL1                            Up     35854842   29296050
        #   fda1:3fb1:1:20::1                                   3          100        100
        #   bgp                                               iom          N/A        N/A
        #   fda1:3fb1:1:20::2
        # CMG901101_VOVI_LB2NET2AL1                            Up     35854471   29296049
        #   10.251.111.1                                        3          100        100
        #   bgp                                               iom          N/A        N/A
        #   10.251.111.2
        # CMG901101_VOVI_LB2NET2AL1                            Up     35854347   29296036
        #   fda1:3fb1:1:21::1                                   3          100        100
        #   bgp                                               iom          N/A        N/A
        #   fda1:3fb1:1:21::2
        # CMG901101_VOVI_LB1NET1AL2                            Up     35854773   29298094
        #   10.122.142.209                                      3          100        100
        #   bgp                                               iom          N/A        N/A
        #   10.122.142.210
        # CMG901101_VOVI_LB1NET1AL2                            Up     35854489   29298091
        #   fda1:3fb1:1:22::1                                   3          100        100
        #   bgp                                               iom          N/A        N/A
        #   fda1:3fb1:1:22::2
        # CMG901101_VOVI_LB2NET2AL2                            Up     35854822   29298196
        #   10.251.111.9                                        3          100        100
        #   bgp                                               iom          N/A        N/A
        #   10.251.111.10
        # CMG901101_VOVI_LB2NET2AL2                            Up     35854387   29298096
        #   fda1:3fb1:1:23::1                                   3          100        100
        #   bgp                                               iom          N/A        N/A
        #   fda1:3fb1:1:23::2
        # -------------------------------------------------------------------------------
        # No. of BFD sessions: 8
        # ==============================================================================='''
        self.print_screen(output)
        logger.info("----- show_router_100012000")

    def do_show_router_6203(self, arg):
        logger.info("+++++ do_show_router")
        logger.info(arg)

        output = '''===============================================================================
Legend:
  Session Id = Interface Name | LSP Name | Prefix | RSVP Sess Name | Service Id
  wp = Working path   pp = Protecting path
===============================================================================
BFD Session
===============================================================================
Session Id                                        State      Tx Pkts    Rx Pkts
  Rem Addr/Info/SdpId:VcId                      Multipl     Tx Intvl   Rx Intvl
  Protocols                                        Type     LAG Port     LAG ID
  Loc Addr
-------------------------------------------------------------------------------
CMG901101_CORE_LB1NET1AL1                            Up     12501484   10214433
  10.251.74.129                                       3          100        100
  bgp                                               iom          N/A        N/A
  10.251.74.130
CMG901101_CORE_LB2NET2AL1                            Up     12501052   10214343
  10.251.75.1                                         3          100        100
  bgp                                               iom          N/A        N/A
  10.251.75.2
CMG901101_CORE_LB1NET1AL2                            Up     12500988   10215069
  10.251.74.145                                       3          100        100
  bgp                                               iom          N/A        N/A
  10.251.74.146
CMG901101_CORE_LB2NET2AL2                            Up     12500849   10215113
  10.251.75.9                                         3          100        100
  bgp                                               iom          N/A        N/A
  10.251.75.10
-------------------------------------------------------------------------------
No. of BFD sessions: 4
==============================================================================='''
        self.print_screen(output)
        logger.info("----- do_show_router_6203")

    def do_show(self, arg):
        logger.info("do_show")

        if arg == '':
            logger.info('empty arg')
            try:
                # ancestors_list = self.cmd_tree.get_ancestors_list()
                self.cmd_tree.set_context('show')
                ancestors_list = self.cmd_tree.get_ancestors_list()
                self.cmg.set_context(ancestors_list)
            except Exception as error:
                print("An exception occurred:", error)
        # else:
        #     logger.info('not empty arg')
        # x = ":".join("{:02x}".format(ord(c)) for c in arg)
        # logger.info(x)
        elif arg:
            # *A:CMG901101# show router 6203 bfd session

            bfd_sessions = {
                "6203": {
                    "CMG901101_CORE_LB1NET1AL1": {
                        "session": {
                            "State": "Up",
                            "Tx Pkts": "12501484",
                            "Rx Pkts": "10214433"
                        },
                        "Rem_Addr": {
                            "Rem_Addr": "10.251.74.129",
                            "Multipl": "3",
                            "Tx Intvl": "100",
                            "Rx Intvl": "100"
                        },
                        "Protocols": {
                            "Protocols": "bgp",
                            "Type": "iom",
                            "LAG Port": "N/A",
                            "LAG ID": "N/A"
                        },
                        "Loc Addr": {
                            "Loc Addr": "10.251.74.130",
                        }
                    },
                    "CMG901101_CORE_LB1NET1AL2": {
                        "session": {
                            "State": "Up",
                            "Tx Pkts": "12501484",
                            "Rx Pkts": "10214433"
                        },
                        "Rem_Addr": {
                            "Rem_Addr": "10.251.74.129",
                            "Multipl": "3",
                            "Tx Intvl": "100",
                            "Rx Intvl": "100"
                        },
                        "Protocols": {
                            "Protocols": "bgp",
                            "Type": "iom",
                            "LAG Port": "N/A",
                            "LAG ID": "N/A"
                        },
                        "Loc Addr": {
                            "Loc Addr": "10.251.74.130",
                        }
                    }
                }
            }
            # logger.info(sessions)
            # logger.info(sessions["CMG901101_CORE_LB1NET1AL1"])
            # logger.info(sessions["CMG901101_CORE_LB1NET1AL1"]["session"])
            # logger.info(sessions["CMG901101_CORE_LB1NET1AL1"]["Rem_Addr"]["Rem_Addr"])

            for key, value in bfd_sessions.items():
                logger.info(key)
                logger.info(value)

            bfd_session = bfd_sessions["6203"]
            logger.info("------------------------------------------------")
            logger.info(bfd_session)
            logger.info("------------------------------------------------")
            output = ""
            key = "6203"
            if key in bfd_sessions.keys():
                logger.info("YESSSSS")
                header = """===============================================================================\r
Legend:\r
  Session Id = Interface Name | LSP Name | Prefix | RSVP Sess Name | Service Id\r
  wp = Working path   pp = Protecting path\r
===============================================================================\r
BFD Session\r
===============================================================================\r
Session Id                                        State      Tx Pkts    Rx Pkts\r
  Rem Addr/Info/SdpId:VcId                      Multipl     Tx Intvl   Rx Intvl\r
  Protocols                                        Type     LAG Port     LAG ID\r
  Loc Addr\r
-------------------------------------------------------------------------------"""
                self.printline(header)
                for key, value in bfd_session.items():
                    logger.info(key)
                    logger.info(value)
                    logger.info(value["session"]["State"])
                    output_1 = "{:<50}{:>5}{:>13}{:>11}".format(key, value["session"]["State"],
                                                                value["session"]["Tx Pkts"],
                                                                value["session"]["Rx Pkts"])
                    output_2 = "  {:<48}{:>5}{:>13}{:>11}".format(value["Rem_Addr"]["Rem_Addr"],
                                                                  value["Rem_Addr"]["Multipl"],
                                                                  value["Rem_Addr"]["Tx Intvl"],
                                                                  value["Rem_Addr"]["Rx Intvl"])
                    self.printline(output_1)
                    self.printline(output_2)

            # CMG901101_CORE_LB1NET1AL1                            Up     12501484   10214433\r
            #   10.251.74.129                                       3          100        100\r
            #   bgp                                               iom          N/A        N/A\r
            #   10.251.74.130\r
            # CMG901101_CORE_LB2NET2AL1                            Up     12501052   10214343\r
            #   10.251.75.1                                         3          100        100\r
            #   bgp                                               iom          N/A        N/A\r
            #   10.251.75.2\r
            # CMG901101_CORE_LB1NET1AL2                            Up     12500988   10215069\r
            #   10.251.74.145                                       3          100        100\r
            #   bgp                                               iom          N/A        N/A\r
            #   10.251.74.146\r
            # CMG901101_CORE_LB2NET2AL2                            Up     12500849   10215113\r
            #   10.251.75.9                                         3          100        100\r
            #   bgp                                               iom          N/A        N/A\r
            #   10.251.75.10\r
            # -------------------------------------------------------------------------------\r
            # No. of BFD sessions: 4\r
            # ===============================================================================\r
            # """

            else:
                logger.info("NOOOOOO")


        else:
            self.printline('show command!')

    def do_greet(self, arg):
        if arg:
            self.printline('Hey {0}! Nice to see you!'.format(arg))
        else:
            self.emptyline()
            self.printline('Hello there!')

    # even if you don't use the arg parameter, it must be included.
    def do_quit(self, arg):
        self.printline('See you later!')

        # if a command returns True, the cmdloop() will stop.
        # this acts like disconnecting from the shell.
        return True

    def do_clear(self, arg):
        self.print('\033c')

    # If an empty line is given as input, we just print out a newline.
    # This fixes a display issue when spamming enter.
    def emptyline(self):
        self.print('\r\n')

    def default(self, line: str) -> None:
        logger.info(f'User {self.client.username} tried to execute command "{line}"')
        # self.printline(self.prompt)
        error_string_1 = " " * (len(self.prompt)) + '^'
        self.printline(error_string_1)
        self.printline(f'Error: Bad command.')
