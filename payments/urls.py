from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("new-sale/", views.new_sale, name="new_sale"),
    path("method/", views.choose_method, name="choose_method"),
    path("card/", views.card_payment, name="card_payment"),
    path("qr/", views.qr_payment, name="qr_payment"),
    path("processing/<int:tx_id>/", views.processing, name="processing"),
    path("result/<int:tx_id>/", views.result, name="result"),
    path("transactions/", views.transactions, name="transactions"),
    path("transactions/<int:tx_id>/", views.transaction_detail, name="transaction_detail"),
    path("refund/<int:tx_id>/", views.refund_start, name="refund_start"),
    path("refund/<int:tx_id>/processing/", views.refund_processing, name="refund_processing"),
]