from .models import Company, Employee, OwnershipType, BusinessType, Financials
from django import forms
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ["slug", "user", "curators", "holdings"]
        widgets = {"phone_number": PhoneNumberPrefixWidget(initial="KZ"),
                   "fax": PhoneNumberPrefixWidget(initial="KZ"),
                   "board_of_directors": forms.Textarea(attrs={'rows': 3, 'style': 'height: 50px;'}),
                   "members_of_management_board": forms.Textarea(attrs={'rows': 3, 'style': 'height: 50px;'}),
                   "description": forms.Textarea(attrs={'rows': 3, 'style': 'height: 50px;'}),
                   }


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ["company"]
        widgets = {"date_of_birth": forms.SelectDateWidget(years=list(range(1900, 2023)))}


# class CompanyFilterForm(forms.ModelForm):
#     class Meta:
#         model = Company
#         fields = ["business_type", "ownership_type"]

class CompanyFilterForm(forms.Form):
    ownership_type = forms.ModelChoiceField(OwnershipType.objects.all(), required=False, label="Тип собственности")
    business_type = forms.ModelChoiceField(BusinessType.objects.all(), required=False, label="Тип бизнеса")


class FinancialsForm(forms.ModelForm):
    class Meta:
        model = Financials
        exclude = ["company"]