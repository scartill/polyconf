import voluptuous as vo
import polyconf as pc

schema = vo.Schema({
    vo.Required('person'): vo.Schema({
        vo.Required('name'): str,
        vo.Required('age'): vo.All(int, vo.Range(min=0, max=120)),
    }),
})

config = pc.Configurator(schema)

# Basic dict
config.load({'person': {'name': 'John', 'age': 30}}, format='dict')
print(config.person.name)

# INI
ini = '''
[person]
name = John
age = 30
'''

config.load(ini, format='ini')
print(config.person.name)

# YAML
yaml = '''
person:
  name: John
  age: 30
'''

config.load(yaml, format='yaml')
print(config.person.name)

# JSON
json = '''
{
    "person": {
        "name": "John",
        "age": 30
    }
}
'''

config.load(json, format='json')
print(config.person.name)

# TOML
toml = '''
[person]
name = "John"
age = 30
'''

config.load(toml, format='toml')
print(config.person.name)
