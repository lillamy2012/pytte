import os


def populate():
    
    data=read_json('group.json')

    for d in data:
        if d['group']=="Berger":
            s=add_scientist(name=d['scientist'])
            add_annotation(scientist=s,sample=d['id'],genotype=d['genotype'].rstrip(), descr=d['descr'],comments=d['comments'],tissue_type=d['tissue_type'],preparation_type=d['preparation_type'],organism=d['organism'],celltype=d['celltype'],antibody=d['antibody'],exptype=d['exptype'])

    ss = range(15351, 15362)
    s,a=Scientist.objects.get_or_create(name="Danhua Jiang")
    add_project(scientist=s,project_name="HTB2_HTB3",sampleL=ss)
    

def read_json(jsonf):
    #print(json)
    with open(jsonf, 'r') as json_file:
        data = json.load(json_file)
    return data


def add_annotation(scientist, sample, genotype, descr, comments, tissue_type, preparation_type, organism, celltype,antibody,exptype):
    obj, created = Annotation.objects.get_or_create(scientist = scientist, sample = sample, genotype = genotype, descr = descr, comments = comments, tissue_type = tissue_type, preparation_type = preparation_type, organism = organism, celltype=celltype,antibody=antibody,exptype=exptype)
    return(obj)

def add_scientist(name):
    obj, created = Scientist.objects.get_or_create(name = name)
    return(obj)

def add_project(scientist, project_name,sampleL):
    obj,created = Project.objects.get_or_create(primary_scientist=scientist,project_name=project_name)
    obj.save()
    obj.samples=sampleL
    return(obj)

def populate_path():
    data= open('bam_anno.tab', 'r').readlines()
    firstLine = data.pop(0)
    for line in data:
        obj=Annotation.objects.filter(pk=str(line.split()[2])).update(raw=str(line.split()[0]))
        obj=Annotation.objects.filter(pk=str(line.split()[2])).update(align=str(line.split()[3]))
    return(obj)

if __name__ == '__main__':
    print "Starting Lookup population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kopf.settings')
    from lookup.models import Annotation, Scientist, Project
    import json
    populate()
    populate_path()