from django import forms
from lean_canvas.models import Channel


class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ["channel"]
