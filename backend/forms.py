# backend/forms.py
from django import forms
from .models import BirthdayDiscount,DeliveryCoupon,FreeGames4Gamers,GovOJTs,YoutubeVideos,Rent591

class BirthdayDiscountForm(forms.ModelForm):
    class Meta:
        model = BirthdayDiscount
        fields = "__all__"  

class DeliveryCouponForm(forms.ModelForm):
    class Meta:
        model = DeliveryCoupon
        fields = "__all__"
        
class FreeGames4GamersForm(forms.ModelForm):
    class Meta:
        model = FreeGames4Gamers
        fields = [
            "title",
            "description",
            "link",
            "publish_date",
            "is_push",
        ]

        widgets = {
            "publish_date": forms.DateInput(attrs={"type": "date"}),
        }
        
class GovOJTsForm(forms.ModelForm):
    class Meta:
        model = GovOJTs
        fields = "__all__"
        widgets = {
            "publish_date": forms.DateInput(attrs={"type": "date"}),
        }
        
class YoutubeVideosForm(forms.ModelForm):
    class Meta:
        model = YoutubeVideos
        fields = ["video_id", "title", "channel_name", "published_at"]
        widgets = {
            "published_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
class Rent591Form(forms.ModelForm):
    class Meta:
        model = Rent591
        fields = ['title', 'region', 'price_info', 'link']