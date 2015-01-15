import os, re, string


def read():
    file = open('antibodie_clean.txt', 'r')
    l=0
    for line in file:
        l=l+1
        match = re.search('Antibody', line)
        if not match:
            data = line.split()
            ab = data[0]
            sr = data[1]
            cm = data[2]
            add_antibody(antibody=ab,source=sr,comment=cm)
        #print ab
        if match:
            print "match"

def add_antibody( antibody, source, comment):
    obj, created = Antibody.objects.get_or_create(antibody = antibody, source = source, comment = comment)
    return(obj)


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kopf.settings')
    from lookup.models import Antibody
    read()