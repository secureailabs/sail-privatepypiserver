# sail-privatepypiserver

currently this code is running at ```172.20.0.5``` in the azure cloud within our vpn\

## deployment instuctions
install arin-core-azure but some means \

```python deploy.py```\

The script will find the right machine on azure and install and start a pipy server there

## release instructions

Set the following environment variables

```export SAIL_PYPI_REPOSITORY_URL="http://172.20.0.5"```\
```export SAIL_PYPI_USERNAME="common"```\
```export SAIL_PYPI_PASSWORD="oi,_geeFqMH7qk&utyoRng%V"```

in arin-azure-core there is an example of a release script (release.py) that will pick these up and deploy wheels to the server

## conspumtion instructions

1. find where your global pip config file is\
```pip config -v list```\
for me this was ```'C:\ProgramData\pip\pip.ini'```

2. Add the following lines to the config file\
```[global]```\
```index-url = http://172.20.0.5```\
```trusted-host = 172.20.0.5```\
```extra-index-url= http://common:oi,_geeFqMH7qk&utyoRng%V@http://172.20.0.5```

3. you can now install private dependancies\
```pip install arin-core-azure```\
You will get a waringing about it happening over http but since it is over a vpn this is not the end of the world