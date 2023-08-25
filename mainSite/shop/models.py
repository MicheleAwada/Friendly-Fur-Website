from django.db import models
from django.core.validators import ValidationError
import re
import uuid
from django.utils.text import slugify
# class Author(models.Model):
#     store_name = models.CharField(max_length=22)


def validate_positve(x):
    if x<0: raise ValidationError("Must Be Positive")



def is_hexadecimal(s):
    if not bool(re.match(r'^[0-9A-Fa-f]+$', s) and len(s)==6):
        raise ValidationError("choose a hexadecimal value")

class AboutProduct(models.Model):
    Weight = models.DecimalField("Product Weight in grams", max_digits=10,decimal_places=3, blank=True, null=True   )

    color_name = models.CharField(max_length=30,default="default", blank=True)
    code = models.CharField(max_length=6, validators=[is_hexadecimal], blank=True, null=True)

    size_name = models.CharField(max_length=30, default="default", blank=True)
    dimension_x = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    dimension_y = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    dimension_z = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)

    def clean(self):
        if (
                (self.dimension_x is None and self.dimension_y is not None)
                or (self.dimension_x is None and self.dimension_z is not None)
                or (self.dimension_y is None and self.dimension_z is not None)
        ):
            raise ValidationError("Either all dimensions must be null or all must have values.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Product(models.Model):
    TYPES = [
        ("Fo", "Food"),
        ("To", "Toys"),
        ("Tr", "Treats"),
        ("MC", "Monthly Crates"),
    ]
    type_code = models.CharField(max_length=2, choices=TYPES)
    title = models.CharField(max_length=40, unique=True)
    description = models.CharField(max_length=1600)
    price = models.DecimalField("Product Price", max_digits=10, decimal_places=2, validators=[validate_positve])
    ship_price = models.DecimalField("Shipping Cost", max_digits=10, decimal_places=2, validators=[validate_positve], default=0)
    quantity = models.PositiveIntegerField("Quantity Available")

    about_product = models.OneToOneField(AboutProduct, on_delete=models.CASCADE)
    product_ingredients = models.ManyToManyField("authe.PossibleAllergies",blank=True)

    slug = models.SlugField(unique=True, blank=True)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def get_url(self):
        return "product/"+str(self.slug)+"/"
    def shipping_cost(self):
        return self.ship_price if self.ship_price!=0 else "Free"
    def in_stock(self):
        return self.quantity!=0
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Use slugify from django.utils.text
        super().save(*args, **kwargs)
class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="images for product",related_name="images")
    image = models.ImageField(upload_to='product/images/')

