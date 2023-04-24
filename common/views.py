from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, \
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED, HTTP_200_OK
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response


def return_serialized_data_or_error_response(_object, serializer_class, response_code) -> Response:
    try:
        return Response(data=serializer_class(_object).data, status=response_code)
    except Exception as exception:
        return Response(data=dict(error=str(exception)), status=HTTP_500_INTERNAL_SERVER_ERROR)


def extract_data_with_validation(request, fields: dict) -> dict or Exception:
    for i in request.data:
        if fields.get(i) is None:
            return Exception(f'{i} is not an attribute for the model')
        if request.data.get(i) is None and fields[i]['required']:
            return Exception(f'{i} is required')
    return request.data


def extract_get_data(request):
    output = {}
    for i in request.GET:
        try:
            output[i] = int(request.GET.get(i)) if request.GET.get(i).find('.') == -1 else float(request.GET.get(i))
        except Exception as exception:
            if request.GET.get(i) == 'true' or request.GET.get(i) == 'false':
                output[i] = request.GET.get(i) == 'true'
            else:
                output[i] = request.GET.get(i)
    return output


def extract_serialized_objects_response(_objects, serializer_class) -> Response:
    output = []
    if _objects:
        try:
            for i in _objects:
                output.append(serializer_class(i).data)
        except Exception as exception:
            return Response(data={'error': str(exception)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data=output, status=HTTP_200_OK)


class ViewSet(ModelViewSet):
    def __init__(self, serializer_class, service, **kwargs):
        super().__init__(**kwargs)
        self.serializer_class = serializer_class
        self.service = service
        self.fields = self.service.fields

    def list(self, request, *args, **kwargs):
        _objects = self.service.filter_by(
            extract_get_data(request=request)) if request.GET is not None else self.service.list()
        return extract_serialized_objects_response(_objects, self.serializer_class)

    def create(self, request, *args, **kwargs):
        data = {}
        for i in request.data:
            if self.fields.get(i) is None:
                return Response(data={'error': f'{i} is not an attribute for the model'}, status=HTTP_400_BAD_REQUEST)
            if request.data.get(i) is None and self.fields[i]['required']:
                return Response(data={'error': f'{i} is required'}, status=HTTP_400_BAD_REQUEST)
            data[i] = request.data.get(i)
        for i in self.fields:
            if self.fields[i].get('unique') is True:
                try:
                    filter = {i: data[i]}
                    self.service.repository.model.objects.get(**filter)
                    return Response(data={'message': f'{i} must be unique to each {self.service.repository.model.__name__}'}, status=HTTP_400_BAD_REQUEST)
                except self.service.repository.model.DoesNotExist:
                    pass
        _object = self.service.create(data)
        if isinstance(_object, Exception):
            return Response(data={"error": str(_object)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        return return_serialized_data_or_error_response(_object=_object, serializer_class=self.serializer_class,
                                                        response_code=HTTP_201_CREATED)

    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            data = self.service.retrieve(pk=pk)
        except  self.service.repository.model.DoesNotExist:
            return Response(data={'error': 'object not found'}, status=HTTP_404_NOT_FOUND)
        return return_serialized_data_or_error_response(_object=data, serializer_class=self.serializer_class,
                                                        response_code=HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        if pk is None:
            return Response(data={'error': 'id must not be null'}, status=HTTP_400_BAD_REQUEST)
        if self.service.retrieve(pk=pk) is None:
            return Response(data={'error': 'object not found'}, status=HTTP_404_NOT_FOUND)
        return return_serialized_data_or_error_response(_object=self.service.put(pk=pk, data=request.data),
                                                        serializer_class=self.serializer_class,
                                                        response_code=HTTP_201_CREATED)

    def destroy(self, request, pk=None, *args, **kwargs):
        if pk is None:
            return Response(data={'error': 'id must not be null'}, status=HTTP_400_BAD_REQUEST)
        deleted = self.service.delete(pk)
        if isinstance(deleted, Exception):
            return Response(data={'error': str(deleted)}, status=HTTP_404_NOT_FOUND)
        return Response(status=HTTP_204_NO_CONTENT)

    @classmethod
    def get_urls(cls):
        return cls.as_view({'get': 'list', 'post': 'create'}), cls.as_view(
            {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})
