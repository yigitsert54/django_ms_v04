from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from .forms import AddBookieForm, MoneyForm, AccountForm, NotificationsForm
from .models import Account, Bookie
from decimal import Decimal
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .utils import (
    create_new_user,
    get_performance,
    get_performance_chart_data,
    get_relevant_user_bets,
    paginate_bookie_bets)
import json
from django.core.validators import validate_email
from django.forms import ValidationError


@login_required(login_url="login")
def dashboard(request):

    # Get user account
    account = request.user.account

    # Get performance fpr summary section
    summary_data = get_performance(request)

    # Get labels and data of performance chart
    p_chart_labels, p_chart_data = get_performance_chart_data(request)

    # Get open bets
    open_bets = account.bet_set.filter(result="open").reverse()

    # get relevant user bets
    value_bets = get_relevant_user_bets(request)

    # Get all user bookies
    bookies = account.bookie_set.all()

    # Create list for all user bookies
    all_bookies = []

    # Add all bookies to list
    for bookie in bookies:
        all_bookies.append(bookie)

    # Sort bookie list
    all_bookies.sort(key=lambda bookie: bookie.balance, reverse=True)

    context = {
        "page_name": "Dashboard",
        "performance": summary_data,
        "performance_chart": {
            "labels": p_chart_labels,
            "data": p_chart_data
        },
        "open_bets": open_bets,
        "value_bets": value_bets,
        "bookies": all_bookies,
    }

    return render(request, "accounts/dashboard2.html", context=context)


def user_login(request):

    # Check if user is already logged in
    if request.user.is_authenticated:
        # redirect to dashboard
        return redirect("dashboard")

    # Handle login request
    if request.method == "POST":

        # Get username and password from POST request
        username = request.POST["username"].lower()
        password = request.POST["password"]

        try:  # Get user from username
            user = User.objects.get(username=username)
        except:  # If username doesn't exist
            messages.error(request, "Nutzer existiert nicht!")
        else:  # If user does exist authenticate login request
            user = authenticate(request, username=username, password=password)

            # If authentication was successful (user is not None)
            if user is not None:

                # Login user
                login(request, user)

                # Get next string from url
                next = request.GET.get("next")

                # if there is a next string...
                if next != "":
                    # .. redirect to next
                    return redirect(next)
                else:  # if there is no next string

                    # redirect to dashboard
                    return redirect("dashboard")

            else:  # If authentication was NOT successful (wrong password)
                messages.error(request, "Falsches Passwort!")

    return render(request, "accounts/login2.html")


@login_required(login_url="login")
def user_logout(request):

    logout(request)
    return redirect("login")


@login_required(login_url="login")
def bookies(request):

    # Get user account
    account = request.user.account

    # Get all user bookies
    bookies = account.bookie_set.all()

    # Create list bookies list
    all_bookies = []

    # Create balance variable for total balance
    balance = Decimal(0)

    # Loop through each bookie
    for bookie in bookies:

        # Add bookie_balance to total balance
        balance += bookie.balance

        # Add bookie to bookies list
        all_bookies.append(bookie)

    # Sort bookie list
    all_bookies.sort(key=lambda bookie: bookie.balance, reverse=True)

    context = {
        "page_name": "Wettanbieter",
        "bookies": all_bookies,
        "balance": balance,
    }
    return render(request, 'accounts/bookies2.html', context=context)


@login_required(login_url="login")
def single_bookie(request, pk):

    # Get single bookie
    single_bookie = Bookie.objects.get(id=pk)

    # Get all bets count
    bets_count = single_bookie.bet_set.all().count()

    bets, custom_page_range = paginate_bookie_bets(
        request, bookiebets_query_set=single_bookie.bet_set.all(), results_per_page=15)

    context = {
        "page_name": f"{single_bookie.name.capitalize()}",
        "bookie": single_bookie,
        "bets": bets,
        "custom_page_range": custom_page_range,
        "bets_count": bets_count,
    }
    return render(request, 'accounts/single_bookie2.html', context=context)


