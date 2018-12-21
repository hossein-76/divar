from django.test import TestCase
from product.models import *

class AddProduct(TestCase):
    def setUp(self):
        city = City.objects.create(name="Tehran")
        vic = Vicinity.objects.create()
