from django.shortcuts import render,redirect


import stripe
from django.conf import settings
from django.contrib import messages

from .cart import Cart
from .forms import CheckoutForm
from order.utilities import checkout

def cart_detail(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            stripe.api_key = settings.STRIPE_SECRET_KEY

            stripe_token = form.cleaned_data['stripe_token']

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            zipcode = form.cleaned_data['zipcode']
            place = form.cleaned_data['place']

            order = checkout(request, first_name, last_name, email, address, zipcode, place, phone,
                             cart.get_total_cost())

            cart.clear()

            return redirect('success')


            # try:
            #     charge = stripe.Charge.create(
            #         amount=int(cart.get_total_cost() * 100),
            #         currency='USD',
            #         description='Charge from Interiorshop',
            #         source=stripe_token
            #     )
            #
            #     first_name = form.cleaned_data['first_name']
            #     last_name = form.cleaned_data['last_name']
            #     email = form.cleaned_data['email']
            #     phone = form.cleaned_data['phone']
            #     address = form.cleaned_data['address']
            #     zipcode = form.cleaned_data['zipcode']
            #     place = form.cleaned_data['place']
            #
            #     order = checkout(request, first_name, last_name, email, address, zipcode, place, phone,
            #                      cart.get_total_cost())
            #
            #     cart.clear()
            #
            #     return redirect('success')
            # except Exception:
            #     messages.error(request, 'There was something wrong with the payment')

    else:
        form = CheckoutForm()

    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quatity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)
        return redirect('cart_detail')

    if change_quatity:
        cart.add(change_quatity, quantity, True)
        return redirect('cart_detail')

    return render(request, 'cart/cart.html', {'form': form, 'stripe_pub_key': settings.STRIPE_PUB_KEY})



def success(request):
    return render(request,'cart/success.html')

