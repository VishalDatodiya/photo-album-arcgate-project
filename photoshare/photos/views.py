from django.shortcuts import render, redirect

from .models import Category, Photo, User

# pagination
from django.core.paginator import Paginator

# Forms
from .forms import PhotoForm, UserForm, UserUpdateForm
# from django.contrib.auth.forms import UserCreationForm

# flash messages 
from django.contrib import messages

# Authentication
from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required




def loginPage(request):

    if request.user.is_authenticated:
        return redirect('gallery')

    page = 'login'

    if request.method == 'POST':
        # username = request.POST.get('username').lower()
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, email=email, password=password)
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


def userProfile(request, pk):
    user = User.objects.get(pk=pk)
    # getting the values of particular users data that what it added.
    # The _set is a reverse lookup class variable django puts in for you.
    # here photo_set.all  => photo is model and using _set, all is method
    photos = user.photo_set.all()
    context = {
        'user': user,
        'photos': photos,
    }
    return render(request, 'photos/profile.html', context)

def userRegistration(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('gallery')
        else:
            messages.error(request, 'An error Occurred during Registration. Please Try again!')


    context = {
        'form' : form,
    }
    return render(request, 'photos/login_registration.html', context)

def userUpdate(request):
    user_name = request.user
    form = UserUpdateForm(instance=user_name)
    # if request.user.is_authenticated:
    #     return redirect('gallery')

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user_name)
        if form.is_valid(): 
            form.save(commit=False)
            return redirect('gallery')
    context = {
        'form':form,
    }
    return render(request, 'photos/update_profile.html', context)


def gallery(request):
    
    category = request.GET.get('category')
    
    if category == None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(category__name__icontains=category)
    categories = Category.objects.extra(select={'lower_name':'lower(name)'}).order_by('lower_name')
    # categories = Category.objects.all(lower_name=Lower('name')).order_by('-name')

    # pagination 
    paginator = Paginator(photos, 9)
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
            image = image,
            place = data['place']
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
        # if request.method == 'POST':
        photo.delete()
        return redirect('gallery')
        
        # return render(request,'photos/delete.html', {'photo': photo})
    else:
        return redirect('gallery')