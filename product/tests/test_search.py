from django.test import TestCase

from product.models import *


class Search(TestCase):
    def setUp(self):
        self.app = AppManager.objects.create()
        self.city = City.objects.create(name="Tehran")
        self.vic = Vicinity.objects.create(name="mahmood-abad", _city=self.city)
        self.vic2 = Vicinity.objects.create(name="mahmood-abad2", _city=self.city)
        self.cat = Category.objects.create(name="cat-1")
        self.cat2 = Category.objects.create(name="cat-2")
        self.p1 = Product.objects.create(name='p_1', description="1111", category=self.cat, price=10000,
                                         vicinity=self.vic)
        self.p2 = Product.objects.create(name='p_2', description="1111", category=self.cat, price=10000,
                                         vicinity=self.vic2)
        self.p3 = Product.objects.create(name='p_3', description="1111", category=self.cat2, price=10000,
                                         vicinity=self.vic)
        self.p4 = Product.objects.create(name='p_4', description="1111", category=self.cat2, price=10000,
                                         vicinity=self.vic2)

    def test_ssss(self):
        s = self.app.search(self.city, [self.vic.name, self.vic2.name], category=self.cat2.name).order_by("id")
        p = Product.objects.filter(name__in=[self.p3.name, self.p4.name]).order_by("id")
        print(s)
        print(p)
        self.assertEqual(list(s), list(p))
