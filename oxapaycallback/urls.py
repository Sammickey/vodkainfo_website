from django.urls import path
from .views import OxaPayCallbackView, deposit

urlpatterns = [
    path('oxapay/deposit/', deposit, name='oxapay_deposit'),
    path('oxapaycallback/oxapay/callback/', OxaPayCallbackView.as_view(), name='oxapay_callback'),
]
