from random import randint

from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer

from dockets.forms import FruitIntakeInitialForm, FruitIntakeSubsequentForm, CrushOrderInitialForm, VarietalEntryForm, \
    VineyardEntryForm, VintageEntryForm, CrushOrderSubsequentForm
from dockets.models.models import Docket, FruitIntake, CrushOrder
from dockets.models.choices import VintageChoices, VarietalChoices, VineyardChoices
from dockets.serializers import DocketSerializer, FruitIntakeSerializer, CrushOrderSerializer


class FruitIntakeViewSet(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.template_name = "fruit_intake.html"

    def get_fruit_intake_object(self, id):
        """
        Helper method to get the object with given todo_id, and user_id
        """
        try:
            return FruitIntake.objects.get(id=id)
        except FruitIntake.DoesNotExist:
            return None

    def get_all_fruit_intakes(self):
        all_fruit_intakes = FruitIntake.objects.order_by("date").reverse().all()
        return all_fruit_intakes

    def get(self, request, id=None, *args, **kwargs):
        renderer_classes = [TemplateHTMLRenderer]

        if not id:
            intake = None
            form = FruitIntakeInitialForm()
        else:
            existing_fruit_intake = self.get_fruit_intake_object(id)
            form = FruitIntakeSubsequentForm()
            serializer = FruitIntakeSerializer(existing_fruit_intake)
            intake = serializer.data

        return render(request, self.template_name, {"form": form,
                                                    "data": self.get_all_fruit_intakes(),
                                                    "intake": intake})

    def post(self, request, id=None, *args, **kwargs):

        if id:
            existing_fruit_intake = self.get_fruit_intake_object(id)
            form = FruitIntakeSubsequentForm(request.POST)
            serializer = FruitIntakeSerializer(existing_fruit_intake)
        else:
            existing_fruit_intake = None
            form = FruitIntakeInitialForm(request.POST)

        if form.is_valid():
            if existing_fruit_intake:
                data = {
                    "date": form.cleaned_data["date"],
                    "number_of_bins": form.cleaned_data["number_of_bins"],
                    "total_weight": form.cleaned_data["total_weight"],
                    "tare_weight": form.cleaned_data["tare_weight"],
                    "units": form.cleaned_data["units"].choice,
                }
                serializer = FruitIntakeSerializer(existing_fruit_intake, data=data)
            else:
                data = {
                    "vintage": int(form.cleaned_data["vintage"].choice),
                    "grower": form.cleaned_data["grower"].choice,
                    "varietal": form.cleaned_data["varietal"].choice,
                    "vineyard": form.cleaned_data["vineyard"].choice,
                    "block": int(form.cleaned_data["block"].choice),
                }
                data["docket_number"] = f'{data["vintage"]}{data["vineyard"]}{data["varietal"]}{data["block"]}'.replace(
                    " ", "")
                serializer = FruitIntakeSerializer(data=data)
            if serializer.is_valid():
                test = serializer.save()
            else:
                print("Serializer error", serializer.errors)
                return Response(None, status=status.HTTP_400_BAD_REQUEST)
            return redirect("fruit-intake", id=test.id)
        else:
            print("invalid form")
            return render(request, self.template_name, {"form": form,
                                                        "data": self.get_all_fruit_intakes(),
                                                        "intake": existing_fruit_intake})

    @staticmethod
    def put(request, id, *args, **kwargs):
        return Response(None, status=status.HTTP_501_NOT_IMPLEMENTED)

    @staticmethod
    def delete(request, id, *args, **kwargs):
        return Response(None, status=status.HTTP_501_NOT_IMPLEMENTED)


class CrushOrderViewSet(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.template_name = "crush_order.html"

    def get_crush_order_object(self, id):
        """
        Helper method to get the object with given todo_id, and user_id
        """
        try:
            return CrushOrder.objects.get(id=id)
        except CrushOrder.DoesNotExist:
            return None

    def get_all_crush_orders(self):
        all_crush_orders = CrushOrder.objects.reverse().all()
        return all_crush_orders

    def get(self, request, id=None, *args, **kwargs):
        if not id:
            order = None
            form = CrushOrderInitialForm()
        else:
            existing_crush_order = self.get_crush_order_object(id)
            form = CrushOrderSubsequentForm()
            serializer = CrushOrderSerializer(existing_crush_order)
            order = serializer.data

        return render(request, self.template_name, {"form": form,
                                                    "data": self.get_all_crush_orders(),
                                                    "order": order})

    def post(self, request, id=None, *args, **kwargs):

        if id:
            existing_crush_order = self.get_crush_order_object(id)
            form = CrushOrderSubsequentForm(request.POST)
            serializer = CrushOrderSerializer(existing_crush_order)
        else:
            existing_crush_order = None
            form = CrushOrderInitialForm(request.POST)

        if form.is_valid():
            if existing_crush_order:
                data = {
                    "date": form.cleaned_data["date"],
                    "number_of_bins": form.cleaned_data["number_of_bins"],
                    "total_weight": form.cleaned_data["total_weight"],
                    "tare_weight": form.cleaned_data["tare_weight"],
                    "units": form.cleaned_data["units"].choice,
                }
                serializer = CrushOrderSerializer(existing_crush_order, data=data)
            else:
                data = {
                    "vintage": int(form.cleaned_data["vintage"].choice),
                    "grower": form.cleaned_data["grower"].choice,
                    "varietal": form.cleaned_data["varietal"].choice,
                    "vineyard": form.cleaned_data["vineyard"].choice,
                    "block": int(form.cleaned_data["block"].choice),
                }
                serializer = CrushOrderSerializer(data=data)
            if serializer.is_valid():
                test = serializer.save()
            else:
                print("Serializer error", serializer.errors)
                return Response(None, status=status.HTTP_400_BAD_REQUEST)
            return redirect("crush-order", id=test.id)
        else:
            print("invalid form")
            return render(request, self.template_name, {"form": form,
                                                        "data": self.get_all_crush_orders(),
                                                        "order": existing_crush_order})

    @staticmethod
    def put(request, id, *args, **kwargs):
        return Response(None, status=status.HTTP_501_NOT_IMPLEMENTED)

    @staticmethod
    def delete(request, id, *args, **kwargs):
        return Response(None, status=status.HTTP_501_NOT_IMPLEMENTED)


class ReportsViewSet(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_object(self, id):
        """
        Helper method to get the object with given todo_id, and user_id
        """
        try:
            return Docket.objects.get(id=id)
        except Docket.DoesNotExist:
            return None

    def get(self, request, id=None, *args, **kwargs):
        """
        Retrieve the prepared dataset.

        :return: (JSON) The incident reports and a 200 status on success
        """
        template_name = "reports.html"
        print("id:", id)
        if id:
            docket = self.get_object(id)
            serializer = DocketSerializer(docket)
            data = [serializer.data]
        else:
            dockets = Docket.objects.all()
            serializer = DocketSerializer(dockets, many=True)
            data = serializer.data
        return render(request, template_name, {"data": data})

    @staticmethod
    def post(request, id=None, *args, **kwargs):
        return Response(None, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request, id, *args, **kwargs):
        return Response(None, status=status.HTTP_501_NOT_IMPLEMENTED)

    @staticmethod
    def delete(request, id, *args, **kwargs):
        return Response(None, status=status.HTTP_501_NOT_IMPLEMENTED)


class DataEntryViewSet(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.renderer_classes = [TemplateHTMLRenderer]
        self.template_name = "data_entry.html"

    @staticmethod
    def get_form(data_type, method="GET"):
        if data_type == "varietal":
            return VarietalEntryForm()
        elif data_type == "vineyard":
            return VineyardEntryForm()
        elif data_type == "vintage":
            return VintageEntryForm()
        else:
            return Response(None, status=status.HTTP_501_NOT_IMPLEMENTED)

    def get(self, request, data_type="vintage", *args, **kwargs):
        """
        Retrieve the prepared dataset.

        :return: (JSON) The incident reports and a 200 status on success
        """
        form = self.get_form(data_type)
        return render(request, self.template_name, {"form": form, "data": data_type})

    def post(self, request, data_type="vintage", *args, **kwargs):
        if data_type == "varietal":
            form = VarietalEntryForm(request.POST)
        elif data_type == "vineyard":
            form = VineyardEntryForm(request.POST)
        elif data_type == "vintage":
            form = VintageEntryForm(request.POST)
        else:
            return Response(None, status=status.HTTP_501_NOT_IMPLEMENTED)
        print("checking validation of", form.data)
        if form.is_valid():
            new_data = {
                "existing_field": form.cleaned_data["existing_field"],
                "edit_value": form.cleaned_data["edit_value"],
                "new_value": form.cleaned_data["new_value"],
            }
            if form.cleaned_data["new_value"]:
                if data_type == "vintage":
                    new_choice = VintageChoices(choice=form.cleaned_data["new_value"])
                elif data_type == "vineyard":
                    new_choice = VineyardChoices(choice=form.cleaned_data["new_value"])
                elif data_type == "varietal":
                    new_choice = VarietalChoices(choice=form.cleaned_data["new_value"])
                new_choice.save()
            elif form.cleaned_data["edit_value"]:
                field_to_replace = form.cleaned_data["existing_field"].choice
                if data_type == "vintage":
                    existing_choice = VintageChoices.objects.get(choice=field_to_replace)
                elif data_type == "vineyard":
                    existing_choice = VineyardChoices.objects.get(choice=field_to_replace)
                elif data_type == "varietal":
                    existing_choice = VarietalChoices.objects.get(choice=field_to_replace)
                existing_choice.choice = form.cleaned_data["edit_value"]  # change field
                existing_choice.save()  # this will update only
            return redirect("data-entry-type", data_type=data_type)
        else:
            print("form invalid")
            return render(request, self.template_name, {"form": form, "docket_number": ""})

    @staticmethod
    def put(request, id, *args, **kwargs):
        return Response(None, status=status.HTTP_501_NOT_IMPLEMENTED)

    @staticmethod
    def delete(request, id, *args, **kwargs):
        return Response(None, status=status.HTTP_501_NOT_IMPLEMENTED)
