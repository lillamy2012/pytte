import os, re, string


def read():
    file = open('kit.txt', 'r')
    l=0
    for line in file:
        l=l+1
        match = re.search('Kittype', line)
        if not match:
            data = line.split()
            kittype = data[0]
            subtype = data[1]
            comment = data[2]
            name = data[3]
            comp = data[4]
            loc = data[5]
            op = data[6]
            pr =data[7]
            st = data[8]
            add_kit(kittype=kittype,subtype=subtype,comment=comment,name=name,company=comp,location=loc,opened=op,protocol=pr,stock=st)
            print kittype
        if match:
            print "match"

def add_kit( kittype,subtype,comment, name, company, location,opened,protocol,stock):
    obj, created = Kit.objects.get_or_create(kittype = kittype, subtype=subtype, comment=comment, name=name, company=company, location=location,opened=opened,protocol=protocol,stock=stock,active=True)
    return(obj)


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kopf.settings')
    from lookup.models import Kit
    read()