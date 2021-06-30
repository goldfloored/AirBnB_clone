#!/usr/bin/python3
"""
a console python package
"""

import cmd
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """
    a class instance to execute a prompt
    """
    prompt = "(hbnb) "
    __classes = ["BaseModel",
                 "User",
                 "State",
                 "City",
                 "Amenity",
                 "Place",
                 "Review"]

    def parse(self, arg):
        return tuple(arg.split())

    def do_EOF(self, arg):
        """'EOF' ends process"""
        print()
        return True

    def do_quit(self, arg):
        """'quit' ends process"""
        return True

    def emptyline(self):
        """if an empty line is entered it is passed waits command"""
        pass

    def do_create(self, arg):
        """Creates a new instance of specified class"""
        if len(arg) == 0:
            print("** class name missing **")
        elif arg not in self.__classes:
            print("** class doesn't exist **")
        else:
            new = eval("{}()".format(arg))
            storage.new(new)
            storage.save()
            print(new.id)

    def do_show(self, arg):
        """Shows attrs of specified instance"""
        args = self.parse(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.__classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            if key not in storage.all():
                print("** no instance found **")
            else:
                obj = storage.all()[key]
                print(obj)

    def do_destroy(self, arg):
        """Destroys specified instance"""
        args = self.parse(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.__classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            if key not in storage.all():
                print("** no instance found **")
            else:
                del storage.all()[key]
                storage.save()

    def do_all(self, arg):
        """Shows attrs of all instances"""
        obj_list = []
        if len(arg) == 0:
            for value in storage.all().values():
                obj_list.append(value.__str__())
            print(obj_list)
        elif arg not in self.__classes:
            print("** class doesn't exist **")
        else:
            for key, value in storage.all().items():
                if arg in key:
                    obj_list.append(storage.all()[key].__str__())
                print(obj_list)

    def do_update(self, arg):
        """Update or add attr to specified instance"""
        args = self.parse(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.__classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif len(args) == 2:
            print("** attribute name missing **")
        elif len(args) == 3:
            print("** value missing **")
        elif ("{}.{}".format(args[0], args[1])) not in storage.all().keys():
            print("** no instance found **")
        else:
            key = "{}.{}".format(args[0], args[1])
            arg_type = type(eval(args[3]))
            attr = args[3].strip('\'\"')
            setattr(storage.all()[key], args[2], arg_type(attr))
            storage.all()[key].save()

if __name__ == '__main__':
    HBNBCommand().cmdloop()
