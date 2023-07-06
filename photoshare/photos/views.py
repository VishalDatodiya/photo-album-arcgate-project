from django.shortcuts import render, redirect

from .models import Category, Photo

# pagination
from django.core.paginator import Paginator

# Forms
from .forms import PhotoForm

# flash messages 
from django.contrib import messages

# Authentication
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User


# Authenticatetion
from django.contrib.auth.decorators import login_required

from django.contrib.auth .forms import UserCreationForm



def loginPage(request):

    if request.user.is_authenticated:
        return redirect('gallery')

    page = 'login'

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('gallery')
        else:
            messages.error(request, "password does not match")

    context = {
        'page' : page,
    }

    return render(request, 'photos/login_registration.html', context)

def logoutPage(request):
    # it will delete the session or token  -> inspect - > application -> coockies
    logout(request)
    return redirect('gallery')


def userRegistration(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('gallery')
        else:
            messages.error(request, 'An error Occurred during Registration. Please Try again!')


    context = {
        'form' : form,
    }
    return render(request, 'photos/login_registration.html', context)

def gallery(request):
    
    category = request.GET.get('category')
    
    if category == None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(category__name__icontains=category)
    categories = Category.objects.extra(select={'lower_name':'lower(name)'}).order_by('lower_name')
    # categories = Category.objects.all(lower_name=Lower('name')).order_by('-name')

    # pagination 
    paginator = Paginator(photos, 6)
    page_numer = request.GET.get('page')
    page_data = paginator.get_page(page_numer)
    
    photo_count = photos.count()

    context = {
        'categories' : categories,
        # 'photos' : photos,
        'photos' : page_data,
        'photo_count' : photo_count,
    }
    return render(request, 'photos/gallery.html', context)

def viewPhoto(request, pk):
    photo = Photo.objects.get(pk=pk)
    context = {
        'photo' : photo,
    } 
    return render(request, 'photos/photo.html', context)

@login_required(login_url='/login')
def addPhoto(request):
    categories = Category.objects.all()
    form = PhotoForm()
    if request.method == 'POST':
        category_name = request.POST.get('category')
        data = request.POST
        image = request.FILES.get('image')
        
        # if data['category'] != 'none':
        #     category = Category.objects.get(id=data['category'])
        # elif data['category_new'] != '':
        #     category, created = Category.objects.get_or_create(name=data['category_new'])
        # else:
        #     category = None
        
        category, created = Category.objects.get_or_create(name=category_name)

        photo = Photo.objects.create(
            user = request.user,
            category = category,
            description = data['description'],
            image = image
        )
        return redirect('gallery')
        
    context = {
        'form': form,   
        'categories' : categories,
    }
    return render(request, 'photos/add.html', context)

@login_required(login_url='/login')
def updatePhoto(request,pk):
    photo = Photo.objects.get(pk=pk)
    form = PhotoForm(instance=photo)
    if request.user == photo.user:
        if request.method == 'POST':
            form = PhotoForm(request.POST, request.FILES, instance=photo)
            if form.is_valid():
                form.save()
                return redirect('gallery')
            
        context = {
            'photo' : photo,
            'form': form,
        }
        return render(request, 'photos/edit.html', context)
    else:
        return redirect('gallery')


@login_required(login_url='/login')
def delete_photo(request, pk):
    photo = Photo.objects.get(pk=pk)
    if request.user == photo.user:
        if request.method == 'POST':
            photo.delete()
            return redirect('gallery')

        return render(request,'photos/delete.html', {'photo': photo})
    else:
        return redirect('gallery')