import os, re, string


def stats():
    file = open('stats.txt', 'r')
    for line in file:
        match = re.search('X', line)
        if not match:
            head = line.split()
        if match:
            words = line.split()
            w = words[0][2:]
            id = int(w[:5])
            print id
            try:
                s=Annotation.objects.get(pk=id)
            except s.DoesNotExist:
                print "Sample does not exist"
            #print s
            #ids = Annotation.objects.get(pk = id)
            #print ids
            zero = words[17]
            tot = words[16]
            max = words[15]
    add_stats(sample =s, zeroReads = zero, totReads = tot, maxReads = max)

def add_stats( sample, zeroReads, totReads, maxReads):
    obj, created = Stats.objects.get_or_create(sample = sample, zeroReads = zeroReads, totReads = totReads, maxReads = maxReads)
    return(obj)

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kopf.settings')
    from lookup.models import Annotation, Scientist, Project, Stats
    stats()