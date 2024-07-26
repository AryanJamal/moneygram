from decimal import Decimal
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.models import Q, Sum
from .models import myCards


# Create your views here.
def index(request):
    if request.method == "POST":
        user = request.user.id
        owner_name = request.POST.get("owner_name")
        person_name = request.POST.get("person_name")
        description = request.POST.get("description")
        amounts = request.POST.get("amounts")
        code = request.POST.get("code")
        try:
            myCards.objects.get_or_create(
                users_id=user,
                owner_name=owner_name,
                person_name=person_name,
                description=description,
                code=code,
                amounts=amounts,
            )
            return render(request, "index.html", {"message": "Created Card!"})
        except:
            return render(request, "index.html", {"message": "No Valid Records!"})
    return render(request, "index.html", {"message": ""})


def cards(request):
    list = myCards.objects.filter(Q(users_id=request.user.id) & Q(accepted=False))
    if list:
        sum = 0
        for item in list:
            sum += item.amounts
        context = {"list": list, "sum": sum}
    else:
        context = {"list": list}
    return render(request, "cards.html", context)


def transferd(request, name):
    if request.method == "POST":
        list = myCards.objects.filter(
            Q(users_id=request.user.id) & Q(owner_name=name) & Q(accepted=True)
        )
        paid = Decimal(request.POST.get("paid"))
        for item in list:
            item.transfered = True
            item.amounts = item.amounts - (item.amounts * paid / 100)
            item.save()
        return render(
            request, "success.html", {"message": "Well Done!", "success": True}
        )
        # except:
        #     return render(
        #         request, "failed.html", {"message": "Bad Input!", "success": True}
        #     )
    return redirect("transfer")


def transfer(request):
    # list = (
    #     myCards.objects.values("owner_name")
    #     .order_by("owner_name")
    #     .annotate(total_price=Sum("amounts"))
    # )
    list = (
        myCards.objects.filter(
            Q(users=request.user.id) & Q(accepted=True) & Q(transfered=False)
        )
        .values("owner_name")
        .order_by("owner_name")
        .annotate(total_price=Sum("amounts"))
    )
    list = [{"id": idx + 1, **item} for idx, item in enumerate(list)]
    context = {"list": list}
    return render(request, "transfered.html", context)


def accepted(request, pk):
    if request.method == "POST":
        list = myCards.objects.get(Q(users_id=request.user.id) & Q(id=pk))
        comision = Decimal(request.POST.get("comision"))
        paid = Decimal(request.POST.get("paid"))
        try:
            list.amounts = calc(list.amounts, comision, paid)
            list.comision = request.POST.get("comision")
            list.paid = request.POST.get("paid")
            list.accepted = True
            list.save()
            return render(
                request,
                "updated.html",
                {"message": "Record Accepted!", "success": True},
            )
        except:
            return render(
                request, "updated.html", {"message": "Bad Input!", "success": True}
            )
    return redirect("cards")


def report(request):
    list = (
        myCards.objects.filter(
            Q(users=request.user.id) & Q(accepted=True) & Q(transfered=True)
        )
        .values("owner_name")
        .order_by("owner_name")
        .annotate(total_price=Sum("amounts"))
    )
    list = [{"id": idx + 1, **item} for idx, item in enumerate(list)]
    context = {"list": list}
    return render(request, "report.html", context)


def earned(request):
    list = myCards.objects.filter(
        Q(users_id=request.user.id) & Q(accepted=True) & Q(transfered=False)
    )
    if list:
        sum = 0
        for item in list:
            sum += item.amounts
        context = {"list": list, "sum": sum}
    else:
        context = {"list": list}
    return render(request, "earned.html", context)


# use percentage
def calc(amount, comision, paid):
    amount = amount - (amount * comision / 100)
    amount = amount - (amount * paid / 100)
    return amount
