
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import OxaPayCallbackSerializer
from rest_framework.request import Request
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .utils import make_qr_code, create_oxapay_static_address, get_or_update_invoice
from .forms import PaymentInitiateForm


@method_decorator(csrf_exempt, name='dispatch')
class OxaPayCallbackView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request: Request):
        # Check if the request is coming from an allowed IP
        client_ip = self.get_client_ip(request)
        allowed_ips = ['162.0.217.89', '185.224.137.171']

        if client_ip not in allowed_ips:
            return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        # Grab incoming JSON data
        post_data = request.data

        try:
            # Validate the data
            serializer = OxaPayCallbackSerializer(data=post_data)
            if serializer.is_valid():
                data = serializer.validated_data

                status_type = data['status']
                track_id = data['trackId']
                # Might be missing in some statuses
                address = data.get('address')

                if status_type == 'Waiting':
                    return Response({'status': 'waiting_for_payment'},
                                    status=status.HTTP_200_OK)

                elif status_type == 'Confirming':
                    return Response({'status': 'payment_confirming'},
                                    status=status.HTTP_200_OK)

                elif status_type == 'Paid':
                    try:
                        amount = round(float(data['price']), 2)
                        currency = data['currency']
                        user = get_or_update_invoice(address, amount)
                        if user:
                            return Response({
                                'status': 'payment_successful',
                                'amount': amount,
                                'currency': currency
                            }, status=status.HTTP_200_OK)
                        else:
                            return Response({'error': 'Invoice not found'},
                                            status=status.HTTP_404_NOT_FOUND)
                    except Exception as e:
                        return Response({
                            'error': 'Failed to process payment',
                            'details': str(e)
                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                elif status_type == 'Expired':
                    return Response({'status': 'payment_expired'},
                                    status=status.HTTP_200_OK)

                elif status_type == 'Complete' and data.get('type') == 'payout':
                    return Response({'status': 'payout_completed'},
                                    status=status.HTTP_200_OK)

                else:
                    return Response({
                        'error': 'Unknown status',
                        'status': status_type
                    }, status=status.HTTP_400_BAD_REQUEST)

            # If serializer is invalid:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'error': 'Internal server error',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@login_required
def deposit(request) -> HttpResponse:
    """
    GET  → show currency-picker form
    POST → create static address, make QR, show both
    """
    import base64

    if request.method == "POST":
        form = PaymentInitiateForm(request.POST)
        if form.is_valid():
            currency = form.cleaned_data["currency"]
            invoice = create_oxapay_static_address(currency, request.user)
            if not invoice:
                return render(request, "dashboard/deposit.html", {
                    "form": form,
                    "error": "Could not create invoice. Try again. (might be invalid oxapay api key)"
                })
            qr_bytes = make_qr_code(invoice.btc_address)
            qr_b64 = base64.b64encode(qr_bytes.getvalue()).decode()
            return render(
                request,
                "dashboard/deposit.html",
                {
                    "address": invoice.btc_address,
                    "currency": invoice.currency,
                    "qr_b64": qr_b64,
                    "form": form,
                },
            )
        else:
            return render(request, "dashboard/deposit.html", {"form": form})

    # GET
    form = PaymentInitiateForm()
    return render(request, "dashboard/deposit.html", {"form": form})
