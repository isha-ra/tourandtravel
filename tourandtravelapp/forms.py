from django.contrib.auth.models import User
from django import forms
from .models import *

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ["title", "offer_starts", "offer_ends",
                  "packages", "details", "cost", "image"]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter title...'
            }),
            'offer_starts': forms.DateInput(attrs={
                'class': 'form-control',
            }),
            'offer_ends': forms.DateInput(attrs={
                'class': 'form-control',
            }),
            'packages': forms.SelectMultiple(attrs={
                'class': 'myselect2',
            }),
            'details': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter details...'
            }),
            'cost': forms.NumberInput(attrs={
                "class": 'form-control',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

class ServicePackageForm(forms.ModelForm):
    class Meta:
        model = ServicePackage
        fields = ["title", "service", "rate", "duration", "details", "image"]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter title...'
            }),
            'service': forms.Select(attrs={
                'class': 'form-control',
            }),
            'rate': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'duration': forms.NumberInput(attrs={
                "class": 'form-control',
            }),
            'details': forms.TextInput(attrs={
                "class": 'form-control',
            }),
            # 'details': SummernoteWidget(),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "comment", ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Fullname...',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your email address...'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your comment...'
            }),

        }


class PackageBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ["package"]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name...'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email...'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your address...'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control datepicker',
                'type': 'date',
                'placeholder': 'Date'
            }),
            'adults': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'kids': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your message...'
            }),
        }
class EnqueryForm(forms.ModelForm):
    package = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control',
        }), queryset=ServicePackage.objects.none())

    class Meta:
        model = Enquery
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name...'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email...'
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter mobile...'
            }),
            'service': forms.Select(attrs={
                'class': 'form-control',
            }),
            'package': forms.Select(attrs={
                'class': 'form-control',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your message...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print(self.data)
        if 'service' in self.data:
            service_obj = self.data.get('service')
            self.fields['package'].queryset = ServicePackage.objects.filter(
                service=service_obj)

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"
        widgets = {
            'sender': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter sender name...'
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter mobile...'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email...'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your subject...'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your message...'
            }),
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = "__all__"
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter title...'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter slug...'
            }),
            'images': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter icon...'
            }),
             'content': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter content..'
            }),
        }

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = "__all__"
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email...'
            }),
        }