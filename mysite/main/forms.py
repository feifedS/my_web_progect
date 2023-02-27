from .models import *
from django import forms

# class Order(forms.ModelForm):
    
#     class Meta:
#         model = Order
#         widgets = {
#             'times_pick': forms.DateTimeInput(),
#         }
#         fields = ("customer",,"times_pick",)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('customer', 'type_of_service',
                'date_created', 'status', 'times_pick',)
        widgets = {
            'times_pick': forms.DateTimeInput(
                attrs={'class': "form-control"}
            ),
        }