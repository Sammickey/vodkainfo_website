from django.contrib import admin

from django.forms import ModelForm

from .models import (
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
    AlexSSN
)

admin.site.register(Price)

admin.site.register(Mickeyssndob)
admin.site.register(Mickeyssndobnew)
admin.site.register(MickeyDL)
admin.site.register(SamSSN)
admin.site.register(SamSSNDob)
admin.site.register(SamDLV2)
admin.site.register(SamAdvancedLookup)
admin.site.register(SamDOB)
admin.site.register(SamPhone)
admin.site.register(SamReversePhone)
admin.site.register(SamReverseSSN)
admin.site.register(SergioSSNDob)
admin.site.register(SergioDL)
admin.site.register(AlexSSN)

