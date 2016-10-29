from django.shortcuts import render
from rest_framework import generics, viewsets
from authapi.serializers import GenericSerializer

def GenericList(for_model, model_serializer=None):
    if not model_serializer:
        model_serializer = GenericSerializer(for_model)

    class GenericModelListCreateView(generics.ListCreateAPIView):
        queryset = for_model.objects.all()
        serializer_class = model_serializer

        def get_view_name(self):
            return self.settings.VIEW_NAME_FUNCTION(for_model, getattr(self, 'suffix', None))

    return GenericModelListCreateView

def GenericModel(for_model, model_serializer=None):
    if not model_serializer:
        model_serializer = GenericSerializer(for_model)

    class GenericModelView(generics.RetrieveUpdateDestroyAPIView):
        queryset = for_model.objects.all()
        serializer_class = model_serializer

        def get_view_name(self):
            return self.settings.VIEW_NAME_FUNCTION(for_model, getattr(self, 'suffix', None))

    return GenericModelView

def GenericModelViewSet(model, serializers={}):
    if not serializers.get('default', None):
        serializers['default'] = GenericSerializer(model)

    class GenericViewSet(viewsets.ModelViewSet):
        queryset = model.objects.all()

        def get_serializer_class(self):
            return serializers.get(self.action, serializers.get('default'))

        def get_view_name(self):
            return self.settings.VIEW_NAME_FUNCTION(model, getattr(self, 'suffix', None))

    return GenericViewSet