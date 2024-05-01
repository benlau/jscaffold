JScaffold 
=========

JScaffold is a library for quickly building user interfaces in Jupyter to manipulate configuration from differnt sources (e.g .env, json) and run shell script or callback.

This project is still under development. Use it at your own risk.

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
Once the submit button is pressed, it will save the changes back to the input if possible, and then run scripts/functions.

By using different forms repeatedly, an application can be built for various purposes

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

- [ ] Run requests example

# Case Study

1. Complicated Application

- [ ] TODO

# API

## FormPanel

```python
from jscaffold import form, FormPanel
```

### form()

The `form` function serves as a shortcut for creating a FormPanel based on inputs and callback scripts or functions.

It accepts a list of Inputable objects (e.g., EnvVar, EnvFileVar, JsonFileVar), which can be passed directly as arguments or wrapped in a list.

If a string is passed, it will automatically be converted to a SharedVar.

Remarks: You should use `form` to create FormPanel instead of creating a FormPanel directly.

Example:

```python
from jscaffold import form, EnvVar
var1 = EnvVar("VAR1")
var2 = EnvVar("VAR2")
form(var1,var2)
form([var,var2])
form("VAR3") # It will be replaced by a `SharedVar` automatically.
```
### FormPanel.title(title:str)

Set the title of the form

Example Usage:

```python
form(var).title("Title of the form")
```

### FormPanel.run(*args)

Configure runnables that will be executed when the form is submitted.

- `*args`: A list of runnable items to execute upon form submission.

Example Usage:

```python
form().run("""
ls
""")

form().run(lambda log: log("Done"))
```

- [ ] Explain more

### FormPanel.action_label(label:str)

Set the label of action button (default: "Submit") 

- `label`: The label

Example Usage:

```python
form(var).action_label("OK")
```

### FormPanel.save_changes(value:bool)

Configure whether to save changes when the form is submitted.

- `value`: Boolean flag to save changes (True) or discard them (False).

Example Usage:

```python
form().save_changes(True)
```

### FormPanel.instant_update(value:bool)

Enable or disable instant updates for the form.

- `value`: Boolean flag to turn instant updates on (True) or off (False).

Example Usage:

```python
form().instant_update(True)
```

## EnvVar

This class provides a wrapper for read/write environment variable. 
It implemented the `Formattable` and `Valuable` interfaces.

The constructor:

```python
EnvVar(key: str)
```

- `key`: The key name of the environment variable.

Example Usage:

```python
from jscaffold import EnvVar
var = EnvVar("ENV")
print(var.value) # Read from the env var "ENV"
var.update("dev") # Set "ENV" to dev
```

## JsonFileVar

This class provides a wrapper for read/write a field inside a JSON file.
It implemented the `Formattable` and `Valuable` interfaces.

The constructor:

```
JsonFileVar(key: str, filename: str)
```

- `key`: The key associated with the variable.
- `filename`: The name of the JSON file.

Example Usage:

```python
from jscaffold import JsonFileVar
json_var = JsonFileVar("config", "settings.json")
```

### JsonFileVar.indent(indent: int)

Set the indentation level for the JSON output.

- `indent`: The number of spaces used for indentation in the JSON file.

Example Usage:

```python
json_var.indent(4)
```

### JsonFileVar.path(value: str)

Set the JSON path where the variable will be read or written.

- `value`: The path within the JSON structure.

Example Usage:

```python
json_var.path("a.b.c")
```

### JsonFileVar.source(filename: str, indent=None)

A context manager for creating `JsonFileVar` instances with a common source file and optional indentation.

- `filename`: The name of the JSON file.
- `indent`: Optional indentation level for the JSON output.

Example Usage:

```python
with JsonFileVar.source("data.json", indent=4) as src:
    json_var1 = src.var("version")
    json_var2 = src.var("name")
```

