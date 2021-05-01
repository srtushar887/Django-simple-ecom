from django.shortcuts import render, get_object_or_404,redirect
from django.db.models import Q
from django.contrib import messages
import random



from .forms import AddtoCartForm
from .models import Category, Product
from cart.cart import Cart


def search(request):
    query = request.GET.get('query')
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'product/search.html',{'products':products,'query':query})


def product(request, category_slug, product_slug):
    cart = Cart(request)

    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)

    if request.method == 'POST':
        form = AddtoCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart.add(product_id=product.id, quantity=quantity,update_quantity=False)

            messages.success(request,'The product was added to the cart')
            return redirect('product',category_slug=category_slug,product_slug=product_slug)
    else:
        form = AddtoCartForm(request.POST)
        similar_product = list(product.category.products.exclude(id=product.id))

        if len(similar_product) >= 4:
            similar_product = random.sample(similar_product, 4)

        return render(request, 'product/product.html',{'product':product, 'similar_product':similar_product,'form':form})

def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    return render(request, 'product/category.html', {'category': category})





