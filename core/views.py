from django.shortcuts import redirect, render
from item import models as item_models
from .forms import Signup
# Create your views here.


def index(request):
    items = item_models.Item.objects.all()
    categories = item_models.Category.objects.all()
    return render(request, 'core/index.html', {
        'items': items,
        "categories": categories
    })


def contact(request):
    return render(request, 'core/contact.html', {})


def signup(request):

    if request.method == 'POST':
        form = Signup(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = Signup()
    return render(request, 'core/signup.html', {'form': form})


