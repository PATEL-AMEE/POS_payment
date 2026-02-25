import random, uuid, time
from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction
from django.utils import timezone
from django.views.decorators.http import require_http_methods

def home(request):
    return render(request, "payments/home.html")


@require_http_methods(["GET", "POST"])
def new_sale(request):
    if request.method == "POST":
        request.session["amount"] = request.POST.get("amount")
        return redirect("choose_method")
    return render(request, "payments/new_sale.html")


@require_http_methods(["GET", "POST"])
def choose_method(request):
    amount = request.session.get("amount")
    if not amount:
        return redirect("new_sale")

    if request.method == "POST":
        method = request.POST.get("method")
        if method == "card":
            return redirect("card_payment")
        if method == "qr":
            request.session["qr_expiry"] = time.time() + 30
            return redirect("qr_payment")

    return render(request, "payments/method.html", {"amount": amount})


@require_http_methods(["GET", "POST"])
def card_payment(request):
    amount = request.session.get("amount")
    if not amount:
        return redirect("new_sale")

    if request.method == "POST":
        scenario = request.POST.get("scenario", "random") 
        tx = Transaction.objects.create(
            amount=amount,
            method="card",
            status="pending",
            reference=str(uuid.uuid4())[:8].upper(),
        )
        request.session["scenario"] = scenario
        return redirect("processing", tx_id=tx.id)

    return render(request, "payments/card.html", {"amount": amount})


@require_http_methods(["GET", "POST"])
def qr_payment(request):
    amount = request.session.get("amount")
    if not amount:
        return redirect("new_sale")

    expiry = request.session.get("qr_expiry", time.time())
    seconds_left = int(expiry - time.time())

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "regenerate":
            request.session["qr_expiry"] = time.time() + 30
            return redirect("qr_payment")

        tx = Transaction.objects.create(
            amount=amount,
            method="qr",
            status="pending",
            reference=str(uuid.uuid4())[:8].upper(),
        )
        request.session["qr_expired"] = seconds_left <= 0
        return redirect("processing", tx_id=tx.id)

    return render(
        request,
        "payments/qr.html",
        {"amount": amount, "seconds_left": max(seconds_left, 0), "expired": seconds_left <= 0},
    )


def processing(request, tx_id):
    tx = get_object_or_404(Transaction, id=tx_id)
    return render(request, "payments/processing.html", {"tx": tx})


def result(request, tx_id):
    tx = get_object_or_404(Transaction, id=tx_id)

    if tx.status != "pending":
        return redirect("transactions")

    if tx.method == "card":
        scenario = request.session.get("scenario", "random")
        if scenario in ["success", "declined", "offline"]:
            tx.status = scenario
        else:
            tx.status = random.choices(["success", "declined", "offline"], [0.8, 0.15, 0.05])[0]
        request.session.pop("scenario", None)

    else:
        expired = request.session.get("qr_expired", False)
        if expired:
            tx.status = "expired"
        else:
            tx.status = random.choices(["success", "offline", "failed"], [0.85, 0.1, 0.05])[0]
        request.session.pop("qr_expired", None)

    tx.save()

    if tx.status == "success":
        return render(request, "payments/success.html", {"tx": tx})

    return render(request, "payments/error.html", {"tx": tx})


def transactions(request):
    txs = Transaction.objects.order_by("-created_at")
    return render(request, "payments/transactions.html", {"transactions": txs})


def transaction_detail(request, tx_id):
    tx = get_object_or_404(Transaction, id=tx_id)
    return render(request, "payments/transaction_detail.html", {"tx": tx})

# Refund 

@require_http_methods(["POST"])
def refund_start(request, tx_id):
    tx = get_object_or_404(Transaction, id=tx_id)

    if tx.status != "success":
        return render(request, "payments/refund_error.html", {"tx": tx})

    return redirect("refund_processing", tx_id=tx.id)


def refund_processing(request, tx_id):
    tx = get_object_or_404(Transaction, id=tx_id)

    if tx.status != "success":
        return render(request, "payments/refund_error.html", {"tx": tx})

    tx.status = "refunded"
    tx.refunded_at = timezone.now()
    tx.refund_reference = ("RF" + uuid.uuid4().hex[:8]).upper()
    tx.save()

    return render(request, "payments/refund_success.html", {"tx": tx})