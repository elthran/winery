from annoying.functions import get_object_or_None

from apps.forms import CrushOrderInitialForm, CrushOrderSubsequentForm
from apps.serializers import CrushOrderSerializer, DocketSerializer, CrushMappingSerializer

from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response

from apps.models.models import FruitIntake, CrushOrder, Docket
from apps.views.base import BaseView


class CrushOrderViewSet(BaseView):
    """
    API endpoint that allows users to be viewed or edited.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.template_name = "crush_order.html"

    def get_crush_order_object(self, id_):
        """
        Helper method to get the object with given todo_id, and user_id
        """
        try:
            return CrushOrder.objects.get(id=id_)
        except CrushOrder.DoesNotExist:
            return None

    def get_all_crush_orders(self):
        all_crush_orders = CrushOrder.objects.all()
        return all_crush_orders

    def get(self, request, id_=None, *args, **kwargs):

        # co = CrushOrder.objects.last()
        # for mapping in co.crush_mappings.all():
        #     print(mapping.crush_order)

        if not id_:
            order = None
            form = CrushOrderInitialForm()
        else:
            existing_crush_order = self.get_crush_order_object(id_=id_)
            form = CrushOrderSubsequentForm()
            serializer = CrushOrderSerializer(existing_crush_order)
            order = serializer.data
        form.fields['docket_1'].initial = Docket.objects.last()

        return render(request, self.template_name, {"form": form,
                                                    "data": self.get_all_crush_orders(),
                                                    "order": order})

    def post(self, request, id_=None, *args, **kwargs):

        if id_:
            existing_crush_order = self.get_crush_order_object(id_)
            form = CrushOrderSubsequentForm(request.POST)
        else:
            existing_crush_order = None
            form = CrushOrderInitialForm(request.POST)

        if form.is_valid():
            docket_1 = None
            docket_2 = None
            mapping_1_data = {}
            mapping_2_data = {}
            if existing_crush_order:
                data = {}
                crush_order = CrushOrderSerializer(existing_crush_order, data=data)
            else:
                crush_order_data = {
                    "vintage": int(form.cleaned_data["vintage"].choice),
                }
                if form.cleaned_data["docket_1"] and form.cleaned_data["docket_1_quantity"] and form.cleaned_data["docket_1_units"]:
                    mapping_1_data = {
                        "quantity": int(form.cleaned_data["docket_1_quantity"]),
                        "units": form.cleaned_data["docket_1_units"].choice,
                    }
                    docket_1 = form.cleaned_data["docket_1"]
                    docket_1 = get_object_or_None(Docket, docket_number=docket_1)
                if form.cleaned_data["docket_2"] and form.cleaned_data["docket_2_quantity"] and form.cleaned_data["docket_2_units"]:
                    mapping_2_data = {
                        "quantity": int(form.cleaned_data["docket_2_quantity"]),
                        "units": form.cleaned_data["docket_2_units"].choice,
                    }
                    docket_2 = form.cleaned_data["docket_2"]
                    docket_2 = get_object_or_None(Docket, docket_number=docket_2)
                crush_order = CrushOrderSerializer(data=crush_order_data)
            if crush_order.is_valid():
                crush_order = crush_order.save()
                if docket_1:
                    crush_mapping = CrushMappingSerializer(data=mapping_1_data)
                    if crush_mapping.is_valid():
                        crush_mapping = crush_mapping.save()
                        crush_mapping.crush_order = crush_order
                        crush_mapping.docket = docket_1
                        crush_mapping.save()
                if docket_2:
                    crush_mapping = CrushMappingSerializer(data=mapping_2_data)
                    if crush_mapping.is_valid():
                        crush_mapping = crush_mapping.save()
                        crush_mapping.crush_order = crush_order
                        crush_mapping.docket = docket_2
                        crush_mapping.save()
            else:
                print("Serializer error", crush_order.errors)
                return Response(None, status=status.HTTP_400_BAD_REQUEST)
            return redirect("crush-order", id_=crush_order.id)
        else:
            return render(request, self.template_name, {"form": form,
                                                        "data": self.get_all_crush_orders(),
                                                        "order": existing_crush_order})

    @staticmethod
    def put(request, id, *args, **kwargs):
        return Response(None, status=status.HTTP_501_NOT_IMPLEMENTED)

    @staticmethod
    def delete(request, id, *args, **kwargs):
        return Response(None, status=status.HTTP_501_NOT_IMPLEMENTED)