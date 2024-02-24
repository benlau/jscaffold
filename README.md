JScaffold 
=========

JScaffold is a Python library that provides a set of functions to build user interfaces, such as configuration and process control, for Jupyter.

This project is still under development. Use it as your own risk.

Features:

- Read/write .env, json file
- Read/write assignment operation in several programming languages
- Configuration Interface
    - Generate from muiltiple source (.env, json, source code)
    - Auto update on changes from other Jupyter cell
- Process Control Interface (WIP)

# Example Usage

## UI for editing .env file

```python
from jscaffold import EnvVarFile, ConfigPanel
HOST=EnvVarFile(".env", "HOST")
API_KEY=EnvVarFile(".env", "API_KEY")
ConfigPanel([HOST, API_KEY]).show()
```


