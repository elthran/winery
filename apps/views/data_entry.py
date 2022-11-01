from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response

from apps.forms import VarietalEntryForm, VineyardEntryForm, \
    VintageEntryForm
from apps.models.choices import VintageChoices, VineyardChoices, VarietalChoices
from apps.views.base import BaseView


class DataEntryViewSet(BaseView):
    """
    API endpoint that allows users to be viewed or edited.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
