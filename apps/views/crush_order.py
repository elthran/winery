from annoying.functions import get_object_or_None

from apps.forms import CrushOrderForm
from apps.models.crush_orders import CrushOrder
from apps.models.dockets import Docket
from apps.serializers import CrushOrderSerializer, CrushOrderDocketMappingSerializer

from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response

from apps.models.models import CrushOrderDocketMapping, CrushOrderVesselMapping
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

    def get_form(self, id_, request_):
        if request_:
            form = CrushOrderForm(request_.POST)
        else:
            form = CrushOrderForm()
        if not id_:
            form.fields['docket_1'].initial = Docket.objects.last()
        return form

    def get_all_crush_orders(self):
        all_crush_orders = CrushOrder.objects.all()
        return all_crush_orders

    def get(self, request, id_=None, *args, **kwargs):
        form = self.get_form(id_=id_, request_=None)
        existing_crush_order = self.get_crush_order_object(id_=id_)
        if existing_crush_order:
            serializer = CrushOrderSerializer(existing_crush_order)
            existing_crush_order = serializer.data
        for crush_order in self.get_all_crush_orders():
            print("id: ", crush_order.id)
        return render(request, self.template_name, {"form": form,
                                                    "data": self.get_all_crush_orders(),
                                                    "order": existing_crush_order})

    def post(self, request, id_=None, *args, **kwargs):
        form = self.get_form(id_=id_, request_=request)
        crush_order = self.get_crush_order_object(id_=id_)
        if form.is_valid():
            if crush_order:
                serialized_crush_order = CrushOrderSerializer(crush_order)
            else:
                crush_order_data = {
                    "vintage": int(form.cleaned_data["vintage"].choice),
                    "crush_type": form.cleaned_data["crush_type"].choice,
                }
                serialized_crush_order = CrushOrderSerializer(data=crush_order_data)
            if serialized_crush_order.is_valid():
                crush_order = serialized_crush_order.save()
                for index in [1, 2]:
                    docket = form.cleaned_data[f"docket_{index}"]
                    if docket:
                        try:
                            crush_mapping = CrushOrderDocketMapping(crush_order=crush_order,
                                                         docket=docket,
                                                         quantity=int(form.cleaned_data[f"docket_{index}_quantity"]),
                                                         units=form.cleaned_data[f"docket_{index}_units"].choice)
                            crush_mapping.save()
                        except Exception as e:
                            raise ValueError("Failed to create crush mapping.", e)
                vessel = form.cleaned_data["vessel_1"]
                if vessel:
                    vessel_crush_order_mapping = CrushOrderVesselMapping(crush_order=crush_order,
                                                                         vessel=vessel,
                                                                         quantity=int(form.cleaned_data["vessel_1_amount"]),
                                                                         units="kg")
                    vessel_crush_order_mapping.save()
                vessel = form.cleaned_data["vessel_2"]
                if vessel:
                    vessel_crush_order_mapping = CrushOrderVesselMapping(crush_order=crush_order,
                                                                         vessel=vessel,
                                                                         quantity=int(form.cleaned_data["vessel_2_amount"]),
                                                                         units="kg")
                    vessel_crush_order_mapping.save()
                return redirect("crush-order", id_=crush_order.id)
            else:
                print("Serializer error", serialized_crush_order.errors)
                return Response(None, status=status.HTTP_400_BAD_REQUEST)
        return render(request, self.template_name, {"form": form,
                                                    "data": self.get_all_crush_orders(),
                                                    "order": crush_order})

    @staticmethod
    def put(request, id, *args, **kwargs):
        return Response(None, status=status.HTTP_501_NOT_IMPLEMENTED)

    @staticmethod
    def delete(request, id, *args, **kwargs):
        return Response(None, status=status.HTTP_501_NOT_IMPLEMENTED)