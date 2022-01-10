from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Match, Bet
from accounts.models import Account, Bookie
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
from .utils import get_relevant_user_bets, get_performance, paginate_bets
from django.contrib import messages
import json
from datetime import datetime


@login_required(login_url="login")
def value_matches(request):

    # Get User Account
    account = request.user.account

    # get relevant user bets
    relevant_user_bets = get_relevant_user_bets(request)

    # Post request for user to save the bet in database
    if request.method == "POST":

        date = datetime.strptime(request.POST["date"], "%d.%m.%Y").date()

        # Get match from POST request
        match = Match.objects.get(
            date=date,
            league=request.POST["league"],
            oddspedia_match_id=request.POST["match_id"]
        )

        # Get bookie from POST request
        bookie = Bookie.objects.get(owner=account, name=request.POST["bookie"])

        # Get bet_type, odd & stake from POST request
        bet = request.POST["bet"]
        odd = Decimal(request.POST["odd"])
        stake = Decimal(request.POST["stake"])

        # Create bet
        Bet.objects.create(
            match=match,
            owner=account,
            bookie=bookie,
            bet_type=bet,
            odd=odd,
            stake=stake,
            result="open"
        )

        messages.success(
            request, f"Wette gespeichert!")

        return redirect("value_bets")

    context = {
        "page_name": "Value Wetten",
        "value_bets": relevant_user_bets,
    }

    return render(request, 'bets/valuebets2.html', context=context)


@login_required(login_url="login")
def bets(request, type):

    # Get User Account
    account = request.user.account

    # Check if bet_type is "open"
    if type == "open":

        # Set type to "open"
        type = "open"

        # filter all bets with result="open"
        all_user_bets = account.bet_set.filter(result="open")

    # Check if bet_type is "ended"
    elif type == "ended":

        # Set type to "ended"
        type = "ended"

        # exclude all bets with result="open"
        all_user_bets = account.bet_set.exclude(result="open")

    # Else: Get all user bets
    else:

        # Set type to "all"
        type = "all"

        # Get all user bets
        all_user_bets = account.bet_set.all()

    # Get bets count
    number_of_bets = all_user_bets.count()

    # paginate user bets
    paginated_bets, custom_page_range = paginate_bets(
        request, bets_query_set=all_user_bets, results_per_page=15)

    context = {
        "bets": paginated_bets,
        "number_of_bets": number_of_bets,
        "type": type,
        "custom_page_range": custom_page_range,
    }

    return render(request, 'bets/bets2.html', context=context)


def add_matches(request):

    # Open valuebets json-file from directory
    with open("C:/Users/yigit/Desktop/Matchsniper3.0/bets_data/valuebets.json", "r", encoding="utf-8") as file:
        all_value_bets = json.load(file)

    # Loop through each match in all_value_bets
    for match in all_value_bets:

        # set right date format (strptime)
        date = datetime.strptime(match["date"], "%d.%m.%Y").date()

        try:  # Try to add a new UNIQUE match to Database

            # Create new database object
            Match.objects.create(
                league=match["league"],
                date=date,
                home_team=match["home_team"],
                away_team=match["away_team"],
                oddspedia_match_id=match["match_id"],
                home_goals=0,
                away_goals=0,
                status="not started"
            )

        except IntegrityError:  # if database object already exists continue with next iteration
            continue

    return JsonResponse({"data": "Done!"})


def get_open_matches(request):

    # Get all open bets - Exclude all matches with status="ended"
    open_matches = Match.objects.all().exclude(status="ended")

    # Create lost for open matches
    open_matches_list = []

    # Loop through open matches
    for data in open_matches:

        # Get date in right string format (strftime)
        date = datetime.strftime(data.date, "%d.%m.%Y")

        # Create match object with required MatchChecker data
        match = {
            "match_id": data.oddspedia_match_id,
            "home_team": data.home_team,
            "away_team": data.away_team,
            "league": data.league,
            "date": date
        }

        # Append match to open_matches_list
        open_matches_list.append(match)

    # Return Json Data
    return JsonResponse({"data": open_matches_list})


def update_matches(request):

    # Handle POST Request
    if request.method == "POST":

        # Loop through each match in post request
        for match_data, standings in request.POST.items():

            # Extract data
            data = match_data.split("%%")

            # Extract result
            result = standings.split(" - ")

            if len(data) == 3:

                # Get date in right format (strptime)
                date = datetime.strptime(data[2], "%d.%m.%Y").date()

                try:  # Get related match from database
                    match_object = Match.objects.get(
                        league=data[1],
                        date=date,
                        oddspedia_match_id=data[0])

                except ObjectDoesNotExist:
                    # If match doesn't exist continue with next iteration
                    continue

                else:
                    if match_object.status != "ended":

                        # Add home & away goals
                        match_object.home_goals = int(result[0])
                        match_object.away_goals = int(result[1])

                        # Change match status to ended
                        match_object.status = "ended"

                        # Save changes
                        match_object.save()

                        # Get all bets for this match
                        all_bets_for_this_match = match_object.bet_set.all()

                        # Loop throgh each bet for this match
                        for bet in all_bets_for_this_match:
                            # Update result of each bet
                            bet.update_result()

    return render(request, 'bets/matches_crud.html')


@login_required(login_url="login")
def performance(request):

    # Get User Account
    account = request.user.account

    # Get performance data
    performance_data = get_performance(request)

    # Get ended bets - Exclude bets with result="open"
    all_user_bets = account.bet_set.exclude(result="open")

    # paginate all finished bets
    finished_bets, custom_page_range = paginate_bets(
        request, bets_query_set=all_user_bets, results_per_page=15)

    context = {
        "bets": finished_bets,
        "performance": performance_data,
        "custom_page_range": custom_page_range,
    }
    return render(request, 'bets/performance2.html', context=context)
