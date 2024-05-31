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
See [installation](https://github.com/ellipse12/Pack/wiki/Installation) for installation help.

Pack works with TOML to provide a declarative way to list your packages. An example configuration on a debian based system might be:
```toml
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
