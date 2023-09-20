from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Product, Brand
from authe.models import CustomerCart
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.aggregates import ArrayAgg
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from .forms import add_to_cart
from django.http import JsonResponse, HttpResponseBadRequest
import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import model_to_dict
from misc.views import MessageLoginRequiredMixin
from django.http import HttpResponseNotFound
# Create your views here.
def truncate_sentence(sentence, max_length=22):
    # Check if the sentence length is within the maximum length
    if len(sentence) <= max_length:
        return sentence

    # Find the last space within the maximum length
    last_space_index = sentence.rfind(' ', 0, max_length)

    # If no space is found, truncate at max_length and add "..."
    if last_space_index == -1:
        return sentence[:max_length] + '...'

    # Truncate at the last space and add "..."
    return sentence[:last_space_index] + '...'
def join_strings_with_commas(strings):
    if len(strings) == 0:
        return ""
    elif len(strings) == 1:
        return strings[0]
    else:
        return f"{', '.join(strings[:-1])} and {strings[-1]}"
def show_allergic(user, products):
    products_allergy_info = []
    for _ in range(len(products)):
        products_allergy_info.append([[], [], []])
    if user.is_authenticated:
        if user.dogs.exists():
            for i, product in enumerate(products):
                if product.product_ingredients.exists():
                    for dog in user.dogs.all():
                        dog_allergies = dog.allergys.all()
                        for ingredient in product.product_ingredients.all():
                            if ingredient in dog_allergies:
                                products_allergy_info[i][0].append(dog.name)
                                break
            for i in range(len(products_allergy_info)):
                if products_allergy_info[i][0]:
                    if len(products_allergy_info[i][
                               0])>1:  # more than one dog to add proper prunuctation like dogs and are instead of dog and is
                        products_allergy_info[i][1] = "s"
                        products_allergy_info[i][2] = "are"
                    else:
                        products_allergy_info[i][1] = ""
                        products_allergy_info[i][2] = "is"
                    products_allergy_info[i][0] = join_strings_with_commas(products_allergy_info[i][0])
    return zip(products, products_allergy_info)
def one_show_allergic(user, product):
    product_allergy_info = [[],[],[]]
    if user.is_authenticated:
        if user.dogs.exists():
            if product.product_ingredients.exists():
                for dog in user.dogs.all():
                    dog_allergies = dog.allergys.all()
                    for ingredient in product.product_ingredients.all():
                        if ingredient in dog_allergies:
                            product_allergy_info[0].append(dog.name)
                            break
            if product_allergy_info[0]:
                if len(product_allergy_info[0])>1:  # more than one dog to add proper prunuctation like dogs and are instead of dog and is
                    product_allergy_info[1] = "s"
                    product_allergy_info[2] = "are"
                else:
                    product_allergy_info[1] = ""
                    product_allergy_info[2] = "is"
                product_allergy_info[0] = join_strings_with_commas(product_allergy_info[0])
    return product_allergy_info
def detailed_show_allergic(user, product):
    if product.product_ingredients.exists() and user.is_authenticated:
        ingredients = [model_to_dict(ingredient) for ingredient in  product.product_ingredients.all()]

        all_allergies_dog_name = []
        user_dogs = user.dogs.all()
        for i in range(len(ingredients)):
            ingredients[i]['dog_name'] = []
        for dog in user_dogs:
            dog_allergies = dog.allergys.values_list("pk", flat=True)
            for i, ingredient in enumerate(ingredients):
                if ingredient["id"] in dog_allergies:
                    ingredients[i]['dog_name'].append(dog.name)
                    if not dog.name in all_allergies_dog_name: all_allergies_dog_name.append(dog.name)
        for i in range(len(ingredients)):
            # ingredients[i]["more_than_one_dog_s"] = "s" if len(ingredients[i]["dog_name"])>1 else ""
            # ingredients[i]["more_than_one_dog_verb"] = "are" if len(ingredients[i]["dog_name"])>1 else "is"
            ingredients[i]['dog_name'] = join_strings_with_commas(ingredients[i]['dog_name'])
        ingredients = sorted(ingredients, key = lambda x: x["dog_name"], reverse=True)
        if all_allergies_dog_name:
            allergic_dogs = f"Allergic for {join_strings_with_commas(all_allergies_dog_name)}"
        else:
            allergic_dogs = ""
        return ingredients, allergic_dogs
    return product.product_ingredients.all(), None
