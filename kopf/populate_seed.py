import os


def add_seed(type,line,ecotype,source,selection,genotype,location,label,comment,date):
    obj,created = Seed.objects.get_or_create(type=type,linename=line,ecotype=ecotype,source=source,selectionmark=selection,genotypeprimer=genotype,location=location,label=label,comment=comment,date=date)
    obj.save()
    return(obj)

def add_relation(offspring,p1):
    obj,created = SeedRelation.objects.get_or_create(offspring=offspring,parent=p1)
    obj.save()
    return(obj)

def add_contact(seed,contact):
    obj,created = SeedContact.objects.get_or_create(seed=seed,contact=contact)
    obj.save()
    return(obj)

def populate():
    li = "h2a.w.6"
    ty = "mutant"
    ec = "Col"
    source = "SALK_024544.32.30.x"
    sel = ""
    ge = ""
    cp = "Zdravko"
    location ="Seed box #1 ZL"
    date = "2015-11-26"
    label=""
    comment=""
    add_seed(ty,li,ec,source,sel,ge,location,label,comment,date)
    seed = Seed.objects.get(pk=1)
    add_contact(seed,cp)
    add_contact(seed,"extra")
    li = "H2A.W.6::HA"
    ty = "transgene"
    ec = "Col"
    source = "SAIL_84_B01 (N803958)"
    sel = ""
    ge = ""
    cp = "Zdravko"
    location ="Seed box #1 ZL"
    date = "2015-11-26"
    label=""
    comment=""
    add_seed(ty,li,ec,source,sel,ge,location,label,comment,date)
    seed = Seed.objects.get(pk=2)
    add_contact(seed,cp)
    li = "HHH"
    ty = "transgene"
    ec = "Col"
    source = "Zdravko"
    sel = ""
    ge = ""
    cp = "Zdravko"
    location ="Seed box #1 ZL"
    date = "2015-11-26"
    label=""
    comment=""
    add_seed(ty,li,ec,source,sel,ge,location,label,comment,date)
    seed = Seed.objects.get(pk=3)
    add_contact(seed,cp)
    #p1 = Seed.objects.get(linename="h2a.w.6")
    #p2 = Seed.objects.get(linename="H2A.W.6::HA")
    #offspring = Seed.objects.get(cp="Zdravko")
    #add_relation(offspring,p1)
#add_relation(offspring,p2)

if __name__ == '__main__':
    print "Starting Seed population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kopf.settings')
    from lookup.models import Seed, SeedRelation, SeedContact
    populate()




