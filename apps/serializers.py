from rest_framework import serializers

from apps.models.models import Docket, CrushOrder, FruitIntake, CrushOrderDocketMapping


class DocketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Docket
        fields = '__all__'


class FruitIntakeSerializer(serializers.ModelSerializer):
    docket = DocketSerializer(read_only=True)

    class Meta:
        model = FruitIntake
        fields = '__all__'


class CrushOrderDocketMappingSerializer(serializers.ModelSerializer):
    docket = DocketSerializer(read_only=True)

    class Meta:
        model = CrushOrderDocketMapping
        fields = '__all__'


class CrushOrderSerializer(serializers.ModelSerializer):
    crush_order_docket_mappings = CrushOrderDocketMappingSerializer(many=True, read_only=True)
    dockets = DocketSerializer(many=True, read_only=True)

    class Meta:
        model = CrushOrder
        fields = '__all__'
