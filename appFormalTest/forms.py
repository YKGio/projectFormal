from django import forms

class cusForm(forms.Form):
    查詢顧客 = forms.CharField(max_length=50, required=False)

class stockForm(forms.Form):
    查詢商品 = forms.CharField(max_length=50, required=False)
