from django.db import models
from django_mysql.models import JSONField


class AppManager(models.Model):
    cities = models.ManyToManyField("City", blank=True)
    categories = models.ManyToManyField("Category", blank=True)

    def search(self, city, vicinity=None, product=None, category=None):
        city = self.cities.get(name=city)
        vicinity = city.get_vicinitiy(vicinity)
        cat = self.categories.get(name=category)
        if not city:
            return None
        q = city.get_products()
        if vicinity:
            q = q & vicinity.get_products()
        if cat:
            q = q & cat.get_products()
        if product:
            q = q & Product.objects.filter(name__icontains=product)
        return q


# mappers

# city vicinity mapper
class CVMapper(models.Model):
    city = models.ForeignKey("City", on_delete=models.CASCADE)
    vicinities = models.ManyToManyField("Vicinity", blank=True)

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
    products = models.ManyToManyField("Product", blank=True)

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
    products = models.ManyToManyField("Product", blank=True)

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
        CVMapper.objects.get_or_create(city=self)
        a = AppManager.objects.all()[0]
        a.cities.add(self)
        a.save()

    def get_vicinities(self):
        cmap = CVMapper.objects.get(city=self)
        return cmap.get_vicinities()

    def get_vicinity(self, vicinity):
        cm = self.get_vicinities()
        for i in cm:
            if i.name == vicinity:
                return vicinity
        return None

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
        try:
            cv = CVMapper.objects.get(city=self.city)
        except:
            raise Exception
        cv.add_vicinity(vic=self)

    def get_products(self):
        cmap = VPMapper.objects.get(vicinity=self)
        return cmap.get_products()

    def get_product(self, product):
        cm = self.get_products()
        for i in cm:
            if i.name == product:
                return i
        return None

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
    alt = models.CharField(max_length=30, blank=True, null=True)


class AttributeChoiceValue(models.Model):
    value = models.CharField(max_length=255)


class Attribute(models.Model):
    name = models.CharField(max_length=100)
    type_attribute = models.CharField(max_length=100, choices=(("numeric", "numeric"), ("value", "value")),
                                      default="value")


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', related_name="childs", on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        CPMapper.objects.get_or_create(category=self)
        a = AppManager.objects.all()[0]
        a.categories.add(self)
        a.save()

    def get_products(self):
        cmap = CPMapper.objects.get(category=self)
        return cmap.get_products()

    def get_product(self, product):
        cmap = CPMapper.objects.get(category=self)
        for i in cmap:
            if i == product:
                return i
        return None

    def add_product(self, product):
        if not isinstance(product, Product):
            raise Exception
        cp = CPMapper.objects.get(category=self)
        cp.add_product(product)
        cp.save()
        parent = self.parent
        while parent:
            cp = CPMapper.objects.get(category=parent)
            cp.add_product(product)
            cp.save()
            parent = parent.get_parent()

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
    image = models.ManyToManyField(ProductImage, blank=True)
    vicinity = models.ForeignKey(Vicinity, on_delete=models.CASCADE)
    attributes = JSONField(default=dict, blank=True, null=True)
    creation_time = models.DateTimeField(auto_now=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        self.vicinity.add_product(self)
        self.category.add_product(self)

    def delete(self, *args, **kwargs):
        self.category.delete_product(self)
        self.vicinity.delete_product(self)
        super(Product, self).delete(*args, **kwargs)
