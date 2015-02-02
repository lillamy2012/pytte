import os, re, string


def populate():
    
    data=read_json('dump1.json')
    
    for e in data:
        if e['model']=="lookup.kit":
            name = e['pk']
            for key, value in e.iteritems():
                if key == 'fields':
                    for fields, text in value.iteritems():
                        if fields == 'kittype':
                            kittype = text
                        
                        if fields == 'comment':
                            comment = text
                        
                        if fields == 'company':
                            company = text
                        
                        if fields == 'location':
                            location = text
                        
                        if fields == 'opened':
                            opened = text
                        
                        if fields == 'stock':
                            stock = text
                        
                        if fields == 'active':
                            active = text
                        
                        if fields == 'subtype':
                            if text == "Rpu":
                                subtype="Purification"
                            elif text == "Rsq":
                                subtype="RNAseq"
                            elif text == "pol":
                                subtype="Polymerase"
                            elif text =="RTPCR":
                                subtype="qPCR"
                            else:
                                 subtype=text

            add_kit(kittype = kittype, subtype = subtype, comment = comment, name = name, company = company, location = location, opened = opened, stock = stock, active=active)





def read_json(jsonf):
    #print(json)
    with open(jsonf, 'r') as json_file:
        data = json.load(json_file)
    return data

def add_kit(kittype, subtype, comment, name, company, location, opened, stock, active ):
    obj, created = Kit.objects.get_or_create(kittype = kittype, subtype = subtype, comment = comment, name = name, company = company, location = location, opened = opened, stock = stock, active=active )
    return(obj)



if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kopf.settings')
    from lookup.models import Kit
    import json
    populate()










#changes =