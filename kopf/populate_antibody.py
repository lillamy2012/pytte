import os, re, string, codecs


def read():
    file = open('antibodies.txt', 'r')
    l=0
    for line in file:
        l=l+1
        print l
        match = re.search('Antibody', line)
        if not match:
           
            data = line.split('\t')
            print data
            ab = data[0]
            sr = data[1]
            con = data[2]
            if len(con.split()) > 0:
                con=float(con.split()[0])
            else:
                con=None
                print con
            ig = data[3]
            dil = data[4]
            sec = data[5]
                #if len(sec.split()) > 0:
                #sec=int(sec.split()[4])
            #print sec
            siz = data[6]
            com = data[7]
            loc = data[8]
            ll=loc.split()
            try:
                ll[5]=loc.split()[5].replace("micro",u"\u00B5",1)
            except IndexError:
                print "no such"
            loc=' '.join( ll )
            print loc
            
            if len(dil.split()) > 0:
                dil=int(dil.split()[0])
            else:
                dil=None
                print dil
            print com
            add_antibody(antibody=ab,source=sr,ig_type=ig,dilution_western=dil,secondary_western=sec,location_work=loc,location_storage="",comment="",active=True,antigen_used="",company=com,protein_size=siz)
            
        if match:
            print "match"


def read2():
    file = open('antibodies2.txt', 'r')
    l=0
    for line in file:
        l=l+1
        #print line
        match = re.search('Antibody', line)
        if not match:
            data = line.split('\t')
            ab = data[0]
            
            sr = data[1]
            #print sr
            ag = data[2]
            #print ag
            ig = data[3]
            dil = data[4]
            if len(dil.split()) > 0:
                dil=int(dil.split()[0])
            else:
                dil=None
            sec = data[5]
            #if len(sec.split()) > 0:
            #sec=int(sec.split()[4])
            #print sec
            siz = data[6]
            loc1 = data[7]
            loc2 = data[8]
            com =  data[9]
            #print lo
            print dil

            add_antibody(antibody=ab,source=sr,ig_type=ig,dilution_western=dil,secondary_western=sec,location_work=loc1,location_storage=loc2,comment=com,active=True,antigen_used=ag,company="",protein_size=siz)
        
        if match:
            print "match"





def add_antibody( antibody, antigen_used,source,ig_type,dilution_western, secondary_western, protein_size,company, location_work,location_storage, comment,active):
    obj, created = Antibody.objects.get_or_create(antibody = antibody, antigen_used=antigen_used, ig_type=ig_type, dilution_western=dilution_western,
    protein_size=protein_size,location_work=location_work,location_storage=location_storage, source = source, comment = comment, active=active,secondary_western=secondary_western,company=company)
    return(obj)


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kopf.settings')
    from lookup.models import Antibody
    read()
    read2()