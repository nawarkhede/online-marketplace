from django.shortcuts import get_object_or_404, redirect, render
from . import models
from django.contrib.auth.decorators import login_required
from .forms import NewItemForm, EdittemForm
from item import models as item_models
from django.db.models import Q

# Create your views here.


def details(request, pk):
    item = get_object_or_404(models.Item, pk=pk)
    related_items = models.Item.objects.filter(category=item.category).exclude(pk=pk)
    return render(
        request, "item/details.html", {"item": item, "related_items": related_items}
    )


@login_required
def newitem(request):
    if request.method == "POST":
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect("item:details", pk=item.pk)

    else:
        form = NewItemForm()
    return render(request, "item/form.html", {"form": form, "title": "Add new item"})


@login_required
def edit(request, pk):
    item = get_object_or_404(item_models.Item, pk=pk, created_by=request.user)
    if request.method == "POST":
        form = EdittemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect("item:details", pk=item.pk)

    else:
        form = EdittemForm(instance=item)
    return render(request, "item/form.html", {"form": form, "title": "Edit item"})


@login_required
def delete(request, pk):
    item = get_object_or_404(item_models.Item, pk=pk, created_by=request.user)
    item.delete()
    return redirect("dashboard:index")


def items(request):
    query = request.GET.get("query")
    category_id = request.GET.get("category_id")
    categories = item_models.Category.objects.all()

    items = item_models.Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(
        request,
        "item/items.html",
        {
            "items": items,
            "query": query,
            "categories": categories,
            "category_id": category_id,
        },
    )
