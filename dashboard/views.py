from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination
from django.conf import settings

from .utils import format_string

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SearchBase

import json
from django.core.serializers.json import DjangoJSONEncoder



from .forms import (
    MickeyssndobForm,
    MickeyssndobnewForm,
    MickeyDLForm,
    SamSSNForm,
    SamSSNDobForm,
    SamDLV2Form,
    SamAdvancedLookupForm,
    SamDOBForm,
    SamPhoneForm,
    SamReversePhoneForm,
    SamReverseSSNForm,
    SergioSSNDobForm,
    SergioDLForm,
    AlexSSNForm,
)

from dashboard.tasks import call_mickeybot_api
from dashboard.models import (
    Price,
    Mickeyssndob,
    Mickeyssndobnew,
    MickeyDL,
    SamSSN,
    SamSSNDob,
    SamDLV2,
    SamAdvancedLookup,
    SamDOB,
    SamPhone,
    SamReversePhone,
    SamReverseSSN,
    SergioSSNDob,
    SergioDL,
    AlexSSN,
)

def dashboard_index(request):
    if not request.user.is_authenticated:
        return redirect('user_login')

    # List of all form models
    form_models = [
        SamSSN,
        Mickeyssndobnew,
        Mickeyssndob,
        SamSSNDob,
        AlexSSN,
        SergioSSNDob,
        SamDOB,
        SergioDL,
        SamDLV2,
        MickeyDL,
        SamAdvancedLookup,
        SamPhone,
        SamReversePhone,
        SamReverseSSN,
    ]

    # Build forms list for template, including price
    price_obj = Price.objects.last()
    forms = []
    for model in form_models:
        price = None
        try:
            price_field = model.get_price_field()
            price = getattr(price_obj, price_field, None)
        except Exception:
            price = None
        forms.append({
            'name': model.get_name(),
            'url': f'dashboard_{model.__name__.lower()}',
            'price': price
        })

    # Get only API request objects for the logged-in user, order by most recent
    all_requests = []
    processing_requests = []
    for model in form_models:
        all_requests += list(model.objects.filter(user=request.user))
    for req in all_requests:
        req.name = req.__class__.get_name()  # Get the readable name using the class method
        if req.status == 'processing':
            processing_requests.append(req)
    all_requests.sort(key=lambda x: x.updated_at, reverse=True)

    # Get wallet balance for logged-in user
    wallet_balance = None
    try:
        wallet_balance = request.user.wallet.balance
    except Exception:
        wallet_balance = None

    # Serialize processing_requests for JavaScript
    processing_requests_json = [
        {
            'id': req.id,
            'display_name': req.__class__.get_name(),
            'status': req.status
        }
        for req in processing_requests
    ]
    return render(request, 'dashboard/index.html', {
        'processing_requests': processing_requests,
        'processing_requests_json': json.dumps(processing_requests_json, cls=DjangoJSONEncoder),
        'forms': forms,
        'wallet_balance': wallet_balance,
    })


class APIHistoryAPIView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        # Get all API requests for the logged-in user
        # List of all form models
        form_models = [
            SamSSN,
            Mickeyssndobnew,
            Mickeyssndob,
            SamSSNDob,
            AlexSSN,
            SergioSSNDob,
            SamDOB,
            SergioDL,
            SamDLV2,
            MickeyDL,
            SamAdvancedLookup,
            SamPhone,
            SamReversePhone,
            SamReverseSSN,
        ]
        all_requests = []
        for model in form_models:
            all_requests += list(model.objects.filter(user=request.user))

        # Sort by updated_at in descending order
        all_requests.sort(key=lambda x: x.updated_at, reverse=True)

        # Paginate the results
        paginator = PageNumberPagination()
        paginator.page_size = int(request.GET.get('page_size', 10))
        page = paginator.paginate_queryset(all_requests, request)
        # manully serialize the data
        serialized_data = [
            {
                'id': req.id,
                'display_name': req.__class__.get_name(),
                'status': req.status,
                'created_at': req.created_at,
                'updated_at': req.updated_at,
                'response': req.response,
                'model_name': req.__class__.get_name(),
            } for req in page
        ]
        return paginator.get_paginated_response(serialized_data)

