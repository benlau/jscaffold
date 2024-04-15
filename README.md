JScaffold 
=========

JScaffold is a library for building user interface in Jupyter quickly. 
And it could manipulate configuration from .env and json files.

This project is still under development. Use it as your own risk.

**Features:**

- Common Format File Read/Write
    - Read/write .env, json file
    - Read/write assignment operation in several programming languages
- A Form-Based Configuration Interface
    - Generate from muiltiple source (.env, json, source code)
    - Auto update on changes from other Jupyter cell

# Introduction

Instead of bundling too many features into a UI and making it complicated, 
it is recommended to spread the features across individual Jupyter cells, 
with each cell doing just one thing. That is the design philosophy of JScaffold.

The main element in JScaffold is a UI form that can read from a field in a .env or .json file as input and then update it. 
Users may also execute a function or script instead of just saving the value. 
By repeating different forms, an application can be built for various purposes.

- [ ] Link to Demo notebook

## Examples

### Edit .env and package.json

```python
from jscaffold import form, EnvFileVar, JsonFileVar
env = EnvFileVar("ENV", ".env").select("dev", "staging", "prod")
version = JsonFileVar("version", "package.json").indent(4)
form([env, version])
```

![image](https://github.com/benlau/jscaffold/assets/82716/a93bf92a-74c8-460d-bf55-2a89e55258d4)

### Pick a file and pass to a shell script

```python
from jscaffold import form, EnvVar
file = EnvVar("FILE").local_path()
script = '''
wc -l $FILE
'''
form(file, script).title("Count line")
```

- [ ] Run shell script

- [ ] Run requests



