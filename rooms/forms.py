from django import forms
from django_countries.fields import CountryField
from . import models as room_models

class SearchForm(forms.Form):

    city = forms.CharField(initial="Anywhere")
    country = CountryField(default="KR").formfield()
    room_type = forms.ModelChoiceField(required=False, empty_label="Any kind", queryset=room_models.RoomType.objects.all())
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(required=False, queryset=room_models.Amenity.objects.all(), widget=forms.CheckboxSelectMultiple)
    facilities = forms.ModelMultipleChoiceField(required=False, queryset=room_models.Facility.objects.all(), widget=forms.CheckboxSelectMultiple)
    house_rules = forms.ModelMultipleChoiceField(required=False, queryset=room_models.HouseRule.objects.all(), widget=forms.CheckboxSelectMultiple)


class PhotoCreateForm(forms.ModelForm):

    class Meta:
        model = room_models.Photo
        fields = (
            "caption",
            "file",
        )

    def clean(self):
        caption = self.cleaned_data["caption"]
        if caption is None:
            self.add_error("caption", forms.ValidationError("Caption is required."))
        file = self.cleaned_data["file"]
        if file is None:
            self.add_error("file", forms.ValidationError("Photo file is required."))
        return self.cleaned_data

    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        room = room_models.Room.objects.get(pk=pk)
        photo.room = room
        photo.save()


class RoomCreateForm(forms.ModelForm):

    """ Room create form definition """

    class Meta:
        model = room_models.Room
        fields = (
            "name",
            "description",
            "country",
            "city",
            "address",
            "price",
            "guests",
            "beds",
            "bedrooms",
            "baths",
            "check_in",
            "check_out",
            "instant_book",
            "room_type",
            "house_rules",
            "amenities",
            "facilities",
        )

    def save(self, *args, **kwargs):
        return super().save(commit=False)

