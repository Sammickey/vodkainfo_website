from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.contrib.auth import get_user_model

User = get_user_model()


class Price(models.Model):
    """Model for storing pricing plans"""
    Mickey_SSN_DOB_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('99999999'))
    Mickey_SSN_DOB_New_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('99999999'))
    Mickey_DL_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('99999999'))
    Sam_SSN_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('99999999'))
    Sam_SSN_DOB_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('99999999'))
    Sam_DLV2_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('99999999'))
    Sam_Advanced_Lookup_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('99999999'))
    Sam_DOB_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('99999999'))
    Sam_Phone_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('99999999'))
    Sam_Reverse_Phone_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('99999999'))
    Sam_Reverse_SSN_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('99999999'))
    Sergio_SSN_DOB_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('99999999'))
    Sergio_DL_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('99999999'))
    Alex_SSN_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('99999999'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class StatusChoices(models.TextChoices):
    CREATED = 'created', 'Created'
    PROCESSING = 'processing', 'Processing'
    SUCCESS = 'success', 'Success'
    FAILED = 'failed', 'Failed'
    
class SearchBase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.CREATED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    response = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True # This model is abstract and should not be created as a table in the database.

    # Mapping from model class name to Price model field name
    PRICE_FIELD_MAP = {
        'Mickeyssndob': 'Mickey_SSN_DOB_price',
        'Mickeyssndobnew': 'Mickey_SSN_DOB_New_price',
        'MickeyDL': 'Mickey_DL_price',
        'SamSSN': 'Sam_SSN_price',
        'SamSSNDob': 'Sam_SSN_DOB_price',
        'SamDLV2': 'Sam_DLV2_price',
        'SamAdvancedLookup': 'Sam_Advanced_Lookup_price',
        'SamDOB': 'Sam_DOB_price',
        'SamPhone': 'Sam_Phone_price',
        'SamReversePhone': 'Sam_Reverse_Phone_price',
        'SamReverseSSN': 'Sam_Reverse_SSN_price',
        'SergioSSNDob': 'Sergio_SSN_DOB_price',
        'SergioDL': 'Sergio_DL_price',
        'AlexSSN': 'Alex_SSN_price',
    }

    DISPLAY_NAME = ''

    @classmethod
    def get_price_field(cls):
        return cls.PRICE_FIELD_MAP[cls.__name__]

    @classmethod
    def get_name(cls):
        return cls.DISPLAY_NAME if cls.DISPLAY_NAME else cls.__name__

    def to_dict(self):
        exclude = {"id", "user", "status", "created_at", "updated_at", "response"}
        return {field.name: getattr(self, field.name) for field in self._meta.fields if field.name not in exclude}


class SamSSN(SearchBase):
    DISPLAY_NAME = 'SSN'
    ENDPOINT = "/api/sam/search/ssn/"
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    dob = models.CharField(max_length=255)


class Mickeyssndobnew(SearchBase):
    DISPLAY_NAME = 'SSN+DOB 1'
    ENDPOINT = "/api/mickey/search/ssn_dob_new"
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)


class Mickeyssndob(SearchBase):
    DISPLAY_NAME = 'SSN+DOB 2'
    ENDPOINT = "/api/mickey/search/"
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)


class SamSSNDob(SearchBase):
    DISPLAY_NAME = 'SSN+DOB 3'
    ENDPOINT = "/api/sam/search/ssndob/"
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)


class AlexSSN(SearchBase):
    DISPLAY_NAME = 'SSN+DOB 4'
    ENDPOINT = "/api/alex/search/ssn"
    full_name = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)


class SergioSSNDob(SearchBase):
    DISPLAY_NAME = 'SSN+DOB 5'
    ENDPOINT = "/api/sergio/search/ssndob/"
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)


class SamDOB(SearchBase):
    DISPLAY_NAME = 'DOB'
    ENDPOINT = "/api/sam/search/dob/"
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)


class SergioDL(SearchBase):
    DISPLAY_NAME = 'DL Lookup 1'
    ENDPOINT = "/api/sergio/search/dl/"
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    dob = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)


class SamDLV2(SearchBase):
    DISPLAY_NAME = 'DL Lookup 2'
    ENDPOINT = "/api/sam/search/dlv2/"
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)


class MickeyDL(SearchBase):
    DISPLAY_NAME = 'DL Lookup 3'
    ENDPOINT = "/api/mickey/search/dl"
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    dob = models.CharField(max_length=255)


class SamAdvancedLookup(SearchBase):
    DISPLAY_NAME = 'DOB/VIN/DL'
    ENDPOINT = "/api/sam/search/advancedlookup/"
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)


class SamPhone(SearchBase):
    DISPLAY_NAME = 'Phone Lookup'
    ENDPOINT = "/api/sam/search/phone/"
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    dob = models.CharField(max_length=255)


class SamReversePhone(SearchBase):
    DISPLAY_NAME = 'Reverse Phone'
    ENDPOINT = "/api/sam/search/reversephone/"
    phonenumber = models.CharField(max_length=255)


class SamReverseSSN(SearchBase):
    DISPLAY_NAME = 'Reverse SSN'
    ENDPOINT = "/api/sam/search/reversessn/"
    ssn = models.CharField(max_length=255)

