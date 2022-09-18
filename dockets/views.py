import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from dockets.models import Docket
from dockets.serializers import DocketSerializer


class DocketViewSet(APIView):
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
        dockets = Docket.objects.all()
        serializer = DocketSerializer(dockets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
