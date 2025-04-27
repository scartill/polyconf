import voluptuous as vo
import polyconf as pc

schema = vo.Schema({
    vo.Required('person'): vo.Schema({
        vo.Required('name'): str,
        vo.Required('score'): float
    }),
})

config = pc.Configurator(schema)

# Basic dict
config.load({'person': {'name': 'John', 'score': 30.0}}, format='dict')
print('Value from dict:', config.person.name)

# INI
ini = '''
[person]
name = John
score = 30.0
'''

config.load(ini, format='ini')
print('Value from INI:', config.person.name)

# YAML
yaml = '''
person:
  name: John
  score: 30.0
'''

config.load(yaml, format='yaml')
print('Value from YAML:', config.person.name)

# JSON
json = '''
{
    "person": {
        "name": "John",
        "score": 30.0
    }
}
'''

config.load(json, format='json')
print('Value from JSON:', config.person.name)

# TOML
toml = '''
[person]
name = "John"
score = 30.0
'''

config.load(toml, format='toml')
print('Value from TOML:', config.person.name)

config.process_args()
print('Value from CLI:', config.person.name)

print("Don't forget to try with --help")
