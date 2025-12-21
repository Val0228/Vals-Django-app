from django import forms
from .models import ModuleSubmission, StudentModuleRegistration, ContactEnquiry

class ModuleSubmissionForm(forms.ModelForm):
    class Meta:
        model = ModuleSubmission
        fields = ['file', 'notes']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.zip,.rar,.txt'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Add any additional notes or comments about your submission...'
            })
        }
        labels = {
            'file': 'Upload File',
            'notes': 'Additional Notes'
        }
        help_texts = {
            'file': 'Accepted formats: PDF, DOC, DOCX, ZIP, RAR, TXT',
            'notes': 'Optional: Add any comments or notes about your submission'
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactEnquiry
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject of your enquiry'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Please provide details about your enquiry...'
            })
        }
        labels = {
            'name': 'Your Name',
            'email': 'Email Address',
            'subject': 'Subject',
            'message': 'Your Message'
        }

