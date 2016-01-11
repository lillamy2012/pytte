import os


def populate():
    
    data=read_json('group.json')

    for d in data:
        if d['group']=="Berger" and d['status']=="Ready":
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
    cl_genotype = autouni(removehash(genotype))
    cl_antibody = autouni(removehash(antibody))
    cl_tissue_type = autouni(removehash(tissue_type))
    obj, created = Annotation.objects.get_or_create(scientist = scientist, sample = sample, genotype = cl_genotype, descr = descr, comments = comments, tissue_type = cl_tissue_type, preparation_type = preparation_type, organism = organism, celltype=celltype,antibody=cl_antibody,exptype=exptype)
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

def autouni(string):
    corr={}
    corr['Col WT'] = ['Col','WT','Col WT','wildtype']
    corr['atrx025'] = ['atrx025','atrx 025']
    corr['10 day old seedling'] = ['10-d old seedling','10-d old seedlings','10-d old Seedling','10-d old Seedlings','10 day old seedling','10 day old seedlings','10 day old Seedling','10 day old Seedlings','10 day seedling','10 day seedlings', '10 day Seedlings']
    corr['Somatic'] = ['Somatic','somatic','Somatics','somatics']
    corr['Root'] = ['Root','Roots','root','roots']
    corr['PolII'] =['Pol II','PolII']
    corr['input'] = ['Input','INPUT']
    for key,value in corr.items():
        if string in value:
            new=key
    if not 'new' in locals():
        new = string
    return(new)

def removehash(string):
    head, sep, tail = string.partition('#')
    return(head)








if __name__ == '__main__':
    print "Starting Lookup population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kopf.settings')
    from lookup.models import Annotation, Scientist, Project
    import json
    populate()
    populate_path()
#removehash('kyp h2a.w #1')