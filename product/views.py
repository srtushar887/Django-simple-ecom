from django.shortcuts import render, get_object_or_404
from django.db.models import Q

import random




from .models import Category, Product


def search(request):
    query = request.GET.get('query')
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'product/search.html',{'products':products,'query':query})


def product(request, category_slug, product_slug):
    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    similar_product = list(product.category.products.exclude(id=product.id))

    if len(similar_product) >= 4:
        similar_product = random.sample(similar_product, 4)

    return render(request, 'product/product.html',{'product':product, 'similar_product':similar_product})

def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    return render(request, 'product/category.html', {'category': category})





