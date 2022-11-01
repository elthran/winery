from rest_framework import serializers

from apps.models.models import Docket, CrushOrder, FruitIntake, CrushMapping


class DocketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Docket
        fields = '__all__'


class FruitIntakeSerializer(serializers.ModelSerializer):
    docket = DocketSerializer(read_only=True)

    class Meta:
        model = FruitIntake
        fields = '__all__'


class CrushMappingSerializer(serializers.ModelSerializer):
    docket = DocketSerializer(read_only=True)

    class Meta:
        model = CrushMapping
        fields = '__all__'


class CrushOrderSerializer(serializers.ModelSerializer):
    crush_mappings = CrushMappingSerializer(many=True, read_only=True)

    class Meta:
        model = CrushOrder
        fields = '__all__'
