#! /usr/bin/python3
import argparse
import os
import sys
import subprocess
import re
import tomlkit as toml
toml_file = "pack.toml"
class PackTemplate:
    def __init__(self, string):
        self._string = string
        self._pattern = re.compile(r'(\$\{(\S*\.?\S*)\})')
    def replace(self, dictionary: dict):
        al = self.__match_all__(self._pattern, self._string)
        copy = self._string
        for i in al:
            loc_temp = re.findall(r'[^{$].*[^}]',i.group())
            loc = list(map(lambda x: x.split("."), loc_temp))
            dl = dictionary
            out = None
            for l in loc:
                for idd in l:
                    temp = dl.get(idd)
                    if not temp:
                        print("Key does not exist: " + '.'.join(l))
                        exit(1)
                    dl = temp
                copy = copy.replace(i.group(), str(dl))
        return copy
    def __match_all__(self, regex, string):
        def __match_all_dummy__(regex, string, array):
            found = regex.search(string)
            if not found:
                return
            else:
                array.append(found)
                __match_all_dummy__(regex, string[found.span()[1]:], array)
        out = []
        __match_all_dummy__(regex, string, out)
        return out




def open_toml(file: str):
    with open(file, mode="rb") as fp:
        out = toml.load(fp)
    return out
def read_config():
    return open_toml(toml_file)
def write_config(data: str):
    with open(toml_file, mode="w") as fp:
        fp.write(data)
def get_current_system(config):
    systems = config.get("system")
    global_system = config.get("pack").get("system")
    if config and systems and global_system:
        current_system = systems.get(global_system)
        if current_system:
            return current_system
    print("could not find system")
    exit(1)

def get_system_packages(config):
    systems = config.get("system")
    global_system = config.get("pack").get("system")
    if config and systems and global_system:
        current_system = systems.get(global_system)
        if current_system:
            return current_system.get("packages")
def get_global_packages(config):
    return config.get("pack").get("packages")
def clean(args):
    pass
def run_command(cmd, config, args=None):
    command = get_current_system(config).get("commands").get(cmd)
    dk = config.unwrap()
    if args:
        dk.update(args)
    template = PackTemplate(command).replace(dk)
    subprocess.run(template.split()) 
def create_global_package_args(id, name, system):
    return {"package":{"id":id, "name":name, "system":system}}
def install(args):
    config = read_config()
    if not config:
        print("No config found")
        return
    system_packages = get_system_packages(config)
    global_packages = get_global_packages(config)
    if global_packages and system_packages:
        for i in global_packages.unwrap():
            if i in system_packages:
                run_command("install", config, create_global_package_args(system_packages.get(i), i, config.get("pack").get("system")))

def remove(args):
    pass
def add(args):
    config = read_config()
    system_packages = get_system_packages(config)
    global_packages = get_global_packages(config)
    if args.package in global_packages:
        print(f"Package: {args.package} already exists.")
        return
    else:
        if args.package in system_packages:
            global_packages.add_line(args.package, indent=" ", add_comma = False, newline=False)
            write_config(toml.dumps(config))
            print(f"{args.package}, add successfuly")
        else:
            print(f"Package: {args.package} does not have a system equivalent")
def edit(args):
    out = subprocess.run([args.editor, toml_file])

def run_arbitrary(args):
    config = read_config()
    run_command(args.command, config) 

def setup_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(required=True, help="Action help")
    parser.add_argument("-f", "--file", help="The file to use as a config")
    #install
    sub_install = sub.add_parser("install", help="installs any new packages in pack.toml").set_defaults(func=install)
    #clean
    sub_clean = sub.add_parser("clean", help="uninstalls removed programs").set_defaults(func=clean)
    #remove
    sub_remove = sub.add_parser("remove", help="remove a program from the list (does not uninstall it)")
    sub_remove.set_defaults(func=remove)
    sub_remove.add_argument("package", help="the package to remove")
    #add
    sub_add = sub.add_parser("add", help="add a package to pack.toml")
    sub_add.set_defaults(func=add)
    sub_add.add_argument("package", help="the package to add")
    #edit
    sub_edit = sub.add_parser("edit", help="edit the pack.toml file")
    sub_edit.add_argument("editor", help="the editor to use, defaults to nano", nargs="?", default="nano")
    sub_edit.set_defaults(func=edit)
    
    #run
    sub_run = sub.add_parser("run", help="run a specefied command")
    sub_run.add_argument("command", help="the command to run")
    sub_run.set_defaults(func=run_arbitrary)

    args = parser.parse_args()
    if args.file:
        toml_file = args.file
    args.func(args)


if __name__ == "__main__":
    setup_parser()
