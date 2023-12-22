from django.shortcuts import render, redirect
from ..models import BankAccount
from social.models import Message
from world.models import DailyClaim
from core.models import Avatar
from datetime import datetime
from utils.error import error_page


def compound_interest(principal, rate, times_per_year, years):
    # (1 + r/n)
    body = 1 + (rate / times_per_year)
    # nt
    exponent = times_per_year * years
    # P(1 + r/n)^nt
    return principal * pow(body, exponent)


def bank_page(request):
    if request.user.is_authenticated():
        today = datetime.today()
        bank_account = BankAccount.objects.filter(user=request.user).first()
        interest = DailyClaim.objects.filter(
            user=request.user,
            daily_type="interest",
            date_of_claim__year=today.year,
            date_of_claim__month=today.month,
            date_of_claim__day=today.day,
        ).first()

        if bank_account != None:
            if bank_account.level == 1:
                rate = 0.1
            elif bank_account.level == 2:
                rate = 0.13
            elif bank_account.level == 3:
                rate = 0.15
            elif bank_account.level == 4:
                rate = 0.16
            else:
                rate = 0.17
            interest_amount = compound_interest(bank_account.balance, rate, 365, 1)
            interest_amount = int((interest_amount - bank_account.balance) / 365)
        else:
            interest_amount = 0
        return render(
            request,
            "shop/bank_page.html",
            {
                "bank_account": bank_account,
                "interest": interest,
                "interest_amount": interest_amount,
            },
        )
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def open_bank_account_page(request):
    if request.user.is_authenticated():
        check_for_bank_account = BankAccount.objects.filter(user=request.user).count()
        if check_for_bank_account == 0:
            error = request.session.pop("error", False)
            return render(request, "shop/open_bank_account_page.html", {"error": error})
        else:
            request.session["error"] = "Your account has already been opened."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def open_bank_account(request):
    if request.user.is_authenticated():
        check_for_bank_account = BankAccount.objects.filter(user=request.user).count()
        if check_for_bank_account == 0:
            level = int(request.POST.get("level"))

            deposit = request.POST.get("deposit")
            if deposit:
                try:
                    deposit = int(deposit)
                except:
                    request.session["error"] = "Your deposit must be an integer."
                    return redirect(open_bank_account_page)
                if deposit >= 100:
                    if level == 2 and deposit < 10000:
                        request.session[
                            "error"
                        ] = "To be a Bronze account, your deposit must be at least 10,000 points."
                        return redirect(open_bank_account_page)
                    elif level == 3 and deposit < 100000:
                        request.session[
                            "error"
                        ] = "To be a Silver account, your deposit must be at least 100,000 points."
                        return redirect(open_bank_account_page)
                    elif level == 4 and deposit < 1000000:
                        request.session[
                            "error"
                        ] = "To be a Gold account, your deposit must be at least 1,000,000 points."
                        return redirect(open_bank_account_page)
                    elif level == 5 and deposit < 10000000:
                        request.session[
                            "error"
                        ] = "To be a Platinum account, your deposit must be at least 10,000,000 points."
                        return redirect(open_bank_account_page)

                    if request.user.profile.points >= deposit:
                        bank = BankAccount.objects.create(
                            user=request.user, balance=deposit, level=level
                        )
                        request.user.profile.points -= deposit
                        request.user.profile.save()
                        return redirect(bank_page)
                    else:
                        request.session[
                            "error"
                        ] = "You must have enough points to cover your deposit."
                        return redirect(open_bank_account_page)
                else:
                    request.session[
                        "error"
                    ] = "Your deposit must be at least 100 points."
                    return redirect(open_bank_account_page)
            else:
                request.session["error"] = "Please enter a deposit amount."
                return redirect(open_bank_account_page)
        else:
            request.session["error"] = "Your account has already been opened."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def deposit(request):
    if request.user.is_authenticated():
        bank_account = BankAccount.objects.filter(user=request.user).first()
        if bank_account:
            deposit = request.POST.get("amount")
            if deposit:
                try:
                    deposit = int(deposit)
                except:
                    request.session["error"] = "Your deposit must be an integer."
                    return redirect(error_page)
                if request.user.profile.points >= deposit:
                    request.user.profile.points -= deposit
                    request.user.profile.save()
                    bank_account.balance += deposit
                    bank_account.save()

                    # AVATARS
                    riches_avatar = Avatar.objects.get(url="riches")
                    if riches_avatar not in request.user.profile.avatars.all():
                        if bank_account.balance >= 1000000:
                            request.user.profile.avatars.add(riches_avatar)
                            request.user.profile.save()
                            message = Message.objects.create(
                                receiving_user=request.user,
                                subject="You just found a secret avatar!",
                                text='You have just received the avatar "Riches!" to use on the boards!',
                            )
                    return redirect(bank_page)
                else:
                    request.session[
                        "error"
                    ] = "You do not have enough points to make that deposit."
                    return redirect(error_page)
            else:
                request.session["error"] = "Please enter a deposit amount."
                return redirect(error_page)
        else:
            request.session[
                "error"
            ] = "You may not deposit if you do not have a bank account."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def withdraw(request):
    if request.user.is_authenticated():
        bank_account = BankAccount.objects.filter(user=request.user).first()
        if bank_account:
            withdraw = request.POST.get("amount")
            if withdraw:
                try:
                    withdraw = int(withdraw)
                except:
                    request.session[
                        "error"
                    ] = "Your withdraw amount must be an integer."
                    return redirect(error_page)
                if bank_account.balance >= withdraw:
                    request.user.profile.points += withdraw
                    request.user.profile.save()
                    bank_account.balance -= withdraw
                    bank_account.save()
                    return redirect(bank_page)
                else:
                    request.session[
                        "error"
                    ] = "You do not have enough points in your bank to make that withdraw."
                    return redirect(error_page)
            else:
                request.session["error"] = "Please enter a withdraw amount."
                return redirect(error_page)
        else:
            request.session[
                "error"
            ] = "You may not withdraw if you do not have a bank account."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def collect_interest(request):
    if request.user.is_authenticated():
        bank_account = BankAccount.objects.filter(user=request.user).first()
        if bank_account:
            today = datetime.today()
            # interest = Interest.objects.filter(user=request.user).first()
            if bank_account.level == 1:
                rate = 0.1
            elif bank_account.level == 2:
                rate = 0.13
            elif bank_account.level == 3:
                rate = 0.15
            elif bank_account.level == 4:
                rate = 0.16
            else:
                rate = 0.17
            interest_amount = compound_interest(bank_account.balance, rate, 365, 1)
            interest_amount = int((interest_amount - bank_account.balance) / 365)
            interest = DailyClaim.objects.filter(
                user=request.user,
                daily_type="interest",
                date_of_claim__year=today.year,
                date_of_claim__month=today.month,
                date_of_claim__day=today.day,
            ).first()
            if not interest:
                bank_account.balance += interest_amount
                bank_account.save()
                interest = DailyClaim.objects.create(
                    user=request.user,
                    message="You have already collected your interest today.",
                    daily_type="interest",
                    points=interest_amount,
                )
                return redirect(bank_page)
            else:
                request.session[
                    "error"
                ] = "You have already collected your interest today."
                return redirect(error_page)
        else:
            request.session[
                "error"
            ] = "You may not collect interest if you do not have a bank account."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def upgrade_bank_account(request):
    if request.user.is_authenticated():
        bank_account = BankAccount.objects.filter(user=request.user).first()
        if bank_account:
            can_upgrade = False
            if bank_account.level == 1 and bank_account.balance >= 10000:
                can_upgrade = True
            elif bank_account.level == 2 and bank_account.balance >= 100000:
                can_upgrade = True
            elif bank_account.level == 3 and bank_account.balance >= 1000000:
                can_upgrade = True
            elif bank_account.level == 4 and bank_account.balance >= 10000000:
                can_upgrade = True

            if can_upgrade:
                bank_account.level += 1
                bank_account.save()
                return redirect(bank_page)
            else:
                request.session[
                    "error"
                ] = "You are not eligible to upgrade your bank account at this time."
                return redirect(error_page)
        else:
            request.session[
                "error"
            ] = "You may not upgrade if you do not have a bank account."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)
