from rest_framework import serializers
from core.models import RealEstate, Property


class RealEstateSerializer(serializers.ModelSerializer):
    """Serializer for a real estate object"""

    class Meta:
        model = RealEstate
        fields = ('id', 'name', 'address')
        read_only_fields = ('id',)


class PropertySerializer(serializers.ModelSerializer):
    """Serializer a property"""
    real_estates = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=RealEstate.objects.all()
    )

    class Meta:
        model = Property
        fields = ('id', 'name', 'address', 'description',
                  'features', 'status', 'type', 'finality',
                  'real_estates')
        read_only_fields = ('id',)


class PropertyDetailSerializer(PropertySerializer):
    """Serializer a property detail"""
    real_estates = RealEstateSerializer(many=True, read_only=True)
