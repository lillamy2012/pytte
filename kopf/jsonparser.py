import json
from pprint import pprint
from lookup.models import Annotation

with open('sample_berger.json') as data_file:
    data = json.load(data_file)

for d in data:
    if d['group']=="Berger":
        a=Annotation(scientist=d['scientist'],sample=d['id'],genotype=d['genotype'],
                     descr=d['descr'],exptype=d['exptype'],comments=d['comments'],
                     tissue_type=d['tissue_type'],preparation_type=d['preparation_type'],
                     organism=d['organism'],celltype=d['celltype'],antibody=d['antibody'])
        a.save()






