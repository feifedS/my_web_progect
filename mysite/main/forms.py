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
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
            # there's a `fields` property now
        self.fields['customer'].required = False
        self.fields['type_of_service'].required = False
        # self.fields['date_created'].required = False
        self.fields['status'].required = False
        self.fields['times_pick'].required = False
        # for field in self.fields:
        #     classes = self.fields[field].widget.attrs.get('class', '')
        #     classes += ' form-control'
        #     self.fields[field].widget.attrs['class'] = classes
    class Meta:
        
        model = Order
        fields = ('customer', 'type_of_service',
                'status', 'times_pick',)
        

# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ('__all__')
#         # widgets = {
#         #     'times_pick': forms.DateTimeInput(
#         #         attrs={'class': "form-control"}
#         #     ),
            
#         # }
