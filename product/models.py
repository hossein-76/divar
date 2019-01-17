from django.db import models
from django.contrib.postgres.fields import JSONField


class AppManager(models.Model):
    _cities = models.ManyToManyField("City", blank=True)
    _categories = models.ManyToManyField("Category", blank=True)

    def search(self, city, vicinities=None, product=None, category=None):
        city = self._cities.get(name=city)
        if not city:
            return None
        q = city.get_products()
        if vicinities:
            q = Product.objects.none()
            for v in vicinities:
                vicinity = city.get_vicinity(v)
                s = vicinity.get_products()
                q = q.union(s)
                if not vicinity:
                    return "invalid vicinity"

        cat = self._categories.get(name=category)
        if cat:
            s = cat.get_products()
            q = q.intersection(s)
        if product:
            s = Product.objects.none()
            for i in q:
                if i.name__icontain == product:
                    s = s.union(i).distinct()
            q = s
        return q

    def expand_cities(self, city):
        self._cities.add(city)
        self.save()

    def expand_categories(self, category):
        self._categories.add(category)
        self.save()

    def delete_city(self, city):
        self._cities.remove(city)
        self.save()

    def delete_category(self, category):
        self._categories.remove(category)
        self.save()

    def get_categories(self):
        return self._categories.all()

    def get_cities(self):
        return self._cities.all()


# mappers

# city vicinity mapper
class CVMapper(models.Model):
    city = models.ForeignKey("City", on_delete=models.CASCADE)
    _vicinities = models.ManyToManyField("Vicinity", blank=True)

    def add_vicinity(self, vic):
        if not isinstance(vic, Vicinity):
            raise Exception
        self._vicinities.add(vic)
        self.save()

    def get_vicinities(self):
        return self._vicinities.all()

    def delete_vicinity(self, vic):
        if not isinstance(vic, Vicinity) or not vic in self._vicinities:
            raise Exception
        self._vicinities.remove(vic)


# category product mapper
class CPMapper(models.Model):
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    _products = models.ManyToManyField("Product", blank=True)

    def add_product(self, product):
        if not isinstance(product, Product):
            raise Exception
        self._products.add(product)
        self.save()

    def get_products(self):
        return self._products.all()

    def delete_product(self, product):
        if not isinstance(product, Product) or not product in self._products:
            raise Exception

        self._products.remove(product)
        self.save()


# Vicinity Product mapper
class VPMapper(models.Model):
    vicinity = models.ForeignKey("Vicinity", unique=True, on_delete=models.CASCADE)
    _products = models.ManyToManyField("Product", blank=True)

    # void
    def add_product(self, product):
        if not isinstance(product, Product):
            raise Exception
        self._products.add(product)
        self.save()

    # list
    def get_products(self):
        return self._products.all()

    # void
    def delete_product(self, product):
        if not isinstance(product, Product) or not product in self._products:
            raise Exception

        self._products.remove(product)
        self.save()


# models
class City(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(City, self).save(*args, **kwargs)

        c, c2 = CVMapper.objects.get_or_create(city=self)
        a = AppManager.objects.all()[0]
        a.expand_cities(self)

    def get_vicinities(self):
        cmap = CVMapper.objects.get(city=self)
        return cmap.get_vicinities()

    def get_vicinity(self, vicinity):
        if isinstance(vicinity, Vicinity):
            cm = self.get_vicinities()
            for i in cm:
                if i == vicinity:
                    return vicinity

        cm = self.get_vicinities()
        for i in cm:
            if i.name == vicinity:
                return i
        return None

    def get_products(self):
        vics = self.get_vicinities()

        p = Product.objects.none()
        for v in vics:
            p = p.union(v.get_products()).distinct()
        return p


class Vicinity(models.Model):
    name = models.CharField(max_length=255)
    _city = models.ForeignKey(City, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(Vicinity, self).save(*args, **kwargs)
        VPMapper.objects.get_or_create(vicinity=self)
        try:
            cv = CVMapper.objects.get(city=self._city)
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
        return self._city


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
    _parent = models.ForeignKey('self', related_name="childs", on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        CPMapper.objects.get_or_create(category=self)
        a = AppManager.objects.all()[0]
        a.expand_categories(self)

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
        parent = self._parent
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
        return self._parent

    def set_parent(self, category):
        self._parent = category
        self.save()


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

    def suggestion(self):
        products = self.category.get_products()[10]
        return products

class Report(models.Model):
    user = models.ForeignKey("account.User", on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    reason = models.CharField(max_length=255, choices=(("inappropriate content", "inappropriate content"),
                                                       ("spam content", "spam content")))
    detail = models.TextField()
    status = models.CharField(max_length=255, choices=(("approved", "approved"),
                                                       ("rejected", "rejected"),
                                                       ("pending", "pending")))

    def __str__(self):
        return "product:{}---user:{}".format(self.product.name, self.user.username)
