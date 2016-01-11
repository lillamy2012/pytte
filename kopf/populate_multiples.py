import os
import csv


def populate():

    with open('lanesAndFlows.csv', 'rb') as csvfile:
        multreader = csv.reader(csvfile, delimiter=';', quotechar='^')
        for row in multreader:
            if (row[4]=="use:ok"):
                name = row[0]
                mdsum = row[3]
                storage = row[1]
                barcode = row[5]
                #print(barcode)
                s=add_multiplex(name=name,storage=storage,mdsum=mdsum,barcode=barcode)
                for sample in barcode.split(','):
                    id=(sample.split(':')[0])
                    update_w_multiplex(id,s)

def add_multiplex(name,storage,mdsum,barcode):
    obj, created = Multiplex.objects.get_or_create(name=name,storage=storage,mdsum=mdsum,barcode=barcode)
    return(obj)

def update_w_multiplex(id,multiplex):
    obj=Annotation.objects.filter(pk=id).update(multi=multiplex)
    return(obj)

if __name__ == '__main__':
    print "Starting script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kopf.settings')
    from lookup.models import Annotation, Scientist, Project, Multiplex
    populate()
