from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View


def Cabinet(request):

    context = {

    }

    return render(request, 'account/cabinet.html', context)


def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not username or not password:
            messages.error(request, 'Пожалуйста, заполните все обязательные поля')
            return redirect('login')
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, 'Неверный логин или пароль')
            return redirect('login')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home-page')

    return render(request, 'account/login.html')


def Register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if not username or not password:
            messages.error(request, 'Пожалуйста, заполните все обязательные поля')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Имя пользователя уже существует!')
            return redirect('register')

        if len(password) < 8:
            messages.error(request, 'Пароль должен содержать не менее 8 символов')
            return redirect('register')

        if not any(char.isupper() for char in password) or \
                not any(char.islower() for char in password) or \
                not any(char.isdigit() for char in password):
            messages.error(request, 'Пароль должен содержать как минимум одну ')
            messages.error(request, 'заглавную букву, одну строчную букву и одну цифру')
            return redirect('register')

        user = User.objects.create_user(first_name=first_name, username=username, password=password, email=email)
        user.save()
        login_user = authenticate(username=username, password=password)
        login(request, login_user)

        return redirect('/')

    return render(request, 'account/register.html')


def Logout(request):
    logout(request)
    return redirect('/')


class EditProfile(View):
    def get(self, request):
        return render(request, 'account/edit-profile.html')

    def post(self, request, *args, **kwargs):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']

        User.objects.filter(id=request.user.id).update(
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        return redirect('cabinet')
