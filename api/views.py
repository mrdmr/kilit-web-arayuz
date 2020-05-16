from rest_framework import viewsets
from api.models import IstasyonModel, OgrenciModel, BisikletModel, EtkinlikModel
from api.serializers import IstasyonSerializer, OgrenciSerializer, BisikletSerializer, EtkinlikSerializer

class IstasyonViewSet(viewsets.ModelViewSet):
    queryset         = IstasyonModel.objects.all()
    serializer_class = IstasyonSerializer

class OgrenciViewSet(viewsets.ModelViewSet):
    queryset = OgrenciModel.objects.all()
    serializer_class = OgrenciSerializer

    def get_queryset(self):
        queryset = OgrenciModel.objects.all()
        _rfid = self.request.query_params.get('rfid', None)
        if _rfid is not None:
            queryset = queryset.filter(rfid=_rfid)
        return  queryset

class BisikletViewSet(viewsets.ModelViewSet):
    queryset = BisikletModel.objects.all()
    serializer_class = BisikletSerializer
    def get_queryset(self):
        queryset = BisikletModel.objects.all()
        _u_id = self.request.query_params.get('u_id', None)
        if _u_id is not None:
            queryset = queryset.filter(u_id=_u_id)
        return queryset

class EtkinlikViewSet(viewsets.ModelViewSet):
    queryset = EtkinlikModel.objects.all()
    serializer_class = EtkinlikSerializer
    def get_queryset(self):
        queryset = EtkinlikModel.objects.all()
        _b_id = self.request.query_params.get('b_id', None)
        if _b_id is not None:
            queryset = queryset.filter(b_id=_b_id)
        return queryset