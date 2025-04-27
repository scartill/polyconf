import voluptuous as vo
import polyconf as pc

schema = vo.Schema({
    vo.Required('name'): str,
    vo.Required('age'): vo.All(int, vo.Range(min=0, max=120)),
})

config = pc.Configurator(schema)
config.load({'name': 'John', 'age': 30, }, format='dict')
print(config.name)
