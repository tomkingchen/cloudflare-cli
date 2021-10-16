# cloudflare-cli
Cloudflare CLI Tool - flare 🔥

## Purpose
Talk to Cloudflare API so you don't have to. I found it's not very convenient to obtain information like Zone ID, firewall rule ID from Cloudflare Dashboard. This tool helps you to get those information easily from Cloudfalre API.

Currently it does only GET queries for most of the resources.
## How to use this tool
Clone the repo and run the code below to install the package. The tool is written in Python 3.8. I haven't tested on other version of Python3.
```
virtualenv -p /usr/bin/python3.8 venv
. venv/bin/activate
pip install --editable .
```
Save your Cloudflare API key in a yaml file under your home directory as `~/.flare.yaml`
```
API_EMAIL: jsmith@contso.com
API_KEY: abcdef.....
```

## Examples
To see available commands:
```
flare
```
To list firewall rules under a zone/site.
```
flare list-fw-rules --zoneid "abcd..."
```