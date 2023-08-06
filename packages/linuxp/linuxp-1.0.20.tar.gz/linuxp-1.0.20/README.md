<img src="https://github.com/linux-profile/linux-profile/blob/master/docs/linuxp.png?raw=true">

![GitHub Org's stars](https://img.shields.io/github/stars/linux-profile?label=LinuxProfile&style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/linux-profile/linux-profile?style=flat-square)
![PyPI](https://img.shields.io/pypi/v/linuxp?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/linuxp?style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/linuxp?style=flat-square)

[![check](https://github.com/linux-profile/linux-profile/actions/workflows/python-publish-pypi.yml/badge.svg)](https://github.com/linux-profile/linux-profile/actions/workflows/python-publish-pypi.yml)
[![check](https://github.com/linux-profile/linux-profile/actions/workflows/python-publish-pypi-test.yml/badge.svg)](https://github.com/linux-profile/linux-profile/actions/workflows/python-publish-pypi-test.yml)
[![check](https://github.com/linux-profile/linux-profile/actions/workflows/python-app-test.yml/badge.svg)](https://github.com/linux-profile/linux-profile/actions/workflows/python-app-test.yml)
![](docs/coverage.svg)

---

- **Documentation**: [https://docs.linuxprofile.com](https://docs.linuxprofile.com)
- **Source Code**: [https://github.com/linux-profile/linux-profile](https://github.com/linux-profile/linux-profile)

---

## [Introduction](https://docs.linuxprofile.com/)

**English**: **Linuxp** is a CLI tool for Linux profile management. With this project it is possible, from commands executed in the console, to create a file in **json** format to store the backup settings. For example, information about packages, aliases, scripts, texts and files. It also allows with a single command to restore the saved settings.

> **Português**: **Linuxp** é uma ferramenta de CLI para gerenciamento de perfil do Linux. Com este projeto é possível, a partir de comandos executados no console, criar um arquivo no formato **json** para armazenar as configurações de backup. Como por exemplo, informações sobre pacotes, alias, scripts, textos e arquivos. Também permite com um único comando restaurar as configurações salvas.

## [Why?](https://docs.linuxprofile.com/)

**English**: With the need to automate processes and execution of scripts, **Linuxp** emerged, a project developed in python that aims to create a standard in the chaos of storing information about packages, aliases, scripts, texts and files in a single place, fully customizable from according to the user.

> **Português**: Com a necessidade de automatizar os processos e execução de scripts, surgiu **Linuxp**, projeto desenvolvido em python que tem como objetivo criar um padrão no caos do armazenamento de informações de pacotes, alias, scripts, textos e arquivos em um único local, totalmente personalizável de acordo com o usuário.

### Quick URLs

- Last Version -> [https://linuxprofile.com/LAST_VERSION](https://linuxprofile.com/LAST_VERSION)
- Installation -> [https://linuxprofile.com/install.sh](https://linuxprofile.com/install.sh)
- Uninstallation -> [https://linuxprofile.com/uninstall.sh](https://linuxprofile.com/uninstall.sh)

## [Installation](https://docs.linuxprofile.com/nav/installation/)

- **PIP**

      pip install linuxp

- **Poetry**

      poetry add linuxp

- **Bash/Curl**

      /bin/bash -c "$(curl -fsSL https://linuxprofile.com/install.sh)"

- **Pacman**

      git clone https://github.com/linux-profile/linux-profile.git
      cd linux-profile
      makepkg
      sudo pacman -U linux-profile-1.0.19-1-any.pkg.tar.zst

## [Uninstallation](https://docs.linuxprofile.com/nav/uninstallation/)

- **PIP**

      pip uninstall linuxp

- **Poetry**

      poetry remove linuxp

- **Bash/Curl**

      /bin/bash -c "$(curl -fsSL https://linuxprofile.com/uninstall.sh)"

- **Pacman**

      sudo pacman -R linux-profile

## [Commands](https://docs.linuxprofile.com/)

| Command               | Description                                                                           | Docs                                   |
|:--------------------- |:------------------------------------------------------------------------------------- | :------------------------------------: | 
| ``linuxp config``     | Settings file management.                                                             | [Link](https://docs.linuxprofile.com/nav/commands/config/) |
| ``linuxp profile``    | Profile file management.                                                              | [Link](https://docs.linuxprofile.com/nav/commands/profile/) |
| ``linuxp add``        | Parameter used to add a new item to the list in your profile file.                    | [Link](https://docs.linuxprofile.com/nav/commands/add/) |
| ``linuxp remove``     | Removes items from the profile file.                                                  | [Link](https://docs.linuxprofile.com/nav/commands/remove/) |
| ``linuxp install``    | This parameter is used to install the modules, **package**, **alias** and **script**. | [Link](https://docs.linuxprofile.com/nav/commands/install/) |
| ``linuxp uninstall``  | Command used to uninstall items. Be **very careful** when running.                    | [Link](https://docs.linuxprofile.com/nav/commands/uninstall/) |
| ``linuxp list``       | Lists all modules in the terminal and can also apply filters to find items.           | [Link](https://docs.linuxprofile.com/nav/commands/list/) |

## Example Profile File

- Link - [linux_profile.json](https://linuxprofile.com/linux_profile.json)

## Commit Style

- ⚙️ FEATURE
- 📝 PEP8
- 📌 ISSUE
- 🪲 BUG
- 📘 DOCS
- 📦 PyPI
- ❤️️ TEST
- ⬆️ CI/CD
- ⚠️ SECURITY

## License

This project is licensed under the terms of the MIT license.
