from django.test import TestCase
from product.models import *


class AddProduct(TestCase):
    def setUp(self):
        self.app = AppManager.objects.create()
        self.city = City.objects.create(name="Tehran")
        self.vic = Vicinity.objects.create(name="mahmood-abad", _city=self.city)
        self.vic2 = Vicinity.objects.create(name="mahmood-abad2", _city=self.city)
        self.cat = Category.objects.create(name="cat-1")
        self.cat2 = Category.objects.create(name="cat-2")

    def test_add(self):
        p1 = Product.objects.create(name='p_1', description="1111", category=self.cat, price=10000, vicinity=self.vic)
        p2 = Product.objects.create(name='p_2', description="1111", category=self.cat, price=10000, vicinity=self.vic2)
        p3 = Product.objects.create(name='p_3', description="1111", category=self.cat2, price=10000, vicinity=self.vic)
        p4 = Product.objects.create(name='p_4', description="1111", category=self.cat2, price=10000, vicinity=self.vic2)

        print(p1)
        print(p2)
        print(p3)
        print(p4)
        if p1 and p2 and p3 and p4:
            return True
        else:
            return False
