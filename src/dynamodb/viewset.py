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

    def retrieve(self, request, *args, **kwargs):
        key_list = self.model_class().__convert_id_to_dynamo_key_list__(
            kwargs.get("pk")
        )
        res = Connector(self.model_class).get(key_list)
        return Response(res, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        key_list = self.model_class().__convert_id_to_dynamo_key_list__(
            kwargs.get("pk")
        )
        data = Connector(self.model_class).get(key_list)
        data.update({k: v for k, v in request.data.items() if v})
        instance = self.model_class().__from_dynamo__(data)
        Connector(self.model_class).update(instance)
        return Response(data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
