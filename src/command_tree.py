from bigtree import dict_to_tree, tree_to_dict
from bigtree import find_name
from src.cmg import Cmg as cmg


import bigtree

# import pandas
from src.logging import logger


class CommandTree:
    def __init__(self):
        self.command_tree = self.create_tree_from_dict()

    def create_tree_from_dict(self):
        path_dict = {
            "root": {"has_context": True, "has_tab_context": True},
            "root/show": {"has_context": False, "has_tab_context": False},
            "root/show/system": {"has_context": False, "has_tab_context": False},
            "root/show/time": {"has_context": False, "has_tab_context": False},
            "root/show/uptime": {"has_context": False, "has_tab_context": False},
            "root/show/users": {"has_context": False, "has_tab_context": False},
            "root/show/version": {"has_context": False, "has_tab_context": False},
            "root/sleep": {"has_context": False, "has_tab_context": False},
            "root/ssh": {"has_context": False, "has_tab_context": False},
        }
        command_tree = dict_to_tree(path_dict)
       # root.show(attr_list=["age"])

        return command_tree

    # converts the user input into a list of single strings
    # input : show router 6203 bfd session
    # output: ['show', 'router', '6203', 'bfd', 'session']
    def get_list_of_commands(self, line):
        # commands_list = ["show", "sleep", "ssh"]
        logger.debug("+++++ get_list_of_commands")
        commands_list = []
        logger.debug(line)
        list_of_commands_in_line = line.split()
        logger.debug(list_of_commands_in_line)
        for command in list_of_commands_in_line:
            try:
                #x_node = bigtree.find_attr(self.command_tree, name='command')
                x_node = find_name(self.command_tree, command)
                logger.info(x_node.children)
                for command in x_node.children:
                    logger.info(command.get_attr("name"))
                    commands_list.append(command.get_attr("name"))
            except Exception as error:
                print("An exception occurred:", error)
            logger.debug("----- get_list_of_commands")

        return commands_list


    # def get_list_of_commands(self, line):
    #     # commands_list = ["show", "sleep", "ssh"]
    #     logger.debug("+++++ get_list_of_commands")
    #     logger.debug(line)
    #     list_of_commands_in_line = line.split()
    #     logger.debug(list_of_commands_in_line)
    #     for command in list_of_commands_in_line:
    #         try:
    #             x_node = bigtree.find_attr(self.command_tree, "has_tab_context", True)
    #             commands_list = []
    #             logger.info(x_node.children)
    #             for command in x_node.children:
    #                 logger.info(command.get_attr("name"))
    #                 commands_list.append(command.get_attr("name"))
    #         except Exception as error:
    #             print("An exception occurred:", error)
    #         logger.debug("----- get_list_of_commands")
    #
    #     return commands_list

    def get_ancestors_string(self):
        logger.info("+++++ get_ancestors_string")
        x_node = bigtree.find_attr(self.command_tree, "has_tab_context", True)
        logger.info(x_node)
        ancestors_list = []
        for leave in x_node.ancestors:
            ancestors_list.append(leave.name)
            logger.info(leave.name)
        # if not ancestors_list:
        ancestors_list.pop()

        logger.info("ancestors_string: ")
        logger.info(ancestors_list)
        self.command_tree.show(attr_list=["has_context", "has_tab_context"])

        ancestors_string = ''
        for i in ancestors_list:
            new_string = ancestors_string + i + ' '
            ancestors_string = new_string

        logger.info("----- get_ancestors_string")

        return ancestors_string

    def get_ancestors_list(self):
        # Todo: shall be renamed, as it returns the list for the context
        logger.info("*************************************************")
        x_node = bigtree.find_attr(self.command_tree, "has_context", True)
        logger.info(x_node)
        ancestors_list = []
        for leave in x_node.ancestors:
            # logger.info(leave)
            ancestors_list.append(leave.name)
            logger.info(leave.name)
        ancestors_list.pop()
        ancestors_list.append(x_node.get_attr('name'))

        logger.info(ancestors_list)
        logger.info("*************************************************")

        return ancestors_list

    def set_context(self, command):
        try:
            logger.info("------------- ende gelÃ¤nde -1 ------------")
            self.command_tree.show(attr_list=["has_context"])
            logger.info("------------- ende gelÃ¤nde 0 ------------")
            # x_node = find_name(self.command_tree, "show")
            # Todo: find_name just works if the command is uniq in the whole tree I think
            x_node = find_name(self.command_tree, command)
            x_node.set_attrs({"has_context": True})
            x_node.parent.set_attrs({"has_context": False})
            logger.info(x_node)
            logger.info(self.command_tree)
            self.command_tree.show(attr_list=["has_context"])
            logger.info("--------------- ende gelÃ¤nde 1 ------------")
            # x_node = find_name(self.command_tree, "root")
            # x_node.set_attrs({"has_context": False})
            logger.info(x_node)
            logger.info(self.command_tree)
            self.command_tree.show(attr_list=["has_context"])
            logger.info("--------------- ende gelÃ¤nde 2 ------------")
        except Exception as error:
            print("An exception occurred:", error)

    def set_tab_context(self, command):
        try:
            logger.debug("+++++ set_tab_context")
            self.command_tree.show(attr_list=["has_tab_context"])
            # Todo: find_name just works if the command is uniq in the whole tree I think
            x_node = find_name(self.command_tree, command)
            x_node.set_attrs({"has_tab_context": True})
            x_node.parent.set_attrs({"has_tab_context": False})
            self.command_tree.show(attr_list=["has_tab_context"])
            logger.debug("----- set_tab_context")
        except Exception as error:
            print("An exception occurred:", error)
