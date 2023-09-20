from django.db import models
from django.core.validators import ValidationError
import re
import uuid
import os
from django.utils.text import slugify
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.fields import ArrayField


def validate_positve(x):
    if x<0: raise ValidationError("Must Be Positive")



def is_hexadecimal(s):
    if not bool(re.match(r'^[0-9A-Fa-f]+$', s) and len(s)==6):
        raise ValidationError("choose a hexadecimal value")

class AboutProduct(models.Model):
    weight = models.DecimalField("Product Weight in grams", max_digits=10,decimal_places=3, blank=True, null=True)

    color_name = models.CharField(max_length=30,default="default", blank=True)
    code = models.CharField(max_length=6, validators=[is_hexadecimal], blank=True, null=True)

    size_name = models.CharField(max_length=30, null=True, blank=True)

    dimension = ArrayField(
        models.DecimalField(max_digits=10, decimal_places=3),
        size=3,
        null=True,
        blank=True,
    )

    # def has_exists(self):
    #     fields = self._meta.get_fields()
    #     nulls = []
    #     for field in fields:
    #         if field is None:
    #

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=4000, blank=True, null=True)

    slug = models.SlugField(unique=True, blank=True)



    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Use slugify from django.utils.text
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name
class Product(models.Model):
    TYPES = [
        ("Fo", "Food"),
        ("To", "Toys"),
        ("Tr", "Treats"),
        ("MC", "Monthly Crates"),
    ]
    type_code = models.CharField(max_length=2, choices=TYPES)
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    price = models.DecimalField("Product Price", max_digits=10, decimal_places=2, validators=[validate_positve])
    ship_price = models.DecimalField("Shipping Cost", max_digits=10, decimal_places=2, validators=[validate_positve], default=0)
    quantity = models.PositiveIntegerField("Quantity Available")


    # search_vector = SearchVectorField(null=True, editable=False)

    brand = models.ForeignKey(Brand, null=True, related_name="brand_products", verbose_name="Product's brand", on_delete=models.CASCADE)
    about_product = models.OneToOneField(AboutProduct,on_delete=models.SET_NULL, null=True, blank=True)
    product_ingredients = models.ManyToManyField("authe.PossibleAllergies",blank=True)

    slug = models.SlugField(unique=True, blank=True)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)


    def class_shipping_free(self):
        return " freeship" if self.ship_price==0 else "";
    def price_whole(self):
        return int(self.price//1)
    def price_decimal(self):
        return str (int(  100*( self.price-(self.price//1) )  ) ).zfill(2)
    def shipping_cost(self):
        return (f"${self.ship_price}" if self.ship_price!=0 else "Free")+" Shipping"
    def in_stock(self):
        if self.quantity>0:
            return "In Stock"
        else:
            return "Out of Stock"
    def in_stock_class(self):
        if self.quantity>0:
            return "stock"
        else:
            return "notstock"
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if not self.slug:
            try:
                self.slug = slugify(self.title)  # Use slugify from django.utils.text
            except:
                raise ValidationError("slug is already taken")
        super().save(*args, **kwargs)

class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="images for product",related_name="images")
    image = models.ImageField(upload_to='product/images/')
    def __str__(self):
        return f"{self.product.title}'s image:  {os.path.basename(self.image.name)}"
