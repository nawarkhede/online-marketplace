from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from item import models as item_models

# Create your views here.


@login_required
def index(request):
    items = item_models.Item.objects.filter(created_by=request.user)
    return render(request, "dashboard/index.html", {"items": items})
