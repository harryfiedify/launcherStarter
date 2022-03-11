# launcherStarter
 
A small Python script for starting game launchers. 

It will start up a list of executables in sequential order, and wait for system usage (network traffic, CPU, disk I/O) to stabilise before continuing.

## Installation & Usage

Install Python 3 to PATH. Customize `config-example.yml` to your liking and save as `config.yml`. Start by executing `run.bat`.

Optionally, you can supply a different config file as an argument:
`python launcherStarter.py file.yml`

