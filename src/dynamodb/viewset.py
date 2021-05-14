from rest_framework import viewsets, status
from rest_framework.response import Response


class DynamoViewset(viewsets.ModelViewSet):
    queryset = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_queryset(self):
        results = self.model_class.dynamo.all()
        return [self.model_class().__from_dynamo__(x) for x in results]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        self.model_class.dynamo.insert(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        key_list = self.model_class().__convert_id_to_dynamo_key_list__(
            kwargs.get("pk")
        )
        res = self.model_class.dynamo.get(key_list)
        if res:
            return Response(res, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        key_list = self.model_class().__convert_id_to_dynamo_key_list__(
            kwargs.get("pk")
        )
        data = self.model_class.dynamo.get(key_list)
        data.update({k: v for k, v in request.data.items() if v})
        instance = self.model_class().__from_dynamo__(data)
        self.model_class.dynamo.update(instance)
        return Response(data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        key_list = self.model_class().__convert_id_to_dynamo_key_list__(
            kwargs.get("pk")
        )
        self.model_class.dynamo.delete(key_list)
        return Response(status=status.HTTP_204_NO_CONTENT)
