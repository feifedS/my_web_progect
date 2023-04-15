from datetime import timedelta
from .models import *
from django import forms
from django.contrib.auth.forms import UserChangeForm
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
# class BookingForm(forms.Form):
#     category = forms.ModelChoiceField(queryset=Category.objects.all())
#     service = forms.ModelChoiceField(queryset= TypesOfServices.objects.all() )
#     barber = forms.ModelChoiceField(queryset=Barber.objects.all())
#     date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 
#                'type': 'date'
#               }),)
#     def __init__(self, *args, **kwargs):
#             super().__init__(*args, **kwargs)
#             if 'category' in self.data:
#                 category_id = self.data.get('category')
#                 self.fields['service'].queryset = TypesOfServices.objects.filter(category_id=category_id)
#             if 'service' in self.data:
#                 service_id = self.data.get('service')
#                 self.fields['barber'].queryset = Barber.objects.filter(services__id=service_id)

class BookingForm(forms.Form):

    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)
    service = forms.ModelChoiceField(queryset=TypesOfServices.objects.none(), empty_label=None)
    barber = forms.ModelChoiceField(queryset=Barber.objects.none(), empty_label=None)
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'category' in self.data:
            category_id = self.data.get('category')
            self.fields['service'].queryset = TypesOfServices.objects.filter(category_id=category_id)
        if 'service' in self.data:
            service_id = self.data.get('service')
            self.fields['barber'].queryset = Barber.objects.filter(services=service_id)

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < datetime.datetime.now().date():
            raise forms.ValidationError('Пожалуйста, выберите дату, начиная с сегодняшнего дня.')
        if date > (datetime.datetime.now().date() + timedelta(days=21)):
            raise forms.ValidationError('Пожалуйста, выберите дату в течение 21 дня.')
        return date
    
    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get("service")
        barber = cleaned_data.get("barber")

        if service and barber:
            if service not in barber.services.all():
                raise forms.ValidationError("Выбранный парикмахер не предлагает выбранные услуги.")



 
            
class BookinForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)
    def __init__(self, *args, **kwargs):
        super(BookinForm, self).__init__(*args, **kwargs)
            # there's a `fields` property now
        self.fields['barber'].required = False
        self.fields['customer'].required = False
        # self.fields['date_created'].required = False
        self.fields['date'].required = False
        self.fields['time'].required = False
        self.fields['service'].required = False
        # for field in self.fields:
        #     classes = self.fields[field].widget.attrs.get('class', '')
        #     classes += ' form-control'
        #     self.fields[field].widget.attrs['class'] = classes
    class Meta:
        
        model = Booking
        fields = ('barber', 'customer',
                'date', 'time','service')
        

class CustomUserForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'age', 'gender', )
# class BookinForm(forms.Form):

#     category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)
#     service = forms.ModelChoiceField(queryset=TypesOfServices.objects.none(), empty_label=None)
#     barber = forms.ModelChoiceField(queryset=Barber.objects.none(), empty_label=None)
#     date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
#     customer = forms.ModelChoiceField(queryset=Barber.objects.none(), empty_label=None)
#     status = forms.ModelChoiceField(queryset=Barber.objects.none(), empty_label=None)
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if 'category' in self.data:
#             category_id = self.data.get('category')
#             self.fields['service'].queryset = TypesOfServices.objects.filter(category_id=category_id)
#         if 'service' in self.data:
#             service_id = self.data.get('service')
#             self.fields['barber'].queryset = Barber.objects.filter(services=service_id)

#     def clean_date(self):
#         date = self.cleaned_data.get('date')
#         if date < datetime.datetime.now().date():
#             raise forms.ValidationError('Пожалуйста, выберите дату, начиная с сегодняшнего дня.')
#         if date > (datetime.datetime.now().date() + timedelta(days=21)):
#             raise forms.ValidationError('Пожалуйста, выберите дату в течение 21 дня.')
#         return date
    
#     def clean(self):
#         cleaned_data = super().clean()
#         service = cleaned_data.get("service")
#         barber = cleaned_data.get("barber")

#         if service and barber:
#             if service not in barber.services.all():
#                 raise forms.ValidationError("Выбранный парикмахер не предлагает выбранные услуги.")