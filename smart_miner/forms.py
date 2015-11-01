from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UploadForm(forms.Form):
    file = forms.FileField()
    
class MissingForm(forms.Form):
    CHOICES =   (('1', 'Mean Imputation'), ('2', 'Hot Deck Imputation'))
    method = forms.ChoiceField(widget=forms.RadioSelect(), choices=CHOICES)
