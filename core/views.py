from django.shortcuts import render


from product.models import Product

def frontpage(request):
    newest_product = Product.objects.all()[0:8]
    return render(request, 'frontpage.html',{'newest_product':newest_product})

def contact(request):
    return render(request, 'contact.html')