@login_required(login_url="login")
def add_bookie(request):

    # Get user account
    account = request.user.account

    # Get add bookie form
    form = AddBookieForm()

    # Define strong bookies
    strong_bookies = ["tipico"]

    # Get all bookies
    bookies = account.bookie_set.all()

    # Create bookie data for data attribute in html (identify all bookies that already exist)
    bookie_data = ""

    # Loop though each bookie
    for bookie in bookies:

        # Add bookie name to bookie data
        bookie_data += bookie.name

        # Add "+"
        bookie_data += "+"

    # Handle POST request
    if request.method == "POST":

        # Get Add bookie form
        form = AddBookieForm(request.POST)

        if form.is_valid():

            # Extract bookie with commit = False
            bookie = form.save(commit=False)

            # If no bookie was sent
            if bookie.name is None:

                # messsage
                messages.error(request, "Bitte einen Wettanbieter auswählen!")

                # return to add_bookie page again
                return redirect("add_bookie")

            # if bookie already exists
            elif account.bookie_set.filter(name=bookie.name).exists():

                # message
                messages.error(
                    request, "Dieser Wettanbieter existiert bereits!")

                # return to add_bookie page again
                return redirect("add_bookie")

            # If no balance/invested_stake was typed
            elif bookie.invested_stake is None or bookie.invested_stake == Decimal(0):
                bookie.invested_stake = Decimal(0)

                # message: Bookie added without stake
                messages.info(
                    request, "Wettanbieter hinugefügt - Kein Wettkapital!")

            # If there's no error
            else:

                # message: Success
                messages.success(
                    request, f'Wettanbieter "{bookie.name.capitalize()}" hinugefügt - {bookie.invested_stake}€ Wettkapital!')

            # Set withdrawed stake to 0
            bookie.withdrawed_stake = 0

            # Set bookie owner to account
            bookie.owner = request.user.account

            # bookie name is strong bookie
            if request.POST["name"].lower() in strong_bookies:

                # Set bookie tax to False
                bookie.tax = False

            else:  # If bookie not in strong bookies

                # Set bookie tax to True
                bookie.tax = True

            bookie.save()

            # return to bookies page
            return redirect("bookies")

    context = {
        "form": form,
        "purpose": "add bookie",
        "bookie_data": bookie_data[0:-1]
    }

    return render(request, 'accounts/bookies_crud.html', context=context)


@login_required(login_url="login")
def deposit_money(request, pk):

    # Get bookie
    bookie = Bookie.objects.get(id=pk)

    # Get MoneyForm
    form = MoneyForm(instance=bookie)

    if request.method == "POST":

        # Get MoneyForm
        form = MoneyForm(request.POST, instance=bookie)

        if form.is_valid():

            #  save bookie with commit=False
            bookie = form.save(commit=False)

            # Extract amount from POST request
            amount = Decimal(request.POST["amount"])

            # if no amount was typed
            if amount == Decimal(0) or amount is None:

                # message
                messages.error(request, "Bitte Betrag eingeben!")

                # redirect to deposit money page again
                return redirect("deposit_money", pk)

            # add amount to invested stake
            bookie.invested_stake += amount

            bookie.save()

            # message
            messages.success(
                request, f"{amount}€ eingezahlt!")

            # redirect to single bookie page
            return redirect("single_bookie", pk)

    context = {
        "purpose": "deposit",
        "bookie": bookie,
        "form": form,
    }
    return render(request, 'accounts/bookies_crud.html', context=context)


@login_required(login_url="login")
def withdraw_money(request, pk):

    # Get bookie
    bookie = Bookie.objects.get(id=pk)

    # Get MoneyForm
    form = MoneyForm(instance=bookie)

    if request.method == "POST":

        # Get MoneyForm
        form = MoneyForm(request.POST, instance=bookie)

        if form.is_valid():

            # Save bookie with commit=False
            bookie = form.save(commit=False)

            # Extract amount from POST request
            amount = Decimal(request.POST["amount"])

            # if no amount was typed
            if amount == Decimal(0) or amount is None:

                # message
                messages.error(request, "Bitte Betrag eingeben!")

                # redirect to withdraw money page again
                return redirect("withdraw_money", pk)

            # if amount is smaller than balance (if user has got enough money)
            elif amount <= bookie.balance:

                # add amount to withdrawed stake
                bookie.withdrawed_stake += amount
                bookie.save()

                # success message
                messages.success(
                    request, f"{bookie.name.capitalize()}: {amount}€ ausgezahlt!")

                # redirect to single_bookie page
                return redirect("single_bookie", pk)

            # if amount is greater than balance (if user hasn't got enough money)
            else:

                # error message
                messages.error(
                    request, f"Nicht genug Wettkapital - Max. {bookie.balance}€ auszahlbar!")

                # redirect to withdraw money page again
                return redirect("withdraw_money", pk)

    context = {
        "purpose": "withdraw",
        "bookie": bookie,
        "form": form,
    }
    return render(request, 'accounts/bookies_crud.html', context=context)


