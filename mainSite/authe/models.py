from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from shop.models import Product
class PossibleAllergies(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class CustomerDog(models.Model):
    name = models.CharField("Dogs Name", max_length=20)
    breed = models.CharField("Dogs Breed", max_length=20)
    allergy = models.ManyToManyField(PossibleAllergies)
    age = models.PositiveSmallIntegerField("Dogs Age")
    male = models.BooleanField(default=True)

class CustomerUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')



        return self.create_user(email, first_name, last_name, password, **extra_fields)


class CustomerCart(models.Model):
    # save_for_later = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey("shop.Product", related_name="in_carts", verbose_name="Users Cart", on_delete=models.CASCADE)
class CustomerUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomerUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    user_cart = models.ManyToManyField(CustomerCart, related_name="all_carts_inside",verbose_name="Users Cart",blank=True)
    dog = models.OneToOneField(CustomerDog, on_delete=models.CASCADE, null=True, blank=True, related_name="dogs_user")


    def __str__(self):
        return self.email

    def getfirstandlast(self):
        return f"{self.first_name} {self.last_name}"
    def getfullname(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"


# allergy_choices = [
#         "Beef",
#         "Chicken",
#         "Dairy(milk, cheese)",
#         "Eggs",
#         "Wheat",
#         "Soy",
#         "Corn",
#         "Fish",
#         "Lamb",
#         "Pork",
#         "Turkey",
#         "Rabbit",
#         "Venison",
#         "Duck",
#         "Potato",
#         "Sweet potatoes",
#         "Rice",
#         "Barley",
#         "Oats",
#         "Rye",
#         "Peanuts",
#         "Tree nuts(almonds, walnuts)",
#         "Sunflower seeds",
#         "Flaxseeds",
#         "Sesame seeds",
#         "Coconut",
#         "Lentils",
#         "Chickpeas",
#         "Kidney beans",
#         "Green peas",
#         "Tomatoes",
#         "Carrots",
#         "Spinach",
#         "Broccoli",
#         "Cauliflower",
#         "Bell peppers",
#         "Apples",
#         "Bananas",
#         "Blueberries",
#         "Strawberries",
#         "Pineapple",
#         "Watermelon",
#         "Grapes",
#         "Raisins",
#         "Oranges",
#         "Lemons",
#         "Lime",
#         "Mango",
#         "Papaya",
#         "Kiwi",
#         "Cranberries",
#         "Cinnamon",
#         "Nutmeg",
#         "Garlic",
#         "Onions",
#         "Chives",
#         "Mushrooms",
#         "Avocado",
#         "Peaches",
#         "Plums",
#         "Cherries",
#         "Apricots",
#         "Prunes",
#         "Pomegranates",
#         "Pears",
#         "Melon",
#         "Quinoa",
#         "Millet",
#         "Spelt",
#         "Teff",
#         "Sorghum",
#         "Tapioca",
#         "Buckwheat",
#         "Alfalfa",
#         "Spirulina",
#         "Chia seeds",
#         "Crab",
#         "Lobster",
#         "Shrimp",
#         "Clams",
#         "Mussels",
#         "Scallops",
#         "Sardines",
#         "Anchovies",
#         "Herring",
#         "Trout",
#         "Salmon",
#         "Tuna",
#         "Cod",
#         "Pollock",
#         "Catfish",
#         "Bass",
#         "Perch",
#         "Tilapia",
#         "Mackerel",
#         "Flounder",
#         "Whitefish",
#         "Halibut",
#         "Sole",
#         "Mahi-mahi",
#     ]

# dog_breeds = [
#     "Labrador Retriever",
#     "German Shepherd",
#     "Golden Retriever",
#     "French Bulldog",
#     "Bulldog",
#     "Poodle",
#     "Beagle",
#     "Rottweiler",
#     "Yorkshire Terrier",
#     "Boxer",
#     "Dachshund",
#     "Siberian Husky",
#     "Shih Tzu",
#     "Great Dane",
#     "Chihuahua",
#     "Pug",
#     "Doberman Pinscher",
#     "Shetland Sheepdog",
#     "Cocker Spaniel",
#     "Australian Shepherd",
#     "Pomeranian",
#     "Border Collie",
#     "Pembroke Welsh Corgi",
#     "Miniature Schnauzer",
#     "Chow Chow",
#     "Bichon Frise",
#     "Basset Hound",
#     "Bernese Mountain Dog",
#     "Cavalier King Charles Spaniel",
#     "West Highland White Terrier",
#     "Bull Terrier",
#     "Shiba Inu",
#     "Weimaraner",
#     "Staffordshire Bull Terrier",
#     "Akita",
#     "Rhodesian Ridgeback",
#     "Newfoundland",
#     "Papillon",
#     "Dalmatian",
#     "Italian Greyhound",
#     "Havanese",
#     "Miniature Pinscher",
#     "Chinese Shar-Pei",
#     "Afghan Hound",
#     "Irish Wolfhound",
#     "Irish Setter",
#     "Basenji",
#     "American Eskimo Dog",
#     "English Springer Spaniel",
#     "Borzoi",
#     "Lhasa Apso",
#     "Collie",
#     "Norwegian Elkhound",
#     "Samoyed",
#     "American Staffordshire Terrier",
#     "Giant Schnauzer",
#     "Bloodhound",
#     "Whippet",
#     "Airedale Terrier",
#     "Saint Bernard",
#     "English Bulldog",
#     "American Bulldog",
#     "Pointer",
#     "Maltese",
#     "Scottish Terrier",
#     "Australian Cattle Dog",
#     "Keeshond",
#     "Great Pyrenees",
#     "Greyhound",
#     "German Shorthaired Pointer",
#     "Mastiff",
#     "Soft Coated Wheaten Terrier",
#     "Alaskan Malamute",
#     "Vizsla",
#     "Chinese Crested",
#     "Bullmastiff",
#     "Löwchen",
#     "Tibetan Terrier",
#     "Ibizan Hound",
#     "Briard",
#     "Standard Schnauzer",
#     "Komondor",
#     "English Setter",
#     "Portuguese Water Dog",
#     "American Eskimo",
#     "Irish Terrier",
#     "Black Russian Terrier",
#     "Border Terrier",
#     "Bearded Collie",
#     "American Water Spaniel",
#     "Canaan Dog",
#     "Harrier",
#     "Belgian Malinois",
#     "Bolognese",
#     "Bouvier des Flandres",
#     "Bedlington Terrier",
#     "Belgian Sheepdog",
#     "Belgian Tervuren",
#     "Boston Terrier",
#     "Norwegian Buhund",
#     "Nova Scotia Duck Tolling Retriever",
#     "Clumber Spaniel",
#     "Irish Water Spaniel",
#     "Dandie Dinmont Terrier",
#     "Finnish Lapphund",
#     "Cesky Terrier",
#     "Irish Red and White Setter",
#     "Finnish Spitz",
#     "Flat-Coated Retriever",
#     "Dutch Shepherd",
#     "Entlebucher Mountain Dog",
#     "Field Spaniel",
#     "Drever",
#     "Curly-Coated Retriever",
#     "Coton de Tulear",
#     "Cirneco dell'Etna",
#     "Czechoslovakian Vlcak",
#     "German Wirehaired Pointer",
#     "Dogo Argentino",
#     "Cane Corso",
#     "Caucasian Shepherd Dog",
#     "Central Asian Shepherd Dog",
#     "Pyrenean Shepherd",
#     "Bull Terrier (Miniature)",
#     "American Bully",
#     "Australian Terrier",
#     "Bedouin Shepherd Dog",
#     "Blue Lacy",
#     "Bouvier des Ardennes",
#     "Bracco Italiano",
#     "Bucovina Shepherd Dog",
#     "Croatian Sheepdog",
#     "King Charles Spaniel",
#     "Chinook",
#     "Clumber Spaniel",
#     "Combai",
#     "Coton de Tulear",
#     "Czechoslovakian Vlcak",
#     "Drentse Patrijshond",
#     "English Foxhound",
#     "Eurasier",
#     "Finnish Lapphund",
#     "Finnish Spitz",
#     "Grand Basset Griffon Vendeen",
#     "Himalayan Sheepdog",
#     "Indian Pariah Dog",
#     "Jagdterrier",
#     "Kangal Dog",
#     "Karakachan Dog",
#     "Kintamani",
#     "Korean Jindo Dog",
#     "Kuchi",
#     "Lagotto Romagnolo",
#     "Lapponian Herder",
#     "Miniature American Shepherd",
#     "Miniature Australian Shepherd",
#     "Mudi",
#     "Neapolitan Mastiff",
#     "Nederlandse Kooikerhondje",
#     "Norfolk Spaniel",
#     "Norwegian Buhund",
#     "Patterdale Terrier",
#     "Peruvian Hairless Dog",
#     "Puli",
#     "Pumi",
#     "Rajapalayam",
#     "Romanian Mioritic Shepherd Dog",
#     "Rottweiler",
#     "Saarloos Wolfdog",
#     "Saluki",
#     "Sarabi Mastiff",
#     "Slovak Cuvac",
#     "Stabyhoun",
#     "Tornjak",
#     "Toy Bulldog",
#     "Toy Manchester Terrier",
#     "Treeing Tennessee Brindle",
#     "Utonagan",
#     "Volpino Italiano",
#     "Wetterhoun",
#     "White Shepherd",
#     "Yorkshire Terrier",
# ]