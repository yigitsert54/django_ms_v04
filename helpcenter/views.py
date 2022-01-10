from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Topic, Support
from .forms import SupportForm
from django.contrib import messages


@login_required(login_url="login")
def faq(request):

    # Get all topics
    topics = Topic.objects.all()

    context = {
        "topics": topics,
    }

    return render(request, "helpcenter/faq.html", context=context)


@login_required(login_url="login")
def single_topic(request, pk):

    # Get single topic
    topic = Topic.objects.get(id=pk)

    context = {
        "topic": topic,
    }

    return render(request, "helpcenter/single_topic.html", context=context)


@login_required(login_url="login")
def support(request):

    # Get Account
    account = request.user.account

    support_requests = account.support_set.all()

    form = SupportForm()

    # Handle POST Request
    if request.method == "POST":

        # Get MoneyForm
        form = SupportForm(request.POST)

        if form.is_valid():

            # Save request with commit=False
            support_request = form.save(commit=False)

            # Set owner of support request
            support_request.owner = account

            # Message
            messages.success(
                request, "Deine Frage ist bei uns eingegangen. Wir werden sie schnellstmöglich beantworten.")

            support_request.save()

            return redirect("support")

    context = {
        "form": form,
        "support_requests": support_requests,
    }

    return render(request, "helpcenter/support.html", context=context)


@login_required(login_url="login")
def single_support(request, pk):

    account = request.user.account

    support = Support.objects.get(owner=account, id=pk)

    if support.answered and not support.seen:
        support.seen = True
        support.save()

    context = {
        "support": support,
    }

    return render(request, "helpcenter/single_support.html", context=context)
