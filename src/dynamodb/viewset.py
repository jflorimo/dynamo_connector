from rest_framework import viewsets, status
from rest_framework.response import Response
from . import Connector


class DynamoViewset(viewsets.ModelViewSet):
    queryset = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_queryset(self):
        results = Connector(self.model_class).all()
        return [self.model_class().__from_dynamo__(x) for x in results]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        Connector(self.model_class).insert(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def retrieve(self, request, *args, **kwargs):
    #     print("RETRIEVE")
