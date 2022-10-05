import json
from datetime import datetime
from random import randint

from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer

from dockets.forms import FruitIntakeForm, CrushOrderForm, VarietalEntryForm, VineyardEntryForm, \
    VintageEntryForm
from dockets.models import Docket, VarietalChoices, VintageChoices, Constants, VineyardChoices
from dockets.serializers import DocketSerializer


class FruitIntakeViewSet(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_object(self, id):
        '''
        Helper method to get the object with given todo_id, and user_id
        '''
        try:
            return Docket.objects.get(id=id)
        except Docket.DoesNotExist:
            return None

    def get(self, request, id=None, *args, **kwargs):
        renderer_classes = [TemplateHTMLRenderer]
        template_name = 'fruit_intake.html'


        try:
            p = Constants(choice="vintage", data_type="int")
            p.save()
        except:
            pass
        try:
            p = VintageChoices(choice=2012)
            p.save()
        except:
            pass
        try:
            p = VarietalChoices(choice="Pinot Noir")
            p.save()
        except:
            pass

        form = FruitIntakeForm()
        if id:
            docket = self.get_object(id)
            serializer = DocketSerializer(docket)
        else:
            dockets = Docket.objects.all()
            serializer = DocketSerializer(dockets, many=True)
        return render(request, template_name, {'form': form, 'reports': serializer.data})

    def post(self, request, id=None, *args, **kwargs):
        form = FruitIntakeForm(request.POST, initial={"block": 3})
        if form.is_valid():
            data = {
                'varietal': form.cleaned_data['varietal'],
                'vineyard': form.cleaned_data['vineyard'],
                'vintage': form.cleaned_data['vintage'],
                'block': form.cleaned_data['block'],
                'grower': form.cleaned_data['grower'],
                'date': form.cleaned_data['date'],
            }
            data['docket_number'] = str(data['varietal']) + str(data['vineyard']) + str(data['block']) + str(randint(1, 100))
            serializer = DocketSerializer(data=data)
            if serializer.is_valid():
                test = serializer.save()
            else:
                print("Serializer error", serializer.errors)
                return Response(None, status=status.HTTP_400_BAD_REQUEST)
            return redirect('crush-order-id', id=test.id)
            # return render(request, 'crush_order.html', {'docket_number': {test.docket_number}})
        else:
            print("invalid form")
            return render(request, 'fruit_intake.html', {'form': form})

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
        '''
        Helper method to get the object with given todo_id, and user_id
        '''
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
        template_name = 'crush_order.html'
        form = CrushOrderForm()
        if id:  # Prefill the form
            docket = self.get_object(id)
            serializer = DocketSerializer(docket)
            form.fields["docket_number"].initial = serializer.data["docket_number"]
            form.fields["vintage"].initial = serializer.data["vintage"]
        return render(request, template_name, {'form': form})

    def post(self, request, id=None, *args, **kwargs):
        form = CrushOrderForm(request.POST)
        if form.is_valid():
            new_data = {
                'vintage': form.cleaned_data['vintage'],
                'docket_number': form.cleaned_data['docket_number'],
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
            return redirect('reports-id', id=test.id)
        else:
            return render(request, 'crush_order.html', {'form': form, 'docket_number': ""})

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
        '''
        Helper method to get the object with given todo_id, and user_id
        '''
        try:
            return Docket.objects.get(id=id)
        except Docket.DoesNotExist:
            return None

    def get(self, request, id=None, *args, **kwargs):
        """
        Retrieve the prepared dataset.

        :return: (JSON) The incident reports and a 200 status on success
        """
        template_name = 'reports.html'
        print("id:", id)
        if id:
            docket = self.get_object(id)
            serializer = DocketSerializer(docket)
            data = [serializer.data]
        else:
            dockets = Docket.objects.all()
            serializer = DocketSerializer(dockets, many=True)
            data = serializer.data
        return render(request, template_name, {'data': data})

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
        self.template_name = 'data_entry.html'

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
        return render(request, self.template_name, {'form': form, 'data': data_type})

    def post(self, request, data_type="vintage", *args, **kwargs):
        if data_type == "varietal":
            form = VarietalEntryForm(request.POST)
        elif data_type == "vineyard":
            form = VineyardEntryForm(request.POST)
        elif data_type == "vintage":
            form = VintageEntryForm(request.POST)
        else:
            return Response(None, status=status.HTTP_501_NOT_IMPLEMENTED)
        if form.is_valid():
            new_data = {
                'existing_field': form.cleaned_data['existing_field'],
                'edit_value': form.cleaned_data['edit_value'],
                'new_value': form.cleaned_data['new_value'],
            }
            if form.cleaned_data['new_value']:
                if data_type == "vintage":
                    new_choice = VintageChoices(choice=form.cleaned_data['new_value'])
                elif data_type == "vineyard":
                    new_choice = VineyardChoices(choice=form.cleaned_data['new_value'])
                elif data_type == "varietal":
                    new_choice = VarietalChoices(choice=form.cleaned_data['new_value'])
                new_choice.save()
            elif form.cleaned_data['edit_value']:
                field_to_replace = form.cleaned_data['existing_field'].choice
                if data_type == "vintage":
                    existing_choice = VintageChoices.objects.get(choice=field_to_replace)
                elif data_type == "vineyard":
                    existing_choice = VineyardChoices.objects.get(choice=field_to_replace)
                elif data_type == "varietal":
                    existing_choice = VarietalChoices.objects.get(choice=field_to_replace)
                existing_choice.choice = form.cleaned_data['edit_value']  # change field
                existing_choice.save()  # this will update only
            return redirect('data-entry-type', data_type=data_type)
        else:
            print("form invalid")
            return render(request, self.template_name, {'form': form, 'docket_number': ""})

    @staticmethod
    def put(request, id, *args, **kwargs):
        return Response(None, status=status.HTTP_501_NOT_IMPLEMENTED)

    @staticmethod
    def delete(request, id, *args, **kwargs):
        return Response(None, status=status.HTTP_501_NOT_IMPLEMENTED)