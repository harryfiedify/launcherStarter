# launcherStarter
 
A small Python script for starting game launchers. 

It will start up a list of executables in sequential order, and wait for system usage (network traffic, CPU, disk I/O) to stabilise before continuing.

Packaged with pyinstaller.

## Installation

1. Download newest release from [here](https://github.com/harryfiedify/launcherStarter/releases)
2. Customize `config-example.yml` to your liking and save as `config.yml`. 
3. Start by executing `launcherStarter.exe`.

## Installing for development

1. Install Python 3 to PATH. 
2. Setup dependencies with `pip install -r requirements.txt` 
3. Customize `config-example.yml` to your liking and save as `config.yml`. 
4. Start by executing `run.bat`.

Optionally, you can supply a different config file as an argument:
`python launcherStarter.py file.yml`

