from django.shortcuts import render, redirect

from .models import Category, Photo

# pagination
from django.core.paginator import Paginator

# Forms
from .forms import PhotoForm

# from django.db.models.functions import Lower


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

    context = {
        'categories' : categories,
        # 'photos' : photos,
        'photos' : page_data
    }
    return render(request, 'photos/gallery.html', context)

def viewPhoto(request, pk):
    photo = Photo.objects.get(pk=pk)
    context = {
        'photo' : photo,
    } 
    return render(request, 'photos/photo.html', context)

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


def updatePhoto(request,pk):
    photo = Photo.objects.get(pk=pk)
    form = PhotoForm(instance=photo)
    
    context = {
        'photo' : photo,
        'form': form,
    }
    return render(request, 'photos/edit.html', context)



def delete_photo(request, pk):
    photo = Photo.objects.get(pk=pk)
    photo.delete()
    return redirect('gallery')
    