import os
import json
from pprint import pprint


def populate():# Start execution here!
    
    #with open('sample_berger.json') as data_file:
    #data = json.load(data_file)
    data=read_json('sample_berger.json')

    for d in data:
        if d['group']=="Berger":
            add_annotation(scientist=d['scientist'],sample=d['id'],genotype=d['genotype'], descr=d['descr'],comments=d['comments'],tissue_type=d['tissue_type'],preparation_type=d['preparation_type'],organism=d['organism'],celltype=d['celltype'])


    # Print out what we have added to the user.
                #for c in Annotation.objects.all():
#print "- {0}".format(str(c))




def read_json(jsonf):
    print(json)
    with open(jsonf, 'r') as json_file:
        data = json.load(json_file)
    return data


def add_annotation(scientist, sample, genotype, descr, comments, tissue_type, preparation_type, organism, celltype):
    obj, created = Annotation.objects.get_or_create(scientist = scientist, sample = sample, genotype = genotype, descr = descr, comments = comments, tissue_type = tissue_type, preparation_type = preparation_type, organism = organism, celltype=celltype)
    return(obj)






if __name__ == '__main__':
    print "Starting Rango population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kopf.settings')
    from lookup.models import Annotation
    populate()