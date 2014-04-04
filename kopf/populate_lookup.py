import os


def populate():
    
    data=read_json('sample_berger.json')

    for d in data:
        if d['group']=="Berger":
            s=add_scientist(name=d['scientist'])
            add_annotation(scientist=s,sample=d['id'],genotype=d['genotype'], descr=d['descr'],comments=d['comments'],tissue_type=d['tissue_type'],preparation_type=d['preparation_type'],organism=d['organism'],celltype=d['celltype'],antibody=d['antibody'])

    ss = range(15351, 15362)
    s,a=Scientist.objects.get_or_create(name="Danhua Jiang")
    add_project(scientist=s,project_name="HTB2_HTB3",sampleL=ss)
    

def read_json(jsonf):
    #print(json)
    with open(jsonf, 'r') as json_file:
        data = json.load(json_file)
    return data


def add_annotation(scientist, sample, genotype, descr, comments, tissue_type, preparation_type, organism, celltype,antibody):
    obj, created = Annotation.objects.get_or_create(scientist = scientist, sample = sample, genotype = genotype, descr = descr, comments = comments, tissue_type = tissue_type, preparation_type = preparation_type, organism = organism, celltype=celltype,antibody=antibody)
    return(obj)

def add_scientist(name):
    obj, created = Scientist.objects.get_or_create(name = name)
    return(obj)

def add_project(scientist, project_name,sampleL):
    obj,created = Project.objects.get_or_create(primary_scientist=scientist,project_name=project_name)
    obj.save()
    obj.samples=sampleL
    return(obj)



if __name__ == '__main__':
    print "Starting Lookup population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kopf.settings')
    from lookup.models import Annotation, Scientist, Project
    import json
    populate()