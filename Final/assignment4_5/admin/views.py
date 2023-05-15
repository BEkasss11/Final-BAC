from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView

from main.models import Product


def AdminPanel(request):
    if request.user.is_superuser:
        products = Product.objects.all()

        context = {
            'products': products
        }
        return render(request, 'admin/admin-panel.html', context)
    else:
        return HttpResponse('', status=404)


class CreateProduct(View):
    template_name = 'admin/create.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        product = Product()
        cover_image = ''
        if request.FILES.get('cover_image'):
            product.cover_image = request.FILES['cover_image']
        product.title = request.POST['title']
        product.model = request.POST['model']
        product.price = request.POST['price']
        product.country = request.POST['country']
        product.manufacturer = request.POST['manufacturer']
        product.description = request.POST['description']

        product.save()
        messages.success(request, 'Продукт успешно создан!')
        return redirect('/')


def UpdateProduct(request, pk):
    if request.user.is_superuser:
        product = get_object_or_404(Product, id=pk)

        if request.method == 'POST':
            if request.FILES.get('cover_image'):
                product.cover_image = request.FILES['cover_image']
            product.title = request.POST.get('title')
            product.model = request.POST.get('model')
            product.price = request.POST.get('price')
            product.country = request.POST.get('country')
            product.manufacturer = request.POST.get('manufacturer')
            product.description = request.POST.get('description')

            is_visible = request.POST.get('is_visible', False)
            if is_visible:
                product.is_visible = True
            else:
                product.is_visible = False

            product.save()
            return redirect('admin')

        context = {
            'product': product
        }

        return render(request, 'admin/update.html', context)
    else:
        return HttpResponse('', status=404)


def DeleteProduct(request, pk):
    if request.user.is_superuser:
        product = get_object_or_404(Product, id=request.POST.get('product_id'))
        Product.objects.filter(id=product.id).delete()

        return redirect('admin')
    else:
        return HttpResponse('', status=404)


class CheckUsers(View):
    def get(self, request):
        if request.user.is_superuser:
            all_users = User.objects.all().exclude(id=request.user.id)

            context = {
                'all_users': all_users
            }

            return render(request, 'admin/check_users.html', context)

        return HttpResponse('', status=404)

    def post(self, request, *args, **kwargs):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Пользователь уже создан!')
            return redirect('check_users')
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Пользователь с этим адресом электронной почты уже создан!')
            return redirect('check_users')

        user = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()

        return redirect('check_users')


class DetailUser(DetailView):
    model = User
    template_name = 'admin/detail_user.html'


class DeleteUser(View):
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.POST.get('delete_user'))
        User.objects.filter(id=user.id).delete()

        return redirect('check_users')


class EditUserProfile(View):
    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)

        context = {
            'user': user
        }

        return render(request, 'account/edit-profile.html', context)

    def post(self, request, pk):
        user = get_object_or_404(User, id=pk)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        return redirect('detail_user', pk=user.id)