import json
from random import randint

from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer

from dockets.forms import FruitIntakeForm, CrushOrderForm
from dockets.models import Docket
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
        """
        Retrieve the prepared dataset.

        :return: (JSON) The incident reports and a 200 status on success
        """
        renderer_classes = [TemplateHTMLRenderer]
        template_name = 'fruit_intake.html'
        if id:
            docket = self.get_object(id)
            serializer = DocketSerializer(docket)
        else:
            dockets = Docket.objects.all()
            serializer = DocketSerializer(dockets, many=True)
        return render(request, template_name, {'data': serializer.data})

    def post(self, request, id=None, *args, **kwargs):
        if request.method == 'POST':
            form = FruitIntakeForm(request.POST)
            if form.is_valid():
                data = {
                    'varietal': form.cleaned_data['varietal'],
                    'vineyard': form.cleaned_data['vineyard'],
                    'block': form.cleaned_data['block'],
                }
                data['docket_number'] = data['varietal'] + data['vineyard'] + data['block'] + str(randint(1, 100))
                serializer = DocketSerializer(data=data)
                if serializer.is_valid():
                    test = serializer.save()
                else:
                    print("Serializer error", serializer.errors)
                    return Response(None, status=status.HTTP_400_BAD_REQUEST)
                return redirect('crush-order-id', id=test.id)
                # return render(request, 'crush_order.html', {'docket_number': {test.docket_number}})
            else:
                print("invalid")
        else:
            form = FruitIntakeForm()
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
        if id:
            docket = self.get_object(id)
            serializer = DocketSerializer(docket)
            docket_number = serializer.data["docket_number"]
        else:
            dockets = Docket.objects.all()
            serializer = DocketSerializer(dockets, many=True)
            docket_number = ""
        return render(request, template_name, {'docket_number': docket_number})

    def post(self, request, id=None, *args, **kwargs):
        if request.method == 'POST':
            form = CrushOrderForm(request.POST)
            if form.is_valid():
                new_data = {
                    'vintage': form.cleaned_data['vintage'],
                    'docket_number': form.cleaned_data['docket_number'],
                }
                docket = Docket.objects.get(docket_number=new_data["docket_number"])
                data = {"year": new_data["vintage"]}
                # docket.vintage = data["vintage"]
                # docket.save()
                # print(docket.vintage, docket.id, docket.docket_number)

                serializer = DocketSerializer(docket, data=data, partial=True)
                if serializer.is_valid():
                    test = serializer.save()
                else:
                    print("Serializer error:", serializer.errors)
                    return Response(None, status=status.HTTP_400_BAD_REQUEST)
                return redirect('reports-id', id=test.id)
        else:
            form = FruitIntakeForm()
        return render(request, 'crush_order.html', {'form': form, 'docket_number': "87"})

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