def download_text_file(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        model_name = request.POST.get('model_name')
        
        if not data:
            data = "No data provided for download."
        else:
            # For JSON models, try to format the JSON properly
            if model_name in settings.JSON_MODEL_NAMES:
                try:
                    import json
                    import ast
                    
                    # First try to parse as JSON
                    try:
                        parsed_data = json.loads(data)
                    except json.JSONDecodeError:
                        # If that fails, try to evaluate as Python literal (handles single quotes)
                        try:
                            parsed_data = ast.literal_eval(data)
                        except (ValueError, SyntaxError):
                            # Last resort: replace single quotes with double quotes
                            parsed_data = json.loads(data.replace("'", '"'))
                    
                    # Create custom formatted output with tabs for nested data
                    data = format_json_with_tabs(parsed_data)
                except (json.JSONDecodeError, ValueError, SyntaxError) as e:
                    # If all parsing fails, use the original format_string function
                    data = f"Error parsing data: {str(e)}\n\nOriginal data:\n{data}"
        
        response = HttpResponse(data, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="response_{datetime.now().strftime("%Y%m%d%H%M%S")}.txt"'
        return response

def format_json_with_tabs(data, indent_level=0):
    """Format JSON data with tabs for better readability"""
    output = []
    tab = "\t" * indent_level
    
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)) and value:
                # For nested objects/arrays, show the key and then the nested content
                output.append(f"{tab}{key.upper()}:")
                output.append(format_json_with_tabs(value, indent_level + 1))
            elif isinstance(value, list) and not value:
                # Empty list
                output.append(f"{tab}{key.upper()}: (No data)")
            else:
                # Simple key-value pair
                formatted_key = key.replace('_', ' ').title()
                output.append(f"{tab}{formatted_key}: {value}")
    
    elif isinstance(data, list):
        for i, item in enumerate(data, 1):
            if isinstance(item, dict):
                output.append(f"{tab}Item {i}:")
                output.append(format_json_with_tabs(item, indent_level + 1))
            else:
                output.append(f"{tab}Item {i}: {item}")
            
            # Add spacing between items except for the last one
            if i < len(data):
                output.append("")
    
    else:
        # Simple value
        output.append(f"{tab}{data}")
    
    return "\n".join(output)

class SearchBaseStatusView(APIView):
    def get(self, request, display_name, id):
        # Dynamically retrieve the model class from the display name
        model = None
        for subclass in SearchBase.__subclasses__():
            if subclass.get_name() == display_name:
                model = subclass
                break

        if model is None:
            return Response({'error': 'Invalid display name'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = model.objects.get(id=id)
        except model.DoesNotExist:
            return Response({'error': 'Instance not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'status': instance.status})


def handle_api_form(request, form_class):
    title = form_class.Meta.model.get_name()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('dashboard_login')
        form = form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            call_mickeybot_api.delay(obj.user.id, obj.__class__.__name__, obj.id)
            return redirect('dashboard_index')
    else:
        form = form_class()
    return render(request, 'form_display.html', {'form': form, 'title': title})


def dashboard_mickeyssndob(request):
    return handle_api_form(request, MickeyssndobForm)


def dashboard_mickeyssndobnew(request):
    return handle_api_form(request, MickeyssndobnewForm)


def dashboard_mickeydl(request):
    return handle_api_form(request, MickeyDLForm)


def dashboard_samssn(request):
    return handle_api_form(request, SamSSNForm)


def dashboard_samssndob(request):
    return handle_api_form(request, SamSSNDobForm)


def dashboard_samdlv2(request):
    return handle_api_form(request, SamDLV2Form)


def dashboard_samadvancedlookup(request):
    return handle_api_form(request, SamAdvancedLookupForm)


def dashboard_samdob(request):
    return handle_api_form(request, SamDOBForm)


def dashboard_samphone(request):
    return handle_api_form(request, SamPhoneForm)


def dashboard_samreversephone(request):
    return handle_api_form(request, SamReversePhoneForm)


def dashboard_samreversessn(request):
    return handle_api_form(request, SamReverseSSNForm)


def dashboard_sergiossndob(request):
    return handle_api_form(request, SergioSSNDobForm)


def dashboard_sergiodl(request):
    return handle_api_form(request, SergioDLForm)


def dashboard_alexssn(request):
    return handle_api_form(request, AlexSSNForm)

