from decimal import Decimal
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q, Sum
from .models import myCards
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.
def login_view(request):
    message = False
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            message = True
    return render(request, "login.html", {"message": message})


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
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
            return render(request, "index.html", {"message": "کارتەکە دروست کرا"})
        except:
            return render(request, "index.html", {"message": "No Valid Records!"})
    return render(request, "index.html", {"message": ""})


@login_required
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


@login_required
def transferd(request, name):
    if request.method == "POST":
        list = myCards.objects.filter(
            Q(users_id=request.user.id) & Q(owner_name=name) & Q(accepted=True)
        )
        paid = Decimal(request.POST.get("paid"))

        for item in list:
            paid2 = item.amounts * paid / 100
            item.transfered = True
            item.amounts = item.amounts - (item.amounts * paid / 100)
            item.paidtwo = paid2
            item.save()
        return render(
            request, "success.html", {"message": "Well Done!", "success": True}
        )
        # except:
        #     return render(
        #         request, "failed.html", {"message": "Bad Input!", "success": True}
        #     )
    return redirect("transfer")


@login_required
def transfer(request):
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


@login_required
def accepted(request, pk):
    if request.method == "POST":
        list = myCards.objects.get(Q(users_id=request.user.id) & Q(id=pk))
        comision = Decimal(request.POST.get("comision"))
        paid = Decimal(request.POST.get("paid"))
        comision2 = list.amounts * comision / 100
        paid2 = list.amounts * paid / 100
        try:
            list.amounts = calc(list.amounts, comision, paid)
            list.comision = comision2
            list.paid = paid2
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


@login_required
def report(request):
    list = (
        myCards.objects.filter(
            Q(users=request.user.id) & Q(accepted=True) & Q(transfered=True)
        )
        .values("owner_name", "paid", "paidtwo", "comision", "updated_at")
        .order_by("owner_name")
        .annotate(total_price=Sum("amounts"))
    )
    sumTotal = 0
    sumCom = 0
    sum3m = 0
    sumNa = 0
    for item in list:
        sumTotal += item["total_price"]
        sumCom += item["comision"]
        sum3m += item["paid"]
        sumNa += item["paidtwo"]
    list = [{"id": idx + 1, **item} for idx, item in enumerate(list)]
    context = {
        "list": list,
        "sumTotal": sumTotal,
        "sumCom": sumCom,
        "sum3m": sum3m,
        "sumNa": sumNa,
    }
    return render(request, "report.html", context)


@login_required
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


@login_required
def delete_card(request, pk):
    if request.method == "POST":
        id = pk
        if id:
            card = get_object_or_404(myCards, id=id, users=request.user)
        else:
            return HttpResponse("No id or name provided", status=400)
        card.delete()
        return redirect("index")  # Redirect to the index page after deletion

    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


# use percentage
def calc(amount, comision, paid):
    amount = amount - (amount * comision / 100)
    amount = amount - (amount * paid / 100)
    return amount
