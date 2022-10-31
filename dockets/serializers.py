from rest_framework import serializers

from dockets.models.models import Docket, CrushOrder, FruitIntake


class DocketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Docket
        fields = '__all__'  # ["docket_number", 'varietal', 'vineyard', 'block']


class FruitIntakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FruitIntake
        fields = '__all__'


class CrushOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrushOrder
        fields = '__all__'
