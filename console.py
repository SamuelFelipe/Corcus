#!/usr/bin/python3

import cmd
import shlex
from datetime import datetime
import models
from models.basemodel import BaseModel, Base
from models.bonus import Bonus
from models.employee import Employee
from models.item import Item
from models.company import Company
from models.admin import Admin


classes = {'bonus': Bonus,
           'item': Item,
           'employee': Employee,
           'company': Company,
           'admin': Admin
           }

time = '%Y-%m-%d'

class CORVUSCommand(cmd.Cmd):

    prompt = 'corvus [{}] '.format(datetime.strftime(datetime.utcnow(), time))

    def do_EOF(self, arg):
        '''Exits console'''
        return True

    def emptyline(self):
        '''Overwriting the emptyline method'''
        return False

    def do_quit(self, arg):
        return True

    def _key_value_parser(self, args):
        '''Creates a dictionary from a list of strings'''
        new_dict = {}
        for arg in args:
            if "=" in arg:
                kvp = arg.split('=', 1)
                key = kvp[0]
                value = kvp[1]
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0].replace('_', ' ')
                else:
                    try:
                        value = int(value)
                    except:
                        try:
                            value = float(value)
                        except:
                            continue
                new_dict[key] = value
        return new_dict


    def do_create(self, arg):
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            new_dict = self._key_value_parser(args[1:])
            instance = classes[args[0]](**new_dict)
        else:
            print("** class doesn't exist **")
            return False
        instance.save()
        print(instance.id)

    def do_all(self, arg):
        args = shlex.split(arg)
        obj_list = []
        if len(args) == 0:
            obj_dict = models.storage.all()
        elif args[0] in classes:
            obj_dict = models.storage.all(classes[args[0]])
        else:
            print("** class doesn't exist **")
            return False
        for key in obj_dict:
            obj_list.append(str(obj_dict[key]))
        print("[", end="")
        print(", ".join(obj_list), end="")
        print("]")

    def do_update(self, arg):
        args = shlex.split(arg)
        if len(args) == 0:
            print('** missing class name **')
        elif args[0] in classes:
            if len(args) > 1:
                if len(args) > 2:
                    matches = models.storage.all(classes[args[0]])
                    for match in matches.values():
                        if type(match.id) is int:
                            id = int(args[1])
                        else:
                            id = args[1]
                        if match.id == id:
                            attr = args[2].split('=')
                            if attr[0] in ['id']:
                                value = int(attr[1])
                            elif attr[0] in ['salary', 'hours', 'value']:
                                value = float(attr[1])
                            else:
                                value = attr[1]
                            setattr(match, attr[0], value)
                            match.save()

                else:
                    print('** missing info **')
            else:
                print('** missing id **')
        else:
            print('** class doesn\'t exist **')


if __name__ == '__main__':
    CORVUSCommand().cmdloop()
