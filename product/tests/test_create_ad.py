from django.test import TestCase
from product.models import *


class AddProduct(TestCase):
    def setUp(self):
        AppManager.objects.create()
        city = City.objects.create(name="Tehran")
        vic = Vicinity.objects.create(name="mahmood-abad", city=city)
        cat = Category.objects.create(name="cat-1",)
