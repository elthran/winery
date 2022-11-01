from annoying.functions import get_object_or_None
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response

from apps.forms import FruitIntakeSubsequentForm, FruitIntakeInitialForm
from apps.models.models import FruitIntake, Docket
from apps.serializers import FruitIntakeSerializer, DocketSerializer
from apps.views.base import BaseView


class FruitIntakeViewSet(BaseView):
    """
    API endpoint that allows users to be viewed or edited.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.template_name = "fruit_intake.html"

    def get_fruit_intake_objects(self, id_=None):
        """
        Return a specific Fruit Intake or all if none are specified.
        """
        if id_:
            return get_object_or_None(FruitIntake, id=id_)
        all_fruit_intakes = FruitIntake.objects.order_by("date").reverse().all()
        return all_fruit_intakes

    def get_or_create_docket(self, data=None):
        """
        Return a specific Fruit Intake or all if none are specified.
        """
        docket_number = f'{data["vintage"]}{data["vineyard"]}{data["varietal"]}{data["block"]}'.replace(" ", "")
        docket = get_object_or_None(Docket, docket_number=docket_number)
        if not docket:
            data["docket_number"] = docket_number
            serializer = DocketSerializer(data=data)
            if serializer.is_valid():
                docket = serializer.save()
            else:
                return Response(None, status=status.HTTP_400_BAD_REQUEST)
        return docket

    def get(self, request, id_=None, *args, **kwargs):

        if not id_:
            intake = None
            form = FruitIntakeInitialForm()
        else:
            existing_fruit_intake = self.get_fruit_intake_objects(id_=id_)
            form = FruitIntakeSubsequentForm()
            serializer = FruitIntakeSerializer(existing_fruit_intake)
            print(serializer)
            intake = serializer.data
            form.fields['date'].initial = intake["date"]
            form.fields['number_of_bins'].initial = intake["number_of_bins"]
            form.fields['total_weight'].initial = intake["total_weight"]
            form.fields['tare_weight'].initial = intake["tare_weight"]
            form.fields['units'].initial = intake["units"]

        return render(request, self.template_name, {"form": form,
                                                    "data": self.get_fruit_intake_objects(),
                                                    "intake": intake})

    def post(self, request, id_=None, *args, **kwargs):

        if id_:
            existing_fruit_intake = self.get_fruit_intake_objects(id_=id_)
            form = FruitIntakeSubsequentForm(request.POST)
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
                docket = None
                serializer = FruitIntakeSerializer(existing_fruit_intake, data=data)
            else:
                data = {
                    "vintage": int(form.cleaned_data["vintage"].choice),
                    "grower": form.cleaned_data["grower"].choice,
                    "varietal": form.cleaned_data["varietal"].choice,
                    "vineyard": form.cleaned_data["vineyard"].choice,
                    "block": int(form.cleaned_data["block"].choice),
                }
                docket = self.get_or_create_docket(data)
                serializer = FruitIntakeSerializer(data=data)
            if serializer.is_valid():  # Assign the docket
                fruit_intake = serializer.save()
                if docket:
                    fruit_intake.docket = docket
                    fruit_intake.save()
            else:
                print("Serializer error", serializer.errors)
                return Response(None, status=status.HTTP_400_BAD_REQUEST)
            return redirect("fruit-intake", id_=fruit_intake.id)
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