class cartPage(MessageLoginRequiredMixin, TemplateView):
    message = "Can't view cart since your not Logged In"
    template_name = "shop/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.user.user_cart
        cart_quantity = cart.values_list("quantity", flat=True)
        product_ids = cart.values_list("product", flat=True)
        products = Product.objects.filter(id__in=product_ids)
        products_allergies = show_allergic(self.request.user, products)
        context['cart'] = [(product, allergies, quantity) for (product,allergies), quantity in zip(products_allergies, cart_quantity)]
        print(list(context["cart"]))
        return context
@login_required
def cart_delete(request):
    if request.method=="POST":
        id = request.POST.get('cart_item_id')
        print(id)
        product = get_object_or_404(Product, pk=id)
        print(product)
        if product:
            cart = request.user.user_cart.filter(product=product)
            print(request.user.user_cart.first())
            print(cart)
            if not cart.exists():
                raise HttpResponseBadRequest()
            cart = cart.first()
            cart.delete()
            messages.success(request, f"Deleted {truncate_sentence(product.title)} from Cart")
            return redirect(reverse("cart"))
        else:
            raise HttpResponseBadRequest()
    else:
        raise HttpResponseBadRequest()
class shopPage(TemplateView):
    template_name = 'shop/shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        productcount = Product.objects.all().count()
        products = Product.objects.all()[:50]
        context["products"] = show_allergic(self.request.user, products)
        return context

def product_detail(request, slug):
    # is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    # if is_ajax:
    if request.method == "POST":
        form = add_to_cart(request.POST)
        if request.user.is_authenticated and form.is_valid():
            quantity = int(form.cleaned_data['quantity'])
            product = get_object_or_404(Product, slug=slug)

            if request.user.user_cart.filter(product__slug=slug): #if already in cart add one to quantity
                existing_product = request.user.user_cart.filter(product__pk=product.pk).first()
                if not (existing_product.quantity > product.quantity):
                    existing_product.quantity += quantity
                    existing_product.save()
                else:
                    return render(request, 'shop/cart_product_error.html')
            else:
                new_cart = CustomerCart(quantity=quantity, product=product)
                new_cart.save()
                request.user.user_cart.add(new_cart)
            return redirect(reverse('added_to_cart', kwargs={'slug': product.slug}))
        else:
            # messages.success(request, )
            return redirect(reverse('login'))
    # else:
    #     return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        form = add_to_cart()
        product = get_object_or_404(Product, slug=slug)
        # images_url = [image for product.images.all().image.url]
        context = {'form': form, 'product':product}
        context['ingredients'], context['allergic_dogs'] = detailed_show_allergic(request.user, product)
        return render(request, 'shop/product_detail.html', context)

def brand_detail(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    products = brand.brand_products.all()
    context = {'brand': brand}
    context["products"] = show_allergic(request.user, products)

    # images_url = [image for product.images.all().image.url]
    return render(request, 'shop/brand_detail.html', context)


def search_view(request):
    products = Product.objects
    raw_query = request.GET.get('q','')
    did_something=[]
    if not raw_query:
        return redirect(reverse("shop"))
    query = SearchQuery(raw_query, search_type='phrase')
    if query:
        products = products.annotate(
            all_product_ingredients=ArrayAgg(
                "product_ingredients__name",
                distinct=True,
            ),
        )
        # SearchVector("product_ingredients__name", weight="D") +\
        vector =SearchVector("title", weight="A") +\
                SearchVector("description", weight="D")+\
                SearchVector("brand__name", weight="B")+\
                SearchVector("type_code", weight="B")+\
                SearchVector("all_product_ingredients", weight="C")
        did_something.append(True)
        rank = SearchRank(vector, query, weights=[0.04,0.2,0.4,1.0])
        products = products.annotate(
            rank=rank
        ).filter(rank__gte=0.2).order_by("-rank")
    raw_filter = request.GET.get('f','')
    if raw_filter:
        filters = raw_filter.split(",")
        default_slider_values = filters
        defaults = [0,-1]
        for i in range(2):
            filters[i]=int(filters[i])
        for i, (default, value) in enumerate(zip(defaults, filters)):
            if default!=value:
                did_something.append(True)
                if i==0: #price min
                    products = products.filter(price__gte=value)
                if i==1: #price max
                    products = products.filter(price__lte=value)
    else:
        default_slider_values = [0,20]
    if not any(did_something):
        products= products.all()

    context = {'query': raw_query,'default_slider_values':default_slider_values}

    context['product_exists'] = not not products
    context['product_count'] = products.count()
    context["products"] = show_allergic(request.user, products)
    return render(request, 'shop/search_results.html', context)

@login_required
def addtocart(request, slug):
    cart = get_object_or_404(CustomerCart, product__slug=slug)


    context = {'quantity':cart.quantity, "product":cart.product,}
    context["allergic_info"] = one_show_allergic(request.user, cart.product)
    return render(request, 'shop/cart_add.html', context)
