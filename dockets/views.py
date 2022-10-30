from random import randint

from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer

from dockets.forms import FruitIntakeInitialForm, FruitIntakeSubsequentForm, CrushOrderForm, VarietalEntryForm, \
    VineyardEntryForm, VintageEntryForm
from dockets.models.models import Docket, FruitIntake
from dockets.models.choices import VintageChoices, VarietalChoices, VineyardChoices, UnitChoices, Constants, \
    GrowerChoices, BlockChoices
from dockets.serializers import DocketSerializer, FruitIntakeSerializer


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

        try:
            p = VintageChoices(choice=2012)
            p.save()
            p = VarietalChoices(choice="Pinot Noir")
            p.save()
            p = VineyardChoices(choice="Blue Grouse")
            p.save()
            p = GrowerChoices(choice="Jacob")
            p.save()
            p = BlockChoices(choice=13)
            p.save()
            p = UnitChoices(choice="kg")
            p.save()
        except:
            pass

        if not id:
            existing_fruit_intake = None
            form = FruitIntakeInitialForm()
        else:
            existing_fruit_intake = self.get_fruit_intake_object(id)
            form = FruitIntakeSubsequentForm()
            serializer = FruitIntakeSerializer(existing_fruit_intake)
            form.fields["vintage"].initial = serializer.data["vintage"]
            form.fields["grower"].initial = serializer.data["grower"]
            form.fields["varietal"].initial = serializer.data["varietal"]
            form.fields["vineyard"].initial = serializer.data["vineyard"]
            form.fields["block"].initial = serializer.data["block"]
            form.fields["docket_number"].initial = serializer.data["docket_number"]

        return render(request, self.template_name, {"form": form,
                                                    "data": self.get_all_fruit_intakes(),
                                                    "intake": existing_fruit_intake})

    def post(self, request, id=None, *args, **kwargs):

        if id:
            existing_fruit_intake = self.get_fruit_intake_object(id)
            print("Resuming intake..", existing_fruit_intake)
            print("docket_number:", existing_fruit_intake.docket_number)
            print("Units:", existing_fruit_intake.units)
            form = FruitIntakeSubsequentForm(request.POST)
            serializer = FruitIntakeSerializer(existing_fruit_intake)
            form.fields["docket_number"].initial = serializer.data["docket_number"]
            form.fields["vintage"].initial = serializer.data["vintage"]
            form.fields["grower"].initial = serializer.data["grower"]
            form.fields["varietal"].initial = serializer.data["varietal"]
            form.fields["vineyard"].initial = serializer.data["vineyard"]
            form.fields["block"].initial = serializer.data["block"]
        else:
            existing_fruit_intake = None
            form = FruitIntakeInitialForm(request.POST)

        print("checking validation of", form.data)
        print("Units:", UnitChoices.objects.all())
        if form.is_valid():
            if existing_fruit_intake:
                print("Updating existing fruit intake")
                data = {
                    "date": form.cleaned_data["date"],
                    "number_of_bins": form.cleaned_data["number_of_bins"],
                    "total_weight": form.cleaned_data["total_weight"],
                    "tare_weight": form.cleaned_data["tare_weight"],
                    "units": form.cleaned_data["units"].choice,
                }
                print("serializing:",  data)
                serializer = FruitIntakeSerializer(existing_fruit_intake, data=data)
            else:
                print("Creating new fruit intake")
                data = {
                    "vintage": int(form.cleaned_data["vintage"].choice),
                    "grower": form.cleaned_data["grower"].choice,
                    "varietal": form.cleaned_data["varietal"].choice,
                    "vineyard": form.cleaned_data["vineyard"].choice,
                    "block": int(form.cleaned_data["block"].choice),
                }
                data["docket_number"] = f'{data["vintage"]}{data["vineyard"]}{data["varietal"]}{data["block"]}'.replace(" ", "")
                serializer = FruitIntakeSerializer(data=data)
            if serializer.is_valid():
                test = serializer.save()
            else:
                print("Serializer error", serializer.errors)
                return Response(None, status=status.HTTP_400_BAD_REQUEST)
            return redirect("fruit-intake", id=test.id)
        else:
            print("invalid form")
            return render(request, self.template_name,{"form": form,
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
        renderer_classes = [TemplateHTMLRenderer]
        template_name = "crush_order.html"
        form = CrushOrderForm()
        if id:  # Prefill the form
            docket = self.get_object(id)
            serializer = DocketSerializer(docket)
            form.fields["docket_number"].initial = serializer.data["docket_number"]
            form.fields["vintage"].initial = serializer.data["vintage"]
        return render(request, template_name, {"form": form})

    def post(self, request, id=None, *args, **kwargs):
        form = CrushOrderForm(request.POST)
        if form.is_valid():
            new_data = {
                "vintage": form.cleaned_data["vintage"],
                "docket_number": form.cleaned_data["docket_number"],
            }
            docket = Docket.objects.get(docket_number=new_data["docket_number"])
            data = {"year": new_data["vintage"]}
            print("data type of", data["year"], "is", type(data["year"]))
            serializer = DocketSerializer(docket, data=data, partial=True)
            if serializer.is_valid():
                test = serializer.save()
            else:
                print("Serializer error:", serializer.errors)
                return Response(None, status=status.HTTP_400_BAD_REQUEST)
            return redirect("reports-id", id=test.id)
        else:
            return render(request, "crush_order.html", {"form": form, "docket_number": ""})

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