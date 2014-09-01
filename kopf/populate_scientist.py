import os


def populate():
    data=read_json('sample_berger.json')
    for d in data:
        if d['group']=="Berger":
            add_scientist(name=d['scientist'])


def read_json(jsonf):
    with open(jsonf, 'r') as json_file:
        data = json.load(json_file)
    return data


def add_scientist(name):
    obj, created = Scientist.objects.get_or_create(name = name)
    return(obj)



if __name__ == '__main__':
    print "Starting scientist population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kopf.settings')
    from lookup.models import Scientist
    import json
    populate()