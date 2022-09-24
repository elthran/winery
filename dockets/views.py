import json

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer

from dockets.models import Docket
from dockets.serializers import DocketSerializer


class FruitIntakeViewSet(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def get(request, *args, **kwargs):
        """
        Retrieve the prepared dataset.

        :return: (JSON) The incident reports and a 200 status on success
        """
        renderer_classes = [TemplateHTMLRenderer]
        template_name = 'fruit_intake.html'
        dockets = Docket.objects.all()
        serializer = DocketSerializer(dockets, many=True)
        # return Response({'profiles': dockets})
        # return Response(serializer.data, status=status.HTTP_200_OK)
        return render(request, template_name, {'data': serializer.data})
        # return Response({'serializer': serializer, 'profile': dockets})

    @staticmethod
    def post(request, *args, **kwargs):
        data = {
            'varietal': request.data.get('varietal'),
            'vineyard': request.data.get('vineyard'),
            'block': request.data.get('block'),
        }
        data['docket_number'] = data['varietal'] + data['vineyard'] + data['block']
        serializer = DocketSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request, *args, **kwargs):
        return Response(None, status=status.HTTP_501_NOT_IMPLEMENTED)

    @staticmethod
    def delete(request, *args, **kwargs):
        return Response(None, status=status.HTTP_501_NOT_IMPLEMENTED)


class CrushOrderViewSet(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def get(request, *args, **kwargs):
        """
        Retrieve the prepared dataset.

        :return: (JSON) The incident reports and a 200 status on success
        """
        renderer_classes = [TemplateHTMLRenderer]
        template_name = 'crush_order.html'
        dockets = Docket.objects.all()
        serializer = DocketSerializer(dockets, many=True)
        # return Response({'profiles': dockets})
        # return Response(serializer.data, status=status.HTTP_200_OK)
        return render(request, template_name, {'data': serializer.data})
        # return Response({'serializer': serializer, 'profile': dockets})

    @staticmethod
    def post(request, *args, **kwargs):
        data = {
            'varietal': request.data.get('varietal'),
            'vineyard': request.data.get('vineyard'),
            'block': request.data.get('block'),
        }
        data['docket_number'] = data['varietal'] + data['vineyard'] + data['block']
        serializer = DocketSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request, *args, **kwargs):
        return Response(None, status=status.HTTP_501_NOT_IMPLEMENTED)

    @staticmethod
    def delete(request, *args, **kwargs):
        return Response(None, status=status.HTTP_501_NOT_IMPLEMENTED)
