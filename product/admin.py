from django.contrib import admin
from product.models import *

my_models = [ProductImage, Product, CPMapper, CVMapper, Category, Attribute, AttributeChoiceValue, Vicinity, City,
             VPMapper]
admin.site.register(my_models)
# Register your models here.
