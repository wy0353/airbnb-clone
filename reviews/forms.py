from django import forms
from . import models as review_models


class CreateReviewForm(forms.ModelForm):

    """ Create Review Form Definition """

    class Meta:
        model = review_models.Review
        fields = (
            "review",
            "accuracy",
            "communication",
            "cleanliness",
            "location",
            "check_in",
            "value",
        )
