from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from .models import Product, ViewedProduct, Cart, CartItem

from django.contrib.auth.decorators import login_required

class HomePage(View):
    def get(self, request):
        products = Product.objects.all()
        viewed_products = ViewedProduct.objects.filter(user=request.user.id)

        if request.GET.get('country'):
            products = products.filter(country__contains=request.GET.get('country'))

        if request.GET.get('is_visible'):
            products = products.filter(is_visible__exact=request.GET.get('is_visible'))
        else:
            products = Product.objects.filter(is_visible=True)

        context = {
            'products': products,
            'viewed_products': viewed_products
        }

        return render(request, 'main/homepage.html', context)

    def post(self, request, *args, **kwargs):
        searched = request.POST.get('searched')
        venues = Product.objects.filter(title__contains=searched)

        context = {
            'searched': searched,
            'venues': venues
        }

        print(venues)

        return render(request, 'main/homepage.html', context)


class ProductDetail(View):
    def get(self, request, pk):
        if request.user.is_superuser:
            product = get_object_or_404(Product, id=pk)
        else:
            product = get_object_or_404(Product.objects.filter(is_visible=True), id=pk)

        if request.user is not None:
            viewed_yet = ViewedProduct.objects.filter(user=request.user, product=product)
            if viewed_yet.exists():
                viewed_yet.delete()

            viewed_product = ViewedProduct(user=request.user, product=product)
            viewed_product.save()

        context = {
            'product': product
        }

        return render(request, 'main/product-detail.html', context)


def Contacs(request):
    return render(request, 'main/Contacs.html')

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')
@login_required
def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

@login_required
def cart(request):
    cart = Cart.objects.get(user=request.user)
    context = {'cart': cart}
    return render(request, 'main/cart.html', context)