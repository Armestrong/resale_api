from rest_framework import serializers
from core.models import RealEstate


class RealEstateSerializer(serializers.ModelSerializer):
    """Serializer for a real estate object"""

    class Meta:
        model = RealEstate
        fields = ('id', 'name', 'address')
        ready_only_fields = ('id',)
