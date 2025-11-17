from django import forms
from adminis.models import Store, Landlord

class StoreForm(forms.ModelForm):
    # Add landlord fields inside the same form
    landlord_name = forms.CharField(max_length=100, label="Landlord Name")
    landlord_email = forms.EmailField(required=False, label="Landlord Email")
    landlord_phone = forms.CharField(max_length=20, required=False, label="Landlord Phone")

    class Meta:
        model = Store
        fields = ['store_name', 'location', 'established_date']
        widgets={
            'established_date': forms.DateInput(attrs={'type': 'date'})
        }

    def save(self, commit=True):
        # First create landlord
        landlord = Landlord.objects.create(
            name=self.cleaned_data['landlord_name'],
            email=self.cleaned_data.get('landlord_email', ''),
            phone=self.cleaned_data.get('landlord_phone', '')
        )
        # Then create store
        store = super().save(commit=False)
        store.landlord = landlord
        if commit:
            store.save()
        return store
