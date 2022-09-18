from rest_framework import serializers

from dockets.models import Docket, Order, Vessel


class DocketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Docket
        fields = '__all__' # ["docket_number", 'varietal', 'vineyard', 'block']

# {"varietal": "grapey", "vineyard": "mine", "block": "7"}

class VesselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vessel
        fields = ["id", "dockets"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "dockets"]
