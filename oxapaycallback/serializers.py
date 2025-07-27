from rest_framework import serializers


class OxaPayCallbackSerializer(serializers.Serializer):
    # Common fields for all statuses
    status = serializers.CharField()  # Waiting, Confirming, Paid, Expired
    trackId = serializers.CharField()
    amount = serializers.CharField()  # String because it can be decimal
    currency = serializers.CharField()
    feePaidByPayer = serializers.IntegerField()
    underPaidCover = serializers.IntegerField()
    email = serializers.CharField(allow_blank=True)
    orderId = serializers.CharField(allow_blank=True)
    description = serializers.CharField(allow_blank=True)
    date = serializers.CharField()  # Unix timestamp
    payDate = serializers.CharField()  # Unix timestamp, can be 0
    type = serializers.CharField()  # Always "payment"

    # Fields for Confirming and Paid status
    address = serializers.CharField(required=False, allow_blank=True)
    senderAddress = serializers.CharField(required=False, allow_blank=True)
    txID = serializers.CharField(required=False, allow_blank=True)
    price = serializers.CharField(required=False, allow_blank=True)
    payAmount = serializers.CharField(required=False, allow_blank=True)
    payCurrency = serializers.CharField(required=False, allow_blank=True)
    network = serializers.CharField(required=False, allow_blank=True)
