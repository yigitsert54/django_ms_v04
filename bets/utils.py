from .models import Match, Bet
from accounts.models import Account, Bookie
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import json


def calculate_rounded_stake(balance, stake):
    number = balance * stake
    rounded_stake = int(number*2)/2
    return "{:.2f}".format(rounded_stake)


def get_relevant_user_bets(request):

    # Get User Account
    account = request.user.account
    total_balance = account.total_balance

    with open("C:/Users/yigit/Desktop/Matchsniper3.0/bets_data/valuebets.json", "r", encoding="utf-8") as file:
        all_value_bets = json.load(file)

    league_names = {
        "germany_1": "DE - 1. Bundesliga",
        "germany_2": "DE - 2. Bundesliga",
        "germany_3": "DE - 3. Liga",
        "turkey_1": "TUR - Süper Lig",
        "spain_1": "ESP - La Liga Primera División",
        "spain_2": "ESP - Segunda División",
        "england_1": "ENG - Premier League",
        "england_2": "ENG - EFL Championship",
        "france_1": "FR - Ligue 1",
        "italy_1": "ITA - Serie A",
        "netherlands_1": "NED - Eredivisie",
        "belgium_1": "BEL - Division 1A",
        "norway_1": "NOR - Eliteserien",
        "sweden_1": "SWE - Fotbollsallsvenskan",
        "USA": "USA - Major League Soccer",
        "denmark_1": "DEN - Superliga",
        "champions_league": "EU - UEFA Champions League",
        "europa_league": "EU - UEFA Europa League",
        "euro_2020": "Europameisterschaft 2020/2021"
    }

    league_urls = {
        "tipico": {
            "germany_1": "https://sports.tipico.de/de/alle/fussball/deutschland/bundesliga",
            "germany_2": "https://sports.tipico.de/de/alle/fussball/deutschland/2-bundesliga",
            "germany_3": "https://sports.tipico.de/de/alle/fussball/deutschland/3-liga",
            "turkey_1": "https://sports.tipico.de/de/alle/fussball/tuerkei/sueper-lig",
            "spain_1": "https://sports.tipico.de/de/alle/fussball/spanien/la-liga",
            "spain_2": "https://sports.tipico.de/de/alle/fussball/spanien/la-liga-2",
            "england_1": "https://sports.tipico.de/de/alle/fussball/england/premier-league",
            "england_2": "https://sports.tipico.de/de/alle/fussball/england/championship",
            "france_1": "https://sports.tipico.de/de/alle/fussball/frankreich/ligue-1",
            "italy_1": "https://sports.tipico.de/de/alle/fussball/italien/serie-a",
            "netherlands_1": "https://sports.tipico.de/de/alle/fussball/niederlande/eredivisie",
            "belgium_1": "https://sports.tipico.de/de/alle/fussball/belgien/first-division-a",
            "norway_1": "https://sports.tipico.de/de/alle/fussball/norwegen/eliteserien",
            "sweden_1": "https://sports.tipico.de/de/alle/fussball/schweden/allsvenskan",
            "USA": "https://sports.tipico.de/de/alle/fussball/usa/mls",
            "denmark_1": "https://sports.tipico.de/de/alle/fussball/daenemark/superligaen",
        },
        "bet-at-home": {
            "germany_1": "https://www.bet-at-home.de/de/sport/fussball/deutschland/bundesliga/2277364",
            "germany_2": "https://www.bet-at-home.de/de/sport/fussball/deutschland/2-bundesliga/2277375",
            "germany_3": "https://www.bet-at-home.de/de/sport/fussball/deutschland/3-liga/2277504",
            "turkey_1": "https://www.bet-at-home.de/de/sport/fussball/turkei/super-lig/2278055",
            "spain_1": "https://www.bet-at-home.de/de/sport/fussball/spanien/primera-division/2277640",
            "spain_2": "https://www.bet-at-home.de/de/sport/fussball/spanien/segunda-division/2277644",
            "england_1": "https://www.bet-at-home.de/de/sport/fussball/england/premier-league/2277590",
            "england_2": "https://www.bet-at-home.de/de/sport/fussball/england/championship/2277594",
            "france_1": "https://www.bet-at-home.de/de/sport/fussball/frankreich/ligue-1/2277664",
            "italy_1": "https://www.bet-at-home.de/de/sport/fussball/italien/serie-a/2277626",
            "netherlands_1": "https://www.bet-at-home.de/de/sport/fussball/niederlande/eredivisie/2277880",
            "belgium_1": "https://www.bet-at-home.de/de/sport/fussball/belgien/pro-league/2277899",
            "norway_1": "https://www.bet-at-home.de/de/sport/fussball/norwegen/eliteserien/2278225",
            "sweden_1": "https://www.bet-at-home.de/de/sport/fussball/schweden/allsvenskan/2278251",
            "USA": "https://www.bet-at-home.de/de/sport/fussball/usa/major-league-soccer/2278775",
            "denmark_1": "https://www.bet-at-home.de/de/sport/fussball/danemark/superligaen/2278084",
        },
        "bet365": {
            "germany_1": "https://www.bet365.de/#/AC/B1/C1/D1002/E62233151/G40/",
            "germany_2": "https://www.bet365.de/#/AC/B1/C1/D1002/E62233179/G40/",
            "germany_3": "https://www.bet365.de/#/AC/B1/C1/D1002/E62488674/G40/",
            "turkey_1": "https://www.bet365.de/#/AC/B1/C1/D1002/E63190999/G40/",
            "spain_1": "https://www.bet365.de/#/AC/B1/C1/D1002/E62271413/G40/",
            "spain_2": "https://www.bet365.de/#/AC/B1/C1/D1002/E62675519/G40/",
            "england_1": "https://www.bet365.de/#/AC/B1/C1/D1002/E61683472/G40/",
            "england_2": "https://www.bet365.de/#/AC/B1/C1/D1002/E61981774/G40/",
            "france_1": "https://www.bet365.de/#/AC/B1/C1/D1002/E62341993/G40/",
            "italy_1": "https://www.bet365.de/#/AC/B1/C1/D1002/E62863982/G40/",
            "netherlands_1": "https://www.bet365.de/#/AC/B1/C1/D1002/E62415349/G40/",
            "belgium_1": "https://www.bet365.de/#/AC/B1/C1/D1002/E61899552/G40/",
            "norway_1": "https://www.bet365.de/#/AC/B1/C1/D13/E59833624/G40/",
            "sweden_1": "https://www.bet365.de/#/AC/B1/C1/D13/E61379101/G40/",
            "USA": "https://www.bet365.de/#/AC/B1/C1/D13/E59091228/G40/",
            "denmark_1": "https://www.bet365.de/#/AC/B1/C1/D13/E62162538/G40/",
        },
        "bildbet": {
            "germany_1": "https://www.bildbet.de/de-de/sports/240/meetings/6316510/all",
            "germany_2": "https://www.bildbet.de/de-de/sports/240/meetings/130019110/all",
            "germany_3": "#",
            "turkey_1": "https://www.bildbet.de/de-de/sports/240/meetings/20548410/all",
            "spain_1": "https://www.bildbet.de/de-de/sports/240/meetings/6320610/all",
            "spain_2": "https://www.bildbet.de/de-de/sports/240/meetings/6378210/all",
            "england_1": "https://www.bildbet.de/de-de/sports/240/meetings/6323610/all",
            "england_2": "https://www.bildbet.de/de-de/sports/240/meetings/6228010/all",
            "france_1": "https://www.bildbet.de/de-de/sports/240/meetings/6270510/all",
            "italy_1": "https://www.bildbet.de/de-de/sports/240/meetings/6317710/all",
            "netherlands_1": "#",
            "belgium_1": "https://www.bildbet.de/de-de/sports/240/meetings/6468110/all",
            "norway_1": "#",
            "sweden_1": "#",
            "USA": "#",
            "denmark_1": "#",
        },
        "betway": {
            "germany_1": "https://sports.betway.de/de/sports/grp/soccer/germany/bundesliga",
            "germany_2": "https://sports.betway.de/de/sports/grp/soccer/germany/2-bundesliga",
            "germany_3": "https://sports.betway.de/de/sports/grp/soccer/germany/3-liga",
            "turkey_1": "https://sports.betway.de/de/sports/grp/soccer/turkey/super-lig",
            "spain_1": "https://sports.betway.de/de/sports/grp/soccer/spain/la-liga",
            "spain_2": "https://sports.betway.de/de/sports/grp/soccer/spain/la-liga-2",
            "england_1": "https://sports.betway.de/de/sports/grp/soccer/england/premier-league",
            "england_2": "https://sports.betway.de/de/sports/grp/soccer/england/championship",
            "france_1": "https://sports.betway.de/de/sports/grp/soccer/france/ligue-1",
            "italy_1": "https://sports.betway.de/de/sports/grp/soccer/italy/serie-a",
            "netherlands_1": "https://sports.betway.de/de/sports/grp/soccer/netherlands/eredivisie",
            "belgium_1": "https://sports.betway.de/de/sports/grp/soccer/belgium/first-division-a",
            "norway_1": "https://sports.betway.de/de/sports/grp/soccer/norway/eliteserien",
            "sweden_1": "https://sports.betway.de/de/sports/grp/soccer/sweden/allsvenskan",
            "USA": "https://sports.betway.de/de/sports/grp/soccer/usa/mls",
            "denmark_1": "https://betway.com/de/sports/grp/soccer/denmark/superligaen",
        },
        "bwin": {
            "germany_1": "https://sports.bwin.de/de/sports/fu%C3%9Fball-4/wetten/deutschland-17/bundesliga-102842",
            "germany_2": "https://sports.bwin.de/de/sports/fu%C3%9Fball-4/wetten/deutschland-17/2-bundesliga-102845",
            "germany_3": "https://sports.bwin.de/de/sports/fu%C3%9Fball-4/wetten/deutschland-17/3-liga-102377",
            "turkey_1": "https://sports.bwin.de/de/sports/fu%C3%9Fball-4/wetten/t%C3%BCrkei-31/s%C3%BCper-lig-102832",
            "spain_1": "https://sports.bwin.de/de/sports/fu%C3%9Fball-4/wetten/spanien-28/laliga-102829",
            "spain_2": "https://sports.bwin.de/de/sports/fu%C3%9Fball-4/wetten/spanien-28/laliga-2-102830",
            "england_1": "https://sports.bwin.de/de/sports/fu%C3%9Fball-4/wetten/england-14/premier-league-102841",
            "england_2": "https://sports.bwin.de/de/sports/fu%C3%9Fball-4/wetten/england-14/championship-102839",
            "france_1": "https://sports.bwin.de/de/sports/fu%C3%9Fball-4/wetten/frankreich-16/ligue-1-102843",
            "italy_1": "https://sports.bwin.de/de/sports/fu%C3%9Fball-4/wetten/italien-20/serie-a-102846",
            "netherlands_1": "https://sports.bwin.de/de/sports/fu%C3%9Fball-4/wetten/niederlande-36/eredivisie-102847",
            "belgium_1": "https://sports.bwin.de/de/sports/fu%C3%9Fball-4/wetten/belgien-35/pro-league-102836",
            "norway_1": "https://sports.bwin.de/de/sports/fu%C3%9Fball-4/wetten/norwegen-21/eliteserien-80",
            "sweden_1": "https://sports.bwin.de/de/sports/fu%C3%9Fball-4/wetten/schweden-29/allsvenskan-103",
            "USA": "https://sports.bwin.de/de/sports/fu%C3%9Fball-4/wetten/nordamerika-9/mls-33155",
            "denmark_1": "https://sports.bwin.de/de/sports/fu%C3%9Fball-4/wetten/d%C3%A4nemark-13/superligaen-102837",
        },
        "interwetten": {
            "germany_1": "https://www.interwetten.de/de/sportwetten/l/1019/deutschland-bundesliga",
            "germany_2": "https://www.interwetten.de/de/sportwetten/l/1020/deutschland-2-liga",
            "germany_3": "https://www.interwetten.de/de/sportwetten/l/405932/deutschland-3-liga",
            "turkey_1": "https://www.interwetten.de/de/sportwetten/l/1036/turkei-super-lig",
            "spain_1": "https://www.interwetten.de/de/sportwetten/l/1030/spanien-laliga",
            "spain_2": "https://www.interwetten.de/de/sportwetten/l/105034/spanien-laliga-2",
            "england_1": "https://www.interwetten.de/de/sportwetten/l/1021/england-premier-league",
            "england_2": "https://www.interwetten.de/de/sportwetten/l/1022/england-championship",
            "france_1": "https://www.interwetten.de/de/sportwetten/l/1024/frankreich-ligue-1",
            "italy_1": "https://www.interwetten.de/de/sportwetten/l/1029/italien-serie-a",
            "netherlands_1": "https://www.interwetten.de/de/sportwetten/l/1027/holland-ehrendivision",
            "belgium_1": "https://www.interwetten.de/de/sportwetten/l/1028/belgien-first-division-a",
            "norway_1": "https://www.interwetten.de/de/sportwetten/l/10251/norwegen-eliteserie",
            "sweden_1": "https://www.interwetten.de/de/sportwetten/l/10235/schweden-1-liga",
            "USA": "https://www.interwetten.de/de/sportwetten/l/10750/usa-major-league-soccer",
            "denmark_1": "https://www.interwetten.de/de/sportwetten/l/1035/danemark-superliga",
        },
        "unibet": {
            "germany_1": "https://www.unibet.de/betting/sports/filter/football/germany/bundesliga/all/matches",
            "germany_2": "https://www.unibet.de/betting/sports/filter/football/germany/2__bundesliga/all/matches",
            "germany_3": "https://www.unibet.de/betting/sports/filter/football/germany/3__liga/all/matches",
            "turkey_1": "https://www.unibet.de/betting/sports/filter/football/turkey/super_lig/all/matches",
            "spain_1": "https://www.unibet.de/betting/sports/filter/football/spain/la_liga/all/matches",
            "spain_2": "https://www.unibet.de/betting/sports/filter/football/spain/la_liga_2/all/matches",
            "england_1": "https://www.unibet.de/betting/sports/filter/football/england/premier_league/all/matches",
            "england_2": "https://www.unibet.de/betting/sports/filter/football/england/the_championship/all/matches",
            "france_1": "https://www.unibet.de/betting/sports/filter/football/france/ligue_1/all/matches",
            "italy_1": "https://www.unibet.de/betting/sports/filter/football/italy/serie_a/all/matches",
            "netherlands_1": "https://www.unibet.de/betting/sports/filter/football/netherlands/eredivisie/all/matches",
            "belgium_1": "https://www.unibet.de/betting/sports/filter/football/belgium/jupiler_pro_league/all/matches",
            "norway_1": "https://www.unibet.de/betting/sports/filter/football/norway/eliteserien/all/matches",
            "sweden_1": "https://www.unibet.de/betting/sports/filter/football/sweden/allsvenskan/all/matches",
            "USA": "https://www.unibet.de/betting/sports/filter/football/usa/mls/all/matches",
            "denmark_1": "https://www.unibet.de/betting/sports/filter/football/denmark/superligaen/all/matches",
        },
        "bet3000": {
            "germany_1": "https://www.bet3000.de/de/sports/top-leagues/1/Fu%C3%9Fball/30/Deutschland/87363584164/Bundesliga",
            "germany_2": "https://www.bet3000.de/de/sports/top-leagues/1/Fu%C3%9Fball/30/Deutschland/87363586390/2.%20Bundesliga",
            "germany_3": "https://www.bet3000.de/de/sports/top-leagues/1/Fu%C3%9Fball/30/Deutschland/87363654979/3.%20Liga",
            "turkey_1": "https://www.bet3000.de/de/sports/top-leagues/1/Fu%C3%9Fball/46/T%C3%BCrkei/87363587290/Super%20Lig",
            "spain_1": "https://www.bet3000.de/de/sports/1/Fussball/32/Spanien/87363573818/LaLiga",
            "spain_2": "https://www.bet3000.de/de/sports/1/Fussball/32/Spanien/87363587883/LaLiga%202",
            "england_1": "https://www.bet3000.de/de/sports/1/Fussball/1/England/87363576607/Premier%20League",
            "england_2": "https://www.bet3000.de/de/sports/1/Fussball/1/England/87363576899/Championship",
            "france_1": "https://www.bet3000.de/de/sports/1/Fussball/7/Frankreich/87363583874/Ligue%201",
            "italy_1": "https://www.bet3000.de/de/sports/1/Fussball/31/Italien/87363580650/Serie%20A",
            "netherlands_1": "https://www.bet3000.de/de/sports/1/Fussball/35/Niederlande/87363584614/Eredivisie",
            "belgium_1": "https://www.bet3000.de/de/sports/1/Fussball/33/Belgien/87363584878/First%20Division%20A",
            "norway_1": "#",
            "sweden_1": "#",
            "USA": "#",
            "denmark_1": "https://www.bet3000.de/de/sports/1/Fussball/8/D%C3%A4nemark/87363585144/Superligaen",
        },
        "xtip": {
            "germany_1": "https://www.merkur-sports.de/de/fussball/deutschland/bundesliga",
            "germany_2": "https://www.merkur-sports.de/de/fussball/deutschland/2-bundesliga",
            "germany_3": "https://www.merkur-sports.de/de/fussball/deutschland/3-liga",
            "turkey_1": "https://www.merkur-sports.de/de/fussball/turkei/super-lig",
            "spain_1": "https://www.merkur-sports.de/de/fussball/spanien/la-liga",
            "spain_2": "https://www.merkur-sports.de/de/fussball/spanien/la-liga-2",
            "england_1": "https://www.merkur-sports.de/de/fussball/england/premier-league",
            "england_2": "https://www.merkur-sports.de/de/fussball/england/championship",
            "france_1": "https://www.merkur-sports.de/de/fussball/frankreich/ligue-1",
            "italy_1": "https://www.merkur-sports.de/de/fussball/italien/serie-a",
            "netherlands_1": "https://www.merkur-sports.de/de/fussball/niederlande/eredivisie",
            "belgium_1": "https://www.merkur-sports.de/de/fussball/belgien/pro-league",
            "norway_1": "#",
            "sweden_1": "#",
            "USA": "#",
            "denmark_1": "https://www.merkur-sports.de/de/fussball/danemark/superligaen",
        },
        "comeon": {
            "germany_1": "https://www.comeonwetten.de/de/sportsbook/sport/fussball/deutschland/bundesliga",
            "germany_2": "https://www.comeonwetten.de/de/sportsbook/sport/fussball/deutschland/2-bundesliga",
            "germany_3": "https://www.comeonwetten.de/de/sportsbook/sport/fussball/deutschland/3-liga",
            "turkey_1": "https://www.comeonwetten.de/de/sportsbook/sport/fussball/turkei/super-lig",
            "spain_1": "https://www.comeonwetten.de/de/sportsbook/sport/fussball/spanien/la-liga",
            "spain_2": "https://www.comeonwetten.de/de/sportsbook/sport/fussball/spanien/segunda",
            "england_1": "https://www.comeonwetten.de/de/sportsbook/sport/fussball/england/premier-league",
            "england_2": "https://www.comeonwetten.de/de/sportsbook/sport/fussball/england/championship",
            "france_1": "https://www.comeonwetten.de/de/sportsbook/sport/fussball/frankreich/ligue-1",
            "italy_1": "https://www.comeonwetten.de/de/sportsbook/sport/fussball/italien/serie-a",
            "netherlands_1": "https://www.comeonwetten.de/de/sportsbook/sport/fussball/niederlande/eredivisie",
            "belgium_1": "https://www.comeonwetten.de/de/sportsbook/sport/fussball/belgien/jupiler-league",
            "norway_1": "#",
            "sweden_1": "#",
            "USA": "#",
        },
        "sunmaker": {
            "germany_1": "https://www.sunmaker.de/de/sports",
            "germany_2": "https://www.sunmaker.de/de/sports",
            "germany_3": "https://www.sunmaker.de/de/sports",
            "turkey_1": "https://www.sunmaker.de/de/sports",
            "spain_1": "https://www.sunmaker.de/de/sports",
            "spain_2": "https://sbtech.sunmaker.de/de/sports/fu%C3%9Fball/spanien-segunda/",
            "england_1": "https://www.sunmaker.de/de/sports",
            "england_2": "https://www.sunmaker.de/de/sports",
            "france_1": "https://www.sunmaker.de/de/sports",
            "italy_1": "https://www.sunmaker.de/de/sports",
            "netherlands_1": "https://www.sunmaker.de/de/sports",
            "belgium_1": "https://www.sunmaker.de/de/sports",
            "norway_1": "https://sbtech.sunmaker.de/de/sports/fu%C3%9Fball/norwegen-elitserien/",
            "sweden_1": "https://sbtech.sunmaker.de/de/sports/fu%C3%9Fball/schweden-allsvenskan/",
            "USA": "https://sbtech.sunmaker.de/de/sports/fu%C3%9Fball/usa-mls/",
            "champions_league": "https://sbtech.sunmaker.de/de/sports/fu%C3%9Fball/champions-league/",
            "europa_league": "https://sbtech.sunmaker.de/de/sports/fu%C3%9Fball/europa-league/",
            "euro_2020": "https://sbtech.sunmaker.de/de/sports/fu%C3%9Fball/euro-2020/"
        },
    }

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

                # Extract league data
                league = match["league"]
                bookie_name = final_bet_advice["bookie"]

                # Create relevant bet
                relevant_bet = {
                    "match_id": match["match_id"],
                    "league": league,
                    "league_string": league_names[league],
                    "league_url": league_urls[bookie_name][league],
                    "date": match["date"],
                    "home_team": match["home_team"],
                    "away_team": match["away_team"],
                    "bet": final_bet_advice["bet_type"],
                    "bet_string": bet_string,
                    "odd": final_bet_advice["odd"],
                    "stake": final_bet_advice["stake"],
                    "bookie": bookie_name,
                }

                # Add relevant bet to relevant_user_bets list
                relevant_user_bets.append(relevant_bet)

    # Sort relevant user bets for date
    relevant_user_bets.sort(
        key=lambda match_: datetime.strptime(match_["date"], "%d.%m.%Y"))

    return relevant_user_bets


def get_all_finished_bets():
    # Create list for ALL bet results
    bet_results = []
    with open("bet_results.csv", "r", encoding="utf-8") as file:

        # loop through each line in valuebets file
        for line in file:
            # strip() lines
            stripped_line = line.strip()

            # Create dict for each match
            match = {
                "league": stripped_line.split(",")[0],
                "date": stripped_line.split(",")[1],
                "home_team": stripped_line.split(",")[2],
                "away_team": stripped_line.split(",")[3],
                "home_goals": stripped_line.split(",")[9].split("-")[0],
                "away_goals": stripped_line.split(",")[9].split("-")[1],
            }

            bet_results.append(match)

    return bet_results


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


def paginate_bets(request, bets_query_set, results_per_page):

    page = request.GET.get("page")
    paginator = Paginator(object_list=bets_query_set,
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
