from django.test import TestCase
from product.models import *


class GetCategoryProducts(TestCase):
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

        print("city products:", self.city.get_products())
        print("vicinity1 products:", self.vic.get_products())
        print("category1 products:", self.cat.get_products())
        print("vicinity2 products:", self.vic2.get_products())
        print("category2 products:", self.cat2.get_products())
        if self.city.get_products() and self.vic.get_products() and self.cat.get_products() and self.vic2.get_products() and self.cat2.get_products():
            return True
        else:
            return False
