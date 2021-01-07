from django.shortcuts import get_object_or_404
from products.models import Product,Comment

def categories(request):
    cat_list = []
    all_cat = Product.objects.all()
    for cat in all_cat:
        name_list = cat.categories.split(',')
        for item in name_list:
            cat_list.append(item)
    cat_dict = {'categories': set(cat_list)}
    return cat_dict

def user_liked_products(request):
        products = Product.objects.filter(likes=request.user.id)
        return {'user_liked_products': products}


def recent_products(request):
    products = Product.objects.all().order_by('-created_at')[:5]
    return {'recent_products': products}


