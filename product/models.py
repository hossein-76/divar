from django.db import models
from django_mysql.models import JSONField


# mappers

# city vicinity mapper
class CVMapper(models.Model):
    city = models.ForeignKey("City", on_delete=models.CASCADE)
    vicinities = models.ManyToManyField("Vicinity")

    def add_vicinity(self, vic):
        if not isinstance(vic, Vicinity):
            raise Exception
        self.vicinities.add(vic)
        self.save()

    def get_vicinities(self):
        return self.vicinities

    def delete_vicinity(self, vic):
        if not isinstance(vic, Vicinity) or not vic in self.vicinities:
            raise Exception
        self.vicinities.remove(vic)


# category product mapper
class CPMapper(models.Model):
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    products = models.ManyToManyField("Product")

    def add_product(self, product):
        if not isinstance(product, Product):
            raise Exception
        self.products.add(product)
        self.save()

    def get_products(self):
        return self.products

    def delete_product(self, product):
        if not isinstance(product, Product) or not product in self.products:
            raise Exception

        self.products.remove(product)
        self.save()


# Vicinity Product mapper
class VPMapper(models.Model):
    vicinity = models.ForeignKey("Vicinity", unique=True, on_delete=models.CASCADE)
    products = models.ManyToManyField("Product")

    # void
    def add_product(self, product):
        if not isinstance(product, Product):
            raise Exception
        self.products.add(product)
        self.save()

    # list
    def get_products(self):
        return self.products

    # void
    def delete_product(self, product):
        if not isinstance(product, Product) or not product in self.products:
            raise Exception

        self.products.remove(product)
        self.save()


# models
class City(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(City, self).save(*args, **kwargs)
        CVMapper.objects.get_object_or_create(city=self)

    def get_vicinities(self):
        cmap = CVMapper.objects.get(city=self)
        return cmap.get_vicinities()

    def get_products(self):
        vics = self.get_vicinities()
        p = Product.objects.none()
        for v in vics:
            p = (p | v.get_products()).distinct()
        return p


class Vicinity(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(Vicinity, self).save(*args, **kwargs)
        VPMapper.objects.get_or_create(vicinity=self)
        cv = CVMapper.objects.get_object_or_create(city=self.city)
        cv.add_vicinity(vic=self)

    def get_products(self):
        cmap = VPMapper.objects.get(vicinity=self)
        return cmap.get_products()

    def add_product(self, product):
        cmap = VPMapper.objects.get(vicinity=self)
        if not isinstance(product, Product):
            raise Exception
        cmap.add_product(product)
        cmap.save()

    def delete(self, *args, **kwargs):
        cmap = VPMapper.objects.get(vicinity=self)
        cmap.delete()
        super(Vicinity, self).delete(*args, **kwargs)

    def delete_product(self, product):
        if not isinstance(product, Product):
            raise Exception
        cmap = VPMapper.objects.get(vicinity=self)
        cmap.delete_product(product)

    def get_city(self):
        return self.city


class ProductImage(models.Model):
    image = models.ImageField(upload_to="product")
    alt = models.CharField(max_length=30)


class AttributeChoiceValue(models.Model):
    value = models.CharField(max_length=255)


class Attribute(models.Model):
    name = models.CharField(max_length=100)


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', related_name="childs", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        CPMapper.objects.get_or_create(category=self)

    def get_product(self):
        cmap = CPMapper.objects.get(category=self)
        return cmap.get_products()

    def add_product(self, product):
        cp = CPMapper.objects.get_or_create(category=self)
        if not isinstance(product, Product):
            raise Exception
        cp.add_product(product)
        cp.save()

    def delete(self, *args, **kwargs):
        cmap = CPMapper.objects.get(category=self)
        cmap.delete()
        super(Category, self).delete(*args, **kwargs)

    def delete_product(self, product):
        if not isinstance(product, Product):
            raise Exception
        cmap = CPMapper.objects.get(category=self)
        cmap.delete_product(product)

    def get_parent(self):
        return self.parent


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField()
    image = models.ManyToManyField(ProductImage)
    vicinity = models.ForeignKey(Vicinity, on_delete=models.CASCADE)
    attributes = JSONField(default=dict)
    creation_time = models.DateTimeField(auto_now=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        self.vicinity.add_product(self)
        self.category.add_product(self)

    def delete(self, *args, **kwargs):
        self.category.delete_product(self)
        self.vicinity.delete_product(self)
        super(Product, self).delete(*args, **kwargs)
