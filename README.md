# Pack
A simple declarative package manager
> [!WARNING]
> Pack is in its early stages of development. Expect Bugs!
# Requirements
Pack requires python 3.x and also requires tomlkit to be installed. TomlKit can be installed using a python package manager, such as pip
```
pip install tomlkit
```
# Getting Started
To get started with pack download _pack.py_ and run it using `python3 pack.py [options]` by default pack will search the current directatory for a `pack.toml` file. Alternatively a bash script has been provided that will set the search directetory to be at "$HOME/.pack" and then you will just need to call it using `pack` without the python syntax. (note you will likely have to change the permissions of the bash script using something like: `chmod u+x pack`)

Pack works with TOML to provide a declarative way to list your packages out. An example configuration might be:
```TOML
[pack]
system = "apt"
packages = ["nvim", "git", "vscode"]
[system.apt.packages]
nvim = "neovim"
git = "git"
vscode = "vscode"
[system.apt.commands]
install = "sudo apt-get install ${package.id}"
```
