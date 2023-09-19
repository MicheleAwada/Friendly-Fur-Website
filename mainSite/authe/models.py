from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.urls import reverse
from datetime import datetime, timedelta
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


def simple_dog_join(old,name):
    if old:
        return old+", "+name
    return name
class PossibleAllergies(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, null=True, blank=True)
    # def add_dog_name(self, name):
    #     if self.dog_name:
    #         self.dog_name+=", "+name
    #     else:
    #         self.dog_name=name


    def __str__(self):
        return self.name
    class Meta:
        ordering = ["name"]
class PossibleBreeds(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, null=True, blank=True)


    def __str__(self):
        return self.name
    class Meta:
        ordering = ["name"]



class CustomerUserManager(BaseUserManager):
    def create_user(self, email, first_name, middle_name,last_name, password=None, **extra_fields):
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
    product = models.OneToOneField("shop.Product", related_name="in_carts", verbose_name="Users Cart", on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Cart"
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

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
    def __str__(self):
        return self.email
    def getfirstandlast(self):
        return f"{self.first_name} {self.last_name}"
    def getfullname(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"


class CustomerDog(models.Model):
    name = models.CharField("Dogs Name", max_length=20)
    breed = models.ManyToManyField(PossibleBreeds,verbose_name="Dogs Breed", blank=True)
    allergys = models.ManyToManyField(PossibleAllergies, blank=True)
    age = models.PositiveSmallIntegerField("Age", null=True, blank=True)
    is_male = models.BooleanField(default=True)
    dog_number = models.PositiveIntegerField(editable=True)

    human = models.ForeignKey(CustomerUser, verbose_name="dog's human", related_name="dogs", on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        if not self.dog_number: self.dog_number = self.human.dogs.count()+1
        super(CustomerDog, self).save(*args, **kwargs)
    def __str__(self):
        return self.name


class limit_ajax_email_validators(models.Model):
    ip = models.CharField(max_length=15, unique=True)
    banned = models.DateTimeField(null=True,blank=True)
    request_amount = models.PositiveSmallIntegerField(default=0,null=True,blank=True)
    def add_request(self):
        self.request_amount+=1
        if self.request_amount>300:
            banned = datetime.now() +timedelta(days=3)
    def is_banned(self):
        if self.banned:
            if self.banned<datetime.now():
                self.banned=None
                return False
            return True
        return False

class UnverifiedUser(AbstractBaseUser):
    email = models.EmailField()
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    verf_user = models.ForeignKey(CustomerUser, verbose_name="Verified_Users_Email_Change",null=True, blank=True, related_name="Unverified_Email_Change", on_delete=models.CASCADE)

    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = ['first_name','last_name','email']


    verification_token = models.CharField(max_length=100, null=True, blank=True)
    user_expiry = models.DateTimeField(null=True, blank=True)
    def get_url(self):
        return reverse("verify", kwargs={"uid64":urlsafe_base64_encode(force_bytes(self.id)),"token":self.token()})
    def token(self):
        self.verification_token = default_token_generator.make_token(self)
        self.user_expiry = datetime.now() + timedelta(hours=3)
        return self.verification_token
    def remove_if_expired(self, timenow):
        if self.is_expired(timenow=timenow):
            self.delete()
            return True
        return False

    def is_expired(self, timenow):
        return timenow > self.user_expiry
    def __str__(self):
        return f"{self.email} id:{self.pk}"
    class Meta:
        verbose_name = "Unverified User"
        verbose_name_plural = "Unverified Users"














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
food_color_mapping = {
    "Beef": "#804000",  # Dark brown
    "Chicken": "#FFFFFF",  # White
    "Dairy(milk, cheese)": "#F2D7D5",  # Cream
    "Eggs": "#FFF28A",  # Light yellow
    "Wheat": "#FFDB58",  # Mustard
    "Soy": "#32CD32",  # Lime green
    "Corn": "#FFD700",  # Gold
    "Fish": "#FF4500",  # Orange red
    "Lamb": "#CD5C5C",  # Indian red
    "Pork": "#FFC0CB",  # Pink
    "Turkey": "#8B4513",  # Saddle brown
    "Rabbit": "#DAA520",  # Goldenrod
    "Venison": "#A0522D",  # Sienna
    "Duck": "#4682B4",  # Steel blue
    "Potato": "#D2691E",  # Chocolate
    "Sweet potatoes": "#D2691E",  # Chocolate
    "Rice": "#FFFF00",  # Yellow
    "Barley": "#E6E6FA",  # Lavender
    "Oats": "#FFD700",  # Gold
    "Rye": "#D2691E",  # Chocolate
    "Peanuts": "#FFA500",  # Orange
    "Tree nuts(almonds, walnuts)": "#8B4513",  # Saddle brown
    "Sunflower seeds": "#FFD700",  # Gold
    "Flaxseeds": "#2E8B57",  # Sea green
    "Sesame seeds": "#A0522D",  # Sienna
    "Coconut": "#F5DEB3",  # Wheat
    "Lentils": "#800080",  # Purple
    "Chickpeas": "#CD853F",  # Peru
    "Kidney beans": "#B22222",  # Firebrick
    "Green peas": "#228B22",  # Forest green
    "Tomatoes": "#FF6347",  # Tomato
    "Carrots": "#FFA500",  # Orange
    "Spinach": "#4B0082",  # Indigo
    "Broccoli": "#008000",  # Green
    "Cauliflower": "#F5F5F5",  # White smoke
    "Bell peppers": "#FF4500",  # Orange red
    "Apples": "#FF4500",  # Orange red
    "Bananas": "#FFFF00",  # Yellow
    "Blueberries": "#4169E1",  # Royal blue
    "Strawberries": "#FF0000",  # Red
    "Pineapple": "#FFD700",  # Gold
    "Watermelon": "#FF69B4",  # Hot pink
    "Grapes": "#800080",  # Purple
    "Raisins": "#800080",  # Purple
    "Oranges": "#FFA500",  # Orange
    "Lemons": "#FFFF00",  # Yellow
    "Lime": "#00FF00",  # Lime
    "Mango": "#FF8C00",  # Dark orange
    "Papaya": "#FFD700",  # Gold
    "Kiwi": "#228B22",  # Forest green
    "Cranberries": "#DC143C",  # Crimson
    "Cinnamon": "#D2691E",  # Chocolate
    "Nutmeg": "#8B4513",  # Saddle brown
    "Garlic": "#FFD700",  # Gold
    "Onions": "#FF4500",  # Orange red
    "Chives": "#FF4500",  # Orange red
    "Mushrooms": "#8B4513",  # Saddle brown
    "Avocado": "#006400",  # Dark green
    "Peaches": "#FFD700",  # Gold
    "Plums": "#DDA0DD",  # Plum
    "Cherries": "#FF0000",  # Red
    "Apricots": "#FFD700",  # Gold
    "Prunes": "#800080",  # Purple
    "Pomegranates": "#8B0000",  # Dark red
    "Pears": "#FFD700",  # Gold
    "Melon": "#FFA500",  # Orange
    "Quinoa": "#E6E6FA",  # Lavender
    "Millet": "#D2B48C",  # Tan
    "Spelt": "#D2691E",  # Chocolate
    "Teff": "#CD853F",  # Peru
    "Sorghum": "#8B4513",  # Saddle brown
    "Tapioca": "#FFD700",  # Gold
    "Buckwheat": "#800080",  # Purple
    "Alfalfa": "#00FF00",  # Lime
    "Spirulina": "#00A86B",
    "Chia seeds": "#9F8B5B",
    "Crab": "#E87E33",
    "Lobster": "#FF6347",
    "Shrimp": "#FFA07A",
    "Clams": "#EEDD82",
    "Mussels": "#CEB899",
    "Scallops": "#FFD700",
    "Sardines": "#1E50A2",
    "Anchovies": "#1E50A2",
    "Herring": "#1E50A2",
    "Trout": "#A67B5B",
    "Salmon": "#FF8C69",
    "Tuna": "#3B5998",
    "Cod": "#185AA9",
    "Pollock": "#75AADB",
    "Catfish": "#4B0082",
    "Bass": "#0B86DA",
    "Perch": "#EBC33D",
    "Tilapia": "#70A288",
    "Mackerel": "#526F35",
    "Flounder": "#FAE7B5",
    "Whitefish": "#F5F5F5",
    "Halibut": "#2A2A2A",
    "Sole": "#FFE4B5",
    "Mahi-mahi": "#FFDB58",
}

food_color_tuples = [(food, food_color_mapping.get(food, "#FFFFFF")) for food in food_color_mapping]
dog_colors_hex = {
    "Labrador Retriever": "#FDD017",  # Yellow
    "German Shepherd": "#BDB76B",  # Tan and black
    "Golden Retriever": "#FFD700",  # Golden
    "French Bulldog": "#E5AA70",  # Fawn
    "Bulldog": "#8B4513",  # Brown
    "Poodle": "#FF00FF",  # Pink (for variety in coat colors)
    "Beagle": "#8B4513",  # Brown (for variety in coat colors)
    "Rottweiler": "#8B0000",  # Black and tan
    "Yorkshire Terrier": "#BDB76B",  # Tan and black
    "Boxer": "#D2691E",  # Fawn
    "Dachshund": "#A0522D",  # Red or brown
    "Siberian Husky": "#87CEEB",  # Gray and white
    "Shih Tzu": "#B8860B",  # Various colors
    "Great Dane": "#696969",  # Various colors
    "Chihuahua": "#8B4513",  # Brown
    "Pug": "#A9A9A9",  # Silver or apricot-fawn
    "Doberman Pinscher": "#8B4513",  # Brown (for variety in coat colors)
    "Shetland Sheepdog": "#B0C4DE",  # Blue merle and tan
    "Cocker Spaniel": "#A0522D",  # Various colors
    "Australian Shepherd": "#4682B4",  # Blue merle and others
    "Pomeranian": "#FF4500",  # Orange or red
    "Border Collie": "#000000",  # Black and white
    "Pembroke Welsh Corgi": "#FFD700",  # Sable, red, and white
    "Miniature Schnauzer": "#A9A9A9",  # Salt and pepper
    "Chow Chow": "#8B4513",  # Red or cream
    "Bichon Frise": "#FFFFFF",  # White
    "Basset Hound": "#8B4513",  # Brown (for variety in coat colors)
    "Bernese Mountain Dog": "#4B0082",  # Black, white, and rust
    "Cavalier King Charles Spaniel": "#B22222",  # Various colors
    "West Highland White Terrier": "#FFFFFF",  # White
    "Bull Terrier": "#8B4513",  # White (for variety in coat colors)
    "Shiba Inu": "#FF4500",  # Red sesame
    "Weimaraner": "#778899",  # Silver-gray
    "Staffordshire Bull Terrier": "#8B4513",  # Brindle (for variety in coat colors)
    "Akita": "#B88169",
    "Rhodesian Ridgeback": "#8B4513",
    "Newfoundland": "#000000",
    "Papillon": "#FFFACD",
    "Dalmatian": "#FFFFFF",
    "Italian Greyhound": "#B0C4DE",
    "Havanese": "#8B4513",
    "Miniature Pinscher": "#8B0000",
    "Chinese Shar-Pei": "#CD853F",
    "Afghan Hound": "#D2B48C",
    "Irish Wolfhound": "#8B4513",
    "Irish Setter": "#8B0000",
    "Basenji": "#000000",
    "American Eskimo Dog": "#FFFFFF",
    "English Springer Spaniel": "#FFFACD",
    "Borzoi": "#8B4513",
    "Lhasa Apso": "#8B4513",
    "Collie": "#B8860B",
    "Norwegian Elkhound": "#696969",
    "Samoyed": "#FFFFFF",
    "American Staffordshire Terrier": "#FF4500",
    "Giant Schnauzer": "#000000",
    "Bloodhound": "#8B0000",
    "Whippet": "#FFFFFF",
    "Airedale Terrier": "#8B4513",
    "Saint Bernard": "#8B0000",
    "English Bulldog": "#8B4513",
    "American Bulldog": "#FFFFFF",
    "Pointer": "#8B4513",
    "Maltese": "#FFFACD",
    "Scottish Terrier": "#000000",
    "Australian Cattle Dog": "#000000",
    "Keeshond": "#8B4513",
}
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