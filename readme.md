# XOXO Readme #

## prerequisite ##
- [```optional```] Visual Studio Code
- [```mandatory```] install Python (3.6.8), throughout this document i use python36 alias
- [```mandatory```] install PyQt5 (5.15.0)
- [```mandatory```] install PySide2 (5.15.1)
- [```mandatory```] install Qt Designer

## steps to run locally ##

### run directly on python file ###
- change working directory to ```root``` folder
- run the ```xoxo.py``` file with this command
```
python36 xoxo.py
```

### run the compiled exe file ###
- go to the place where the xoxo.exe file located
- make sure there's nothing missing on this project folder
- double click on the exe file

## steps to convert the ui file into python file ##
- change working directory into ```ui-template``` folder
- make sure the ```xoxo.ui``` file is listed there
- run the following command
```
python36 -m PyQt5.uic.pyuic -x xoxo.ui -o xoxo.py
```

## warnings ##
- do not modify the ui file content directly, it may cause error

## developer footnote ##
- if we want to initiate gitignore on new project, use this command after creating the ```.gitignore``` file
```
git config --global core.excludesFile ~/.gitignore
```
- if we want to check the reason behind some files are ignored by ```.gitignore``` file, use this command
```
git check-ignore -v xoxo.xml
```
