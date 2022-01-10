from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
import uuid


# Each Model is a table in the database
# null=True means, it is not required
# blank=True ist for the form, it means we are allowed to submit a form with this field empty


class Account(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=300, null=True, blank=True)
    order_id = models.CharField(max_length=50, null=True, blank=True)
    notifications = models.BooleanField(blank=True, default=False)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        account_name = f"{self.first_name} {self.last_name}"
        return str(account_name)

    class Meta:
        ordering = ["first_name"]

    # Calculate total balance of Account
    @property
    def total_balance(self):

        all_bookies = self.bookie_set.all()
        total_balance = Decimal(0)

        for bookie in all_bookies:
            total_balance += bookie.balance

        return total_balance

    @property
    def has_unseen_answers(self):

        support = self.support_set.filter(answered=True, seen=False)

        if len(support) > 0:
            has_unseen = True
        else:
            has_unseen = False

        return has_unseen


class Bookie(models.Model):
    BOOKIE_NAMES = (
        (None, "Wettanbieter auswählen"),
        ("bet-at-home", "Bet-At-Home"),
        ("bet365", "Bet365"),
        ("betway", "Betway"),
        ("bwin", "Bwin"),
        ("interwetten", "Interwetten"),
        ("unibet", "Unibet"),
        ("comeon", "ComeOn"),
        ("sunmaker", "Sunmaker"),
        ("bet3000", "Bet3000"),
        ("tipico", "Tipico"),
        ("xtip", "X-Tip"),
        ("bildbet", "BildBet"),
    )

    owner = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, null=True,
                            blank=True, choices=BOOKIE_NAMES)
    invested_stake = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    withdrawed_stake = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    tax = models.BooleanField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        bookie_name = f"{self.name.capitalize()} ({self.owner.first_name} {self.owner.last_name})"
        return str(bookie_name)

    class Meta:
        ordering = ["owner", "name"]

    # Calculate Balance
    @property
    def balance(self):
        # first calculation for credits from invested & withdrawed stake
        bet_credits = self.invested_stake - self.withdrawed_stake

        # get all bets for that bookie
        bets = self.bet_set.all()

        # Get factor for tax
        if self.tax:
            factor = Decimal(0.95)
        else:
            factor = Decimal(1)

        # Loop through all bets of that bookie
        for bet in bets:
            # substract bet stake from bookie balance
            bet_credits -= bet.stake

            if bet.result == "won":
                # if bet is won add win amount to bookie balance
                bet_credits += round(bet.odd * bet.stake * factor, 2)

        return round(bet_credits, 2)

    @property
    def finished_bets(self):

        finished_bets = self.bet_set.all().exclude(result="open")

        return finished_bets
