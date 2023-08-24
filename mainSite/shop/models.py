from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import ValidationError
import re
# class Author(models.Model):
#     store_name = models.CharField(max_length=22)


def validate_positve(x):
    if x<0: raise ValidationError("Must Be Positive")



def is_hexadecimal(s):
    if not bool(re.match(r'^[0-9A-Fa-f]+$', s) and len(s)==6):
        raise ValidationError("choose a hexadecimal value")
class Colors(models.Model):
    color_name = models.CharField(max_length=30)
    code = models.CharField(max_length=6, validators=[is_hexadecimal])

class productIngrediants(models.Model):
    pass
    # names = ArrayField(
    #     models.CharField(max_length=100, choices=[(name, name) for name in PossibleAllergies.objects.values_list('name', flat=True)]),
    #     blank=True,
    #     null=True
    # )

class Sizes(models.Model):
    size_name = models.CharField(max_length=30)
    Dimensionx = models.DecimalField(max_digits=10,decimal_places=3)
    Dimensiony = models.DecimalField(max_digits=10,decimal_places=3)
    Dimensionz = models.DecimalField(max_digits=10,decimal_places=3)

class AboutProduct(models.Model):
    Weight = models.DecimalField("Product Weight", max_digits=10,decimal_places=3)
    colors = models.ManyToManyField(Colors)
    # manysizes = models.BooleanField(default=False)
    # if manysizes
    sizes = models.ManyToManyField(Sizes)
class Product(models.Model):
    TYPES = [
        ("To", "Toys"),
        ("Tr", "Treats"),
        ("MC", "Monthly Crates"),
    ]
    type_code = models.CharField(max_length=2, choices=TYPES)
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=400)
    price = models.DecimalField("Product Price", max_digits=10, decimal_places=2, validators=[validate_positve])
    ship_price = models.DecimalField("Shipping Cost", max_digits=10, decimal_places=2, validators=[validate_positve], default=0)
    quantity = models.PositiveIntegerField("Quantity Available")
    images = models.ImageField(upload_to='images/')

    about_product = models.OneToOneField(AboutProduct, on_delete=models.CASCADE)
    ingrediants = models.OneToOneField(productIngrediants, on_delete=models.CASCADE)
    def in_stock(self):
        return self.quantity!=0
    def __str__(self):
        return self.title


