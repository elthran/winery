from annoying.functions import get_object_or_None

from apps.forms import CrushOrderForm
from apps.models.vessels import Vessel
from apps.serializers import CrushOrderSerializer, CrushOrderDocketMappingSerializer

from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response

from apps.views.base import BaseView


class RackingViewSet(BaseView):
    """
    API endpoint that allows users to be viewed or edited.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.template_name = "racking.html"

    def get(self, request, id_=None, *args, **kwargs):
        all_vessels = Vessel.objects.all()
        return render(request, self.template_name, {"data": all_vessels})

    def post(self, request, id_=None, *args, **kwargs):
        return Response(None, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request, id, *args, **kwargs):
        return Response(None, status=status.HTTP_501_NOT_IMPLEMENTED)

    @staticmethod
    def delete(request, id, *args, **kwargs):
        return Response(None, status=status.HTTP_501_NOT_IMPLEMENTED)