import os


def populate():
    ss = range(15351, 15362)
    add_project(scientist="Danhua",project_name="HTB2_HTB3",sampleL=ss)





def add_project(scientist, project_name,sampleL):
    obj,created = Project.objects.get_or_create(primary_scientist=scientist,project_name=project_name)
    obj.save()
    obj.samples=sampleL
    return(obj)


if __name__ == '__main__':
    print "Starting Lookup population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kopf.settings')
    from lookup.models import Project
    populate()