@login_required(login_url="login")
def settings(request):
    account = request.user.account

    # Create password change form
    pw_form = PasswordChangeForm(user=request.user)
    account_form = AccountForm(instance=account)
    notifications_form = NotificationsForm(instance=account)

    context = {
        "pw_form": pw_form,
        "account_form": account_form,
        "notifications_form": notifications_form,
    }
    return render(request, 'accounts/settings.html', context=context)


@login_required(login_url="login")
def change_password(request):

    # Handle POST request
    if request.method == "POST":

        # Get form data
        form = PasswordChangeForm(user=request.user, data=request.POST)

        # Check if form is valid
        if form.is_valid():

            form.save()

            # message
            messages.success(request, f"Passwort geändert!")

            # Update session
            update_session_auth_hash(request, form.user)

            # redirect to settings page again
            return redirect("settings")

        # If form is not valid
        else:

            # Create custom error messages
            error_messages = {
                "password_incorrect": "Dein aktuelles Passwort wurde falsch eingegeben!",
                "password_mismatch": "Die beiden Passwörter stimmten nicht überein!",
                "password_too_short": "Dieses Passwort ist zu kurz. Es muss mindestens 8 Zeichen enthalten!",
                "password_entirely_numeric": "Passwort darf nicht ausschließlich aus Zahlen bestehen!",
                "password_too_similar": "Das Passwort ähnelt deinen persönlichen Daten zu sehr!",
                "password_too_common": "Passwort darf kein häufig verwendetes Passwort sein!",
            }

            # Load all error messages from validation errors
            error_dict = json.loads(form.errors.as_json())

            # Set error message
            error_message = ""

            # Loop through each custom error
            for code, msg in error_messages.items():

                # Loop throgh each validation error
                for label, error_list in error_dict.items():

                    # Loop through each error in list
                    for error in error_list:

                        # Check if the codes macth
                        if code == error["code"]:

                            # Set error_message to custom msg
                            error_message = msg

                            # Create error message
                            messages.error(request, msg)

                            # redirect to settings page again
                            return redirect("settings")

            # Check if no error message was set
            if error_message == "":

                # Create a general error message
                messages.error(request, "Das hat leider nicht geklappt!")

                # redirect to settings page again
                return redirect("settings")

    # redirect to settings page again
    return redirect("settings")


@login_required(login_url="login")
def edit_account(request):

    # Get User account
    account = request.user.account

    # Handle POST request
    if request.method == "POST":

        # Get form
        form = AccountForm(request.POST, instance=account)

        # Check if form is valid
        if form.is_valid():

            # Save form data without commiting
            account = form.save(commit=False)

            # Extract POST data
            email = request.POST["email"].lower()
            first_name = request.POST["first_name"].capitalize()
            last_name = request.POST["last_name"].capitalize()

            # Check if names are valid
            if len(first_name) <= 1 or len(last_name) <= 1:

                # Error message
                messages.error(request, f"Vor- oder Nachname ungültig!")
                # redirect to settings page again
                return redirect("settings")

            try:  # Validate Email
                validate_email(email)

            except ValidationError:  # If email is NOT valid
                # Error message
                messages.error(request, f"Bitte eine gültige E-Mail eingeben!")

                # redirect to settings page again
                return redirect("settings")

            else:  # If email is valid

                # Set account values to POST data
                account.first_name = first_name
                account.last_name = last_name
                account.email = email

                # message
                messages.success(request, f"Passwort geändert!")

                account.save()

                # redirect to settings page again
                return redirect("settings")

    # redirect to settings page again
    return redirect("settings")


@login_required(login_url="login")
def edit_notifications(request):

    # Get User account
    account = request.user.account

    # Handle POST request
    if request.method == "POST":

        # Get form
        form = NotificationsForm(request.POST, instance=account)

        # Check if form is valid
        if form.is_valid():

            # Save form
            form.save()

            # Message
            messages.success(request, f"Einstellungen gespeichert!")

            # redirect to settings page again
    return redirect("settings")

    # redirect to settings page again
    return redirect("settings")


@csrf_exempt
def digistore_registration(request):

    if request.method == "POST":

        data = create_new_user(request)

        return JsonResponse(data)
