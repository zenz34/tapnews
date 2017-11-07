import yaml
import json

with open('backend_conf.yaml', 'r') as stream:
    config = yaml.load(stream)
    #print config
    jason = json.dumps(config)
    print jason
