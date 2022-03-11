# launcherStarter
 
A small Python script for starting game launchers. 

It will start up a list of executables in sequential order, and wait for system usage (network traffic, CPU, disk I/O) to stabilise before continuing.

Packaged with pyinstaller.

## Installation

1. Download newest release from [here](https://github.com/harryfiedify/launcherStarter/releases)
2. Customize `config-example.yml` to your liking and save as `config.yml`. 
3. Start by executing `launcherStarter.exe`.

## Installing for development

1. Install Python 3 to *PATH*. 
2. Setup dependencies with `pip install -r requirements.txt` 
3. Customize `config-example.yml` to your liking and save as `config.yml`. 
4. Start by executing `run.bat`.
5. The executable file can be generated with *pyinstaller*.


## Config file

launcherStart.py reads its instructions from a YAML-file, typically called `config.yml`. You can supply a different config file as an argument:
`launcherStarter.exe file.yml`

In the `recipe` section of the YAML, there are two possible commands:
- `wait` for waiting for system resources, e.g. a download to finish or disk install to complete
- `launch` will start the specified executable in a separate process

You can configure standard settings for the `wait`-command in the block `defaults\wait-default` of the config file.
- `cpu|network|disk: True|False` whether the resource watcher is enabled for CPU-percentage, network incoming bandwidth or hard disk transfers
- `*-limit` (in kB/s or %) defines the upper limit of the watched resource
- `*-length` determines the length of the rolling average for the resource. Queries are made roughly once every second.
- `time` (in seconds) specifies the minimum wait time
- `timeout` (in seconds) specifies the maximum wait time

These settings can be overridden by specifying them again in the desired `wait`-block.


