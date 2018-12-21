from django.db import models


class City(models.Model):
    name = models.CharField(max_length=255)


class Vicinity(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)


class ProductImage(models.Model):
    image = models.ImageField(upload_to="product")
    alt = models.CharField(max_length=30)


class AttributeChoiceValue(models.Model):
    value = models.CharField(max_length=255)


class Attribute(models.Model):
    name = models.CharField(max_length=100)
    valid_values = models.ManyToManyField(AttributeChoiceValue)


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', related_name="childs", on_delete=models.CASCADE)
    products = models.ManyToManyField('Product')


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.FloatField()
    image = models.ManyToManyField(ProductImage)
    vicinity = models.ForeignKey(Vicinity, on_delete=models.CASCADE)
    attributes = models.ManyToManyField(Attribute)
    creation_time = models.DateTimeField(default=None, null=True, blank=True)


# mappers

# city vicinity mapper
class CVMapper(models.Model):
    city = models.ForeignKey("City", on_delete=models.CASCADE)
    vicinities = models.ManyToManyField("Vicinity")


# category product mapper
class CPMapper(models.Model):
    city = models.ForeignKey("City", on_delete=models.CASCADE)
    vicinities = models.ManyToManyField("Vicinity")


# Vicinity Product mapper
class VPMapper(models.Model):
    city = models.ForeignKey("City", on_delete=models.CASCADE)
    vicinities = models.ManyToManyField("Vicinity")
