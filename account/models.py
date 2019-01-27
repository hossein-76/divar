from django.db import models
from django.contrib.auth.models import AbstractUser
from product.models import Product
from django.contrib.auth import login as user_login, logout as user_logout


# it has username and password and email by default because it inherit from django abstract user
class User(AbstractUser):
    wish_list = models.ManyToManyField(Product, null=True)

    def __str__(self):
        return "name:{}".format(self.username)

    def add_to_wish_list(self, product):
        if not isinstance(product, Product):
            raise Exception
        self.wish_list.add(product)

    def remove_from_wish_list(self, product):
        if not isinstance(product, Product):
            raise Exception
        self.wish_list.remove(product)

