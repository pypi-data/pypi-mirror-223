# Development

To develop the package first install its dependencies. Open the _Python Command Prompt_ or _Python PowerShell Prompt_ and type

```shell
conda install --file requirements.txt --file requirements_test.txt --file docs/requirements_docs.txt
```

To make the package usable in you Python installation install it in ``--editable`` mode:

```shell
pip install --no-deps --editable .
```
