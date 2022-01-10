import string
import random
from django.contrib.auth.models import User
from .models import Account, Bookie
from bets.models import Match, Bet
from decimal import Decimal
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import json


# Get performance Data for summary section
def get_performance(request):

    # Get User Account
    account = request.user.account

    # Get all user bets
    all_user_bets = account.bet_set.all()

    # Set counter for number of bets
    bet_count = 0

    # Set counter for profit
    profit = Decimal(0)

    # Set counter for wins
    wins = 0

    # Loop through all user bets
    for bet in all_user_bets:

        if bet.match.status == "ended":  # If match status is "ended"

            # increase bet count
            bet_count += 1

            # Substract bet stake from profit
            profit -= bet.stake

            # Get bookie factor
            if bet.bookie.tax:
                factor = Decimal(0.95)
            else:
                factor = Decimal(1)

            # If bet is won..
            if bet.result == "won":

                # ..add win amount to profit
                profit += bet.odd * bet.stake * factor

                # Increase wins count
                wins += 1

    # Calculate winrate
    if bet_count > 0:
        winrate = round(wins/bet_count*100, 2)
    else:
        winrate = round(0, 2)

    # get prfit sign
    if profit > Decimal(0):
        profit_sign = "+"
    else:
        profit_sign = ""

    performance_data = {
        "bet_count": bet_count,
        "wins": wins,
        "profit": round(profit, 2),
        "winrate": winrate,
        "profit_sign": profit_sign,
    }

    return performance_data


# generate a random password for digistore purchase
def generate_password():

    # Get all ascii letters
    all_letters = string.ascii_letters

    # Create empty password string
    password = ""

    # Loop until password length is 10
    while len(password) < 10:

        # in 30% of times extract a number
        if random.choice(range(1, 101)) <= 30:

            # Get random digit from 0 to 9
            number = random.choice(range(0, 10))

            # transform digit to string
            symbol = str(number)

        # In 70% of times extract letter
        else:

            # Get random letter
            symbol = random.choice(all_letters)

        # Check if letter is not capital "i" or lower "L"
        if symbol != "I" and symbol != "l":

            # Add symbol to password
            password += symbol

    return password


