from django.shortcuts import get_object_or_404, redirect, render

from . import forms

from item import models as item_models
from django.contrib.auth.decorators import login_required
from . import models

# Create your views here.


@login_required
def new_conversation(request, pk):
    item = get_object_or_404(item_models.Item, pk=pk)

    if item.created_by == request.user:
        return redirect("dashboard:index")

    conversations = models.Conversation.objects.filter(item=item).filter(
        members__in=[request.user.id]
    )

    if conversations:
        pass

    if request.method == "POST":
        form = forms.ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = models.Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect("item:details", pk=item.pk)

    else:
        form = forms.ConversationMessageForm()

    return render(request, "conversation/new.html", {"form": form})


@login_required
def inbox(request):
    conversations = models.Conversation.objects.filter(members__in=[request.user.id])

    return render(request, "conversation/inbox.html", {"conversations": conversations})


@login_required
def detail(request, pk):
    conversation = models.Conversation.objects.filter(
        members__in=[request.user.id]
    ).get(pk=pk)

    if request.method == "POST":
        form = forms.ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect("conversation:detail", pk=pk)
    else:
        form = forms.ConversationMessageForm()

    return render(
        request,
        "conversation/detail.html",
        {"conversation": conversation, "form": form},
    )
