from apps.models.fruit_intakes import FruitIntake
from apps.views.base import BaseView


class ReportsViewSet(BaseView):
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
        dockets = Docket.objects.all()
        print("Dockets:", dockets)
        fruit_intakes = FruitIntake.objects.first()
        print(fruit_intakes.docket)
        print("FruitIntake:", fruit_intakes)
        crush_orders = CrushOrder.objects.all()
        print("CrushOrder:", crush_orders)
        return

    @staticmethod
    def post(request, id=None, *args, **kwargs):
        return Response(None, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request, id, *args, **kwargs):
        return Response(None, status=status.HTTP_501_NOT_IMPLEMENTED)

    @staticmethod
    def delete(request, id, *args, **kwargs):
        return Response(None, status=status.HTTP_501_NOT_IMPLEMENTED)
