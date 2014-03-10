from django import template

register = template.Library()

def get_object_field(object,field):
    
    return object._meta.get_field(field).verbose_name # put here whatever you would like to return

get_object_field = register.filter(get_object_field)