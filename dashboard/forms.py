from django.forms import ModelForm

from .models import (
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
    AlexSSN
)

# Global exclude fields for SearchBase-inherited models
SEARCHBASE_EXCLUDE_FIELDS = ['user', 'status', 'created_at', 'updated_at', 'response']


class MickeyssndobForm(ModelForm):
    class Meta:
        model = Mickeyssndob
        fields = '__all__'
        exclude = SEARCHBASE_EXCLUDE_FIELDS

class MickeyssndobnewForm(ModelForm):
    class Meta:
        model = Mickeyssndobnew
        fields = '__all__'
        exclude = SEARCHBASE_EXCLUDE_FIELDS

class MickeyDLForm(ModelForm):
    class Meta:
        model = MickeyDL
        fields = '__all__'
        exclude = SEARCHBASE_EXCLUDE_FIELDS

class SamSSNForm(ModelForm):
    class Meta:
        model = SamSSN
        fields = '__all__'
        exclude = SEARCHBASE_EXCLUDE_FIELDS

class SamSSNDobForm(ModelForm):
    class Meta:
        model = SamSSNDob
        fields = '__all__'
        exclude = SEARCHBASE_EXCLUDE_FIELDS

class SamDLV2Form(ModelForm):
    class Meta:
        model = SamDLV2
        fields = '__all__'
        exclude = SEARCHBASE_EXCLUDE_FIELDS

class SamAdvancedLookupForm(ModelForm):
    class Meta:
        model = SamAdvancedLookup
        fields = '__all__'
        exclude = SEARCHBASE_EXCLUDE_FIELDS

class SamDOBForm(ModelForm):
    class Meta:
        model = SamDOB
        fields = '__all__'
        exclude = SEARCHBASE_EXCLUDE_FIELDS

class SamPhoneForm(ModelForm):
    class Meta:
        model = SamPhone
        fields = '__all__'
        exclude = SEARCHBASE_EXCLUDE_FIELDS

class SamReversePhoneForm(ModelForm):
    class Meta:
        model = SamReversePhone
        fields = '__all__'
        exclude = SEARCHBASE_EXCLUDE_FIELDS

class SamReverseSSNForm(ModelForm):
    class Meta:
        model = SamReverseSSN
        fields = '__all__'
        exclude = SEARCHBASE_EXCLUDE_FIELDS

class SergioSSNDobForm(ModelForm):
    class Meta:
        model = SergioSSNDob
        fields = '__all__'
        exclude = SEARCHBASE_EXCLUDE_FIELDS

class SergioDLForm(ModelForm):
    class Meta:
        model = SergioDL
        fields = '__all__'
        exclude = SEARCHBASE_EXCLUDE_FIELDS

class AlexSSNForm(ModelForm):
    class Meta:
        model = AlexSSN
        fields = '__all__'
        exclude = SEARCHBASE_EXCLUDE_FIELDS
