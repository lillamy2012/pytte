import django_tables2 as tables
from lookup.models import Seed, SeedContact

class SeedTable(tables.Table):
    #one = tables.Column(accessor='seedcontact.contact')
    #first = tables.Column(accessor='seedrelation')
    #last = tables.Column(accessor='seed.ecotype')
    myid = tables.Column(accessor='seed.pk')
    class Meta:
        model = SeedContact
#attrs = {"class": "paleblue"}
        fields = ('contact',)
        sequence = ('myid',)