# Create new digistore user
def create_new_user(request):

    # Extract email from POST request
    email = request.POST["email"].lower()

    # Check if user already exist
    try:  # Try to get user
        user = User.objects.get(username=email)

        # Create data for error response
        data_error = {
            "status": "error",
            "message": "Dieser Benutzer existiert bereits",
        }

        # return error response
        return data_error

    # if user doesn't exist
    except User.DoesNotExist:

        # Extract order id
        order_id = request.POST["order_id"]

        # Extract first name
        first_name = request.POST["address_first_name"]

        # Extract last name
        last_name = request.POST["address_last_name"]

        # generate password
        password = generate_password()

        # Create user
        user = User.objects.create_user(
            email=email,
            username=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        # Extract user account
        account = Account.objects.get(user=user)

        # Set order id for account
        account.order_id = order_id
        account.save()

        # Create data for success response
        data_success = {
            "status": "success",
            "key": f"Benutzername:{email}|Kennwort:{password}",
            "data": [],
            "headline": "Ihre Zugangsdaten",
            "show_on": [
                "receipt_page",
                "order_confirmation_email"
            ]
        }

        # return success response
        return data_success


# Get scope for performance Chart (days, weeks or months)
def get_scope(finished_user_bets):

    all_months = []
    all_weeks = []
    # Loop through all finished bets
    for bet in finished_user_bets:

        # Extract match date
        date = bet.match.date

        # Extract further & more specific date data (month.year & week.year)
        month = f"{datetime.strftime(date, '%m')}.{datetime.strftime(date, '%Y')}"
        week = f"{date.isocalendar().week}.{date.isocalendar().year}"

        # if month is not in all_month
        if month not in all_months:
            # append month to all_month
            all_months.append(month)

        # if week is not in all_weeks
        if week not in all_weeks:
            # append week to all_weeks
            all_weeks.append(week)

    # Get scope
    if len(all_months) >= 3:
        scope = "month"
    elif len(all_weeks) >= 3:
        scope = "week"
    else:
        scope = "day"

    return scope


# Get data for performance chart
def get_performance_chart_data(request):

    # Get User Account
    account = request.user.account

    # Get all finished user bets
    finished_user_bets = account.bet_set.exclude(result="open")

    # Get scope
    scope = get_scope(finished_user_bets)

    # Create labels and data lists
    labels = []
    data = []

    # Set balance
    balance = Decimal(0)

    # if scope is month
    if scope == "month":

        # Loop through each finished bet (reversed from database - date ascending)
        for bet in finished_user_bets[::-1]:

            # Extract date
            date = bet.match.date

            # Create month string (month.year)
            month = f"{datetime.strftime(date, '%m')}.{datetime.strftime(date, '%Y')}"

            # if month is not in labels
            if month not in labels:

                # if len labels is not 0 (not first data point)
                if len(labels) != 0:
                    # append balance to data
                    data.append(round(float(balance), 2))

                # append month string to labels
                labels.append(month)

            # subtract stake from balance
            balance -= bet.stake

            # if bet is won
            if bet.result == "won":

                # Get bookie factor
                if bet.bookie.tax:
                    factor = Decimal(0.95)
                else:
                    factor = Decimal(1)

                # add win amount to balance
                balance += bet.stake * bet.odd * factor

        # Add last balance to data after loop is finished
        data.append(round(float(balance), 2))

        return labels, data

    # if scope is week
    elif scope == "week":

        # Create list for weeks
        weeks = []

        # Loop through each finished bet (reversed from database - date ascending)
        for bet in finished_user_bets[::-1]:

            # Extract date
            date = bet.match.date

            # Create week string (week.year)
            week = f"{date.isocalendar().week}.{date.isocalendar().year}"
            # if week is not in weeks list
            if week not in weeks:

                # if len weeks is not 0 (not first data point)
                if len(weeks) != 0:
                    # append balance to data
                    data.append(round(float(balance), 2))

                # append week string to weeks list
                weeks.append(week)

            # subtract stake from balance
            balance -= bet.stake

            # if bet is won
            if bet.result == "won":

                # Get bookie factor
                if bet.bookie.tax:
                    factor = Decimal(0.95)
                else:
                    factor = Decimal(1)

                # add win amount to balance
                balance += bet.stake * bet.odd * factor

        # Add last balance to data after loop is finished
        data.append(round(float(balance), 2))

        n = 0
        # Loop through each week to create labels for each week
        for w in weeks:

            # Add 1 to n
            n += 1

            # Append "Woche n" to labels
            labels.append(f"Woche {n}")

        return labels, data

    # if scope is day
    else:

        # Loop through each finished bet (reversed from database - date ascending)
        for bet in finished_user_bets[::-1]:

            # Create date string (dd.mm.yyyy)
            date = datetime.strftime(bet.match.date, '%d.%m.%Y')

            # if date not in labels
            if date not in labels:

                # if len labels is not 0 (not first data point)
                if len(labels) != 0:
                    # append balance to data
                    data.append(round(float(balance), 2))

                # append date string to labels
                labels.append(date)

            # subtract stake from balance
            balance -= bet.stake

            # if bet is won
            if bet.result == "won":

                # Get bookie factor
                if bet.bookie.tax:
                    factor = Decimal(0.95)
                else:
                    factor = Decimal(1)

                # add win amount to balance
                balance += bet.stake * bet.odd * factor

        # Add last balance to data after loop is finished
        data.append(round(float(balance), 2))

        return labels, data


# Calculate stake for a bet (balance = total_balance, stake = bet_stake_advice )
def calculate_rounded_stake(balance, stake):

    # Calculate exatct stake
    number = balance * stake

    # round down exact stake to 0.5
    rounded_stake = int(number*2)/2

    # return with 2 decimal places -> "{:.2f}"
    return "{:.2f}".format(rounded_stake)


def paginate_bookie_bets(request, bookiebets_query_set, results_per_page):

    page = request.GET.get("page")
    paginator = Paginator(object_list=bookiebets_query_set,
                          per_page=results_per_page)

    try:
        bets = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        bets = paginator.page(page)
    except EmptyPage:
        bets = []

    left_page_range = int(page) - 4
    right_page_range = 1 + int(page) + 4

    if left_page_range < 1:
        left_page_range = 1

    if right_page_range > paginator.num_pages:
        right_page_range = paginator.num_pages + 1

    temporary_range = range(left_page_range, right_page_range)

    if len(temporary_range) < 9:

        if right_page_range < 10:
            right_page_range = 10
            left_page_range = 1
            if right_page_range > paginator.num_pages:
                right_page_range = paginator.num_pages + 1
        else:
            left_page_range = right_page_range - 9

    custom_page_range = range(left_page_range, right_page_range)

    return bets, custom_page_range


def get_relevant_user_bets(request):

    # Get User Account
    account = request.user.account
    total_balance = account.total_balance

    with open("C:/Users/yigit/Desktop/Matchsniper3.0/bets_data/valuebets.json", "r", encoding="utf-8") as file:
        all_value_bets = json.load(file)

    relevant_user_bets = []
    for match in all_value_bets:

        # Get date in datetime format
        date = datetime.strptime(match["date"], "%d.%m.%Y").date()

        # filter related match from database
        match_object = Match.objects.filter(
            league=match["league"], date=date, oddspedia_match_id=match["match_id"])

        # Check if match exixts in database
        if match_object.exists():

            match_object = Match.objects.get(
                league=match["league"], date=date, oddspedia_match_id=match["match_id"])

            # Try to find bet (for match & account) to see if the user has already a bet for that match
            bet_object = Bet.objects.filter(match=match_object, owner=account)

            if bet_object.exists():
                continue

            # Dict for bet adivice with maximum value for each match
            max_value_advice = {}

            # Loop through each bet_type, bookie_data in value bets
            for bet_type, bookie_data in match["value_bets"].items():

                # Loop through each advice
                for data in bookie_data:

                    # filter related user-bookie from database
                    bookie_object = Bookie.objects.filter(
                        owner=account, name=data["bookie"])

                    if bookie_object.exists():

                        bookie = Bookie.objects.get(
                            owner=account, name=data["bookie"])

                        # If bet_type not in bet_advices add it to dict
                        if bet_type not in max_value_advice:
                            max_value_advice[bet_type] = {
                                "bookie": "",
                                "value": 0,
                                "possibility": 0,
                                "odd": 0,
                                "stake": 0
                            }

                        # Check if current value is greater than advice value
                        if data["value"] > max_value_advice[bet_type]["value"]:

                            # Get current stake advice
                            stake = Decimal(data["stake"])
                            personal_bet_stake = calculate_rounded_stake(
                                total_balance, stake)

                            # Check if bookie balance is greater than bet_stake
                            if Decimal(personal_bet_stake) <= bookie.balance:

                                # Reset values of max_value_advice
                                max_value_advice[bet_type]["bookie"] = data["bookie"]
                                max_value_advice[bet_type]["value"] = data["value"]
                                max_value_advice[bet_type]["possibility"] = data["possibility"]
                                max_value_advice[bet_type]["odd"] = data["odd"]
                                max_value_advice[bet_type]["stake"] = personal_bet_stake

            # Continue with next steps if len(max_value_advice) > 0
            if len(max_value_advice) > 0:

                # dict for the final bet advice
                final_bet_advice = {
                    "bet_type": "",
                    "bookie": "",
                    "possibility": 0,
                    "odd": 0,
                    "stake": 0
                }

                # Loop through each advice in bet_advices for this match to find final advice with highest possibility
                for bet_type, data in max_value_advice.items():
                    if data["possibility"] > final_bet_advice["possibility"]:
                        final_bet_advice["bet_type"] = bet_type
                        final_bet_advice["bookie"] = data["bookie"]
                        final_bet_advice["possibility"] = data["possibility"]
                        final_bet_advice["odd"] = data["odd"]
                        final_bet_advice["stake"] = data["stake"]

                # Create bet_string
                if final_bet_advice["bet_type"] == "home":
                    bet_string = f'{match["home_team"]}(1)'

                elif final_bet_advice["bet_type"] == "draw":
                    bet_string = 'Unentschieden(X)'

                elif final_bet_advice["bet_type"] == "away":
                    bet_string = f'{match["away_team"]}(2)'

                else:
                    bet_string = final_bet_advice["bet_type"]

                # Create relevant bet
                relevant_bet = {
                    "match_id": match["match_id"],
                    "league": match["league"],
                    "date": match["date"],
                    "home_team": match["home_team"],
                    "away_team": match["away_team"],
                    "bet": bet_string,
                    "odd": final_bet_advice["odd"],
                    "stake": final_bet_advice["stake"],
                    "bookie": final_bet_advice["bookie"],
                }

                # Add relevant bet to relevant_user_bets list
                relevant_user_bets.append(relevant_bet)

    # Sort relevant user bets for date
    relevant_user_bets.sort(
        key=lambda match_: datetime.strptime(match_["date"], "%d.%m.%Y"))

    return relevant_user_bets
