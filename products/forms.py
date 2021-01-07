from django import forms
from .models import Product,Comment
from django.forms.widgets import Select, SelectMultiple

class SelectWOA(Select):

    def create_option(self, name, value, label, selected, index, 
                      subindex=None, attrs=None):
        if isinstance(label, dict):
            opt_attrs = label.copy()
            label = opt_attrs.pop('label')
        else: 
            opt_attrs = {}
        option_dict = super(SelectWOA, self).create_option(name, value, 
            label, selected, index, subindex=subindex, attrs=attrs)
        for key,val in opt_attrs.items():
            option_dict['attrs'][key] = val
        return option_dict

class ProductCreateForm(forms.ModelForm):
    pCondition=[
        ('New','New'),
        ('Used','Used'),
    ]
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter title'}))
    categories = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Categories separated by comma. Example: chinese,thai'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    location = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Location'}))
    price = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Price'}))
    condition = forms.ChoiceField(label="Condition",choices=pCondition,widget=SelectWOA)
    quantity = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Quantity'}))
    details = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Product
        fields = ['title','image','categories','location','price','condition','quantity','details']
