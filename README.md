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

![jscaffold-concept](https://github.com/benlau/jscaffold/assets/82716/39c9be21-f19f-43f7-97e1-1611ef99ec72)

The basic element is a form that is rendered based on the types/format of the input source. 
Once the confirm button is pressed, it will save the changes back to the input if possible, and then run scripts/functions."

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

![image](https://github.com/benlau/jscaffold/assets/82716/cf425d02-93ce-4f39-911c-f4561bcbb859)


### Pick a file and pass to a shell script

```python
from jscaffold import form, EnvVar
file = EnvVar("FILE").local_path()
script = '''
wc -l $FILE
'''
form(file, script).title("Count line")
```

- [ ] Run requests


# API

## FormPanel

```python
from jscaffold import form

# Definition
def form(*inputs)
```

The `form` function is a shortcut to create a FormPanel that renders a form UI based on optional inputs and callback scripts/functions.

This accepts a list of Inputable objects (e.g., EnvVar, EnvFileVar, JsonFileVar) passed as an array by any number of arguments.

In case you pass a string, it will be converted to SharedVar automaticall
Example:

```
from jscaffold import from, EnvVar
var1 = EnvVar("VAR1")
var2 = EnvVar("VAR2")
form(var1,var2)
form([var,var2])
form("VAR3") # It will be replaced by a `SharedVar` automatically.
```
### title

```
class FormPanel
   def title(self, value: string):
```

Set the title of the form

### action_label

```
class FormPanel
  def action_label(self, value: string):
```

Set the label of action button (default: "Confirm") 

## Data sources

### EnvFile

```
from jscaffold import EnvFile
```


