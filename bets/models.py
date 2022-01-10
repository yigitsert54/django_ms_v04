from decimal import Decimal
from django.db import models
import uuid
from accounts.models import Account, Bookie
from datetime import datetime

# null=True means, it is not required
# blank=True is for the form, it means we are allowed to submit a form with this field empty


class Match(models.Model):
    league = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True)
    home_team = models.CharField(max_length=100, null=True, blank=True)
    away_team = models.CharField(max_length=100, null=True, blank=True)
    oddspedia_match_id = models.CharField(max_length=15, null=True, blank=True)
    home_goals = models.IntegerField(null=True, blank=True)
    away_goals = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=30, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        formatted_date = datetime.strftime(self.date, "%d.%m.%Y")
        name = f"{self.home_team} - {self.away_team} ({formatted_date})"
        return name

    class Meta:
        verbose_name_plural = "Matches"
        unique_together = [["league", "date", "home_team", "away_team"]]
        ordering = ["-date", "league"]

    # get league_name
    @property
    def league_name(self):

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

        return league_names[self.league]


class Bet(models.Model):

    # ForeignKey: Match (in Klammern) can have many bets (class)
    # But each bet (class) is connected to one Match (in Klammern)
    match = models.ForeignKey(
        Match, null=True, blank=True, on_delete=models.CASCADE)

    owner = models.ForeignKey(
        Account, null=True, blank=True, on_delete=models.CASCADE)

    bookie = models.ForeignKey(
        Bookie, null=True, blank=True, on_delete=models.CASCADE)

    bet_type = models.CharField(max_length=50, null=True, blank=True)

    odd = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True)

    stake = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)

    result = models.CharField(max_length=10, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)

    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        name = f"{self.match} - ({self.owner})"
        return name

    class Meta:
        ordering = ["match"]

    def update_result(self):
        # Check if match has ended
        if self.match.status == "ended":

            # Create list for winning bets
            winning_bets = []

            # Check all outcome possibilities
            if self.match.home_goals > self.match.away_goals:  # home_win
                winning_bets.append("home")
                winning_bets.append("DC_1X")
                winning_bets.append("DC_12")

            elif self.match.home_goals < self.match.away_goals:  # away_win
                winning_bets.append("away")
                winning_bets.append("DC_X2")
                winning_bets.append("DC_12")

            else:  # draw
                winning_bets.append("draw")
                winning_bets.append("DC_1X")
                winning_bets.append("DC_X2")

            # Check if bet was right
            if self.bet_type in winning_bets:
                self.result = "won"
            else:
                self.result = "lost"

            self.save()

        # get league_name

    @property
    def result_string(self):

        if self.match.status == "ended":
            if self.result == "won":
                return "gewonnen"
            else:
                return "verloren"
        else:
            return "offen"

    @property
    def win_amount(self):

        amount = -1 * self.stake

        if self.match.status == "ended":

            if self.result == "won":

                if self.bookie.tax:
                    factor = Decimal(0.95)
                else:
                    factor = Decimal(1)

                amount += self.stake * self.odd * factor

            return abs(round(amount, 2))

        else:
            return "-"

    @property
    def bet_string(self):
        if self.bet_type == "home":
            return self.match.home_team + "(1)"
        elif self.bet_type == "away":
            return self.match.away_team + "(2)"
        elif self.bet_type == "draw":
            return "Unentschieden(X)"
        else:
            return self.bet_type
