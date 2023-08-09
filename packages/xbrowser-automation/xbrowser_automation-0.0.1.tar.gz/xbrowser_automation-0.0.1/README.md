[![pipeline status](https://git.benteler.net/czirala/xbrowser_automation/badges/main/pipeline.svg)](https://git.benteler.net/czirala/xbrowser_automation/commits/main)
[![coverage report](https://git.benteler.net/czirala/xbrowser_automation/badges/main/coverage.svg)](https://git.benteler.net/czirala/xbrowser_automation/commits/main)

# xbrowser_automation

xbrowser gui

## Installation & setup

### Install Python

As this is a Python package, please install a Python version first. We recommend to use our own [BENTELER Anaconda Installer](https://git.benteler.net/python/python-installer), see some instructions in our [Python wiki](https://python.pods.benteler.net/)

### Install `xbrowser_automation`

Afterwards you can install the package by opening the _Python Command Prompt_ or _Python PowerShell Prompt_ and type

```shell
conda install xbrowser_automation
```

## Usage

```python
import xbrowser_automation
```

## Development

To develop the package first install its dependencies. Open the _Python Command Prompt_ or _Python PowerShell Prompt_ and type

```shell
conda install --file requirements.txt --file requirements_test.txt --file docs/requirements_docs.txt
```

To make the package usable in you Python installation install it in ``--editable`` mode:

```shell
pip install --no-deps --editable .
```
