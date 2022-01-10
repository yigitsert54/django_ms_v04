
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from .models import Account


# Create account when user is created
def create_account(sender, instance, created, **kwargs):
    # sender = The Model that triggers the action
    # instance = the instance of the model (e.g. instance="Yigit Sert" from model="Account")
    # created = True or False (new Instance was created or just saved/modified/changed)

    # Get User instance
    user = instance

    if created:  # If new User is created

        # Create Account
        account = Account.objects.create(
            user=user,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email
        )


# Update user when account is updated
def update_account(sender, instance, created, **kwargs):
    account = instance
    user = account.user

    if created == False:
        user.first_name = account.first_name
        user.last_name = account.last_name
        user.email = account.email
        user.username = account.email
        user.save()


# Delete User when Account is deleted
def delete_user(sender, instance, **kwargs):

    # instance = Account (We want to get account.user)
    user = instance.user
    user.delete()


# if new user is created, create connected account
post_save.connect(create_account, sender=User)


# if account is modified/updated, update user
post_save.connect(update_account, sender=Account)

# if account is deleted, delete user
post_delete.connect(delete_user, sender=Account)
