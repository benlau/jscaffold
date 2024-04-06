JScaffold 
=========

JScaffold is a library for building user interface inside Jupyter quickly. It could manipulate configuration from .env and json files.

This project is still under development. Use it as your own risk.

**Features:**

- Read/write .env, json file
- Read/write assignment operation in several programming languages
- Configuration Interface
    - Generate from muiltiple source (.env, json, source code)
    - Auto update on changes from other Jupyter cell
- Process Control Interface (WIP)

# Introduction

Instead of bundling too many features into a UI and making it complicated, it is recommended to spread the features across individual Jupyter cells, with each cell doing just one thing. JScaffold is designed for this purpose.

The main element in JScaffold is a UI form that can read from a field in a .env or .json file as input and then update it. Users may also execute a function or script instead of just saving the value. By repeating this form, an application can be built for various purposes.

## Edit .env and package.json

```python
from jscaffold import form, EnvFileVar, JsonFileVar
env = EnvFileVar("ENV", ".env")
version = JsonFileVar("version", "package.json").indent(4)
form([env, version])
```

- [ ] Example of running script / program

# Example Usage

## UI for editing .env file

```python
from jscaffold import EnvVarFile, ConfigPanel
HOST=EnvVarFile("HOST", ".env")
API_KEY=EnvVarFile("API_KEY", ".env")
ConfigPanel([HOST, API_KEY]).show()
```


