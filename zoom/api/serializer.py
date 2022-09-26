from rest_framework import serializers
from zoom.models import Zoom
# Create your views here.
class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Zoom
        fields='__all__'