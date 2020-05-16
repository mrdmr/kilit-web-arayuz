from rest_framework import serializers
from api.models import IstasyonModel, OgrenciModel, BisikletModel, EtkinlikModel

class IstasyonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model  = IstasyonModel
        fields = ('url','ad', 'adres')

class OgrenciSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model  = OgrenciModel
        fields = ('url','okul_no', 'ad', 'soyad', 'rfid', 'ceza', 'yasakli', 'bisikletiVar', 'son_etkinlik')

class BisikletSerializer(serializers.ModelSerializer):
    class Meta:
        model  = BisikletModel
        fields = ('url','b_id', 'u_id', 'istasyon', 'arizali', 'son_alan', 'giris_tarih', 'istasyonda')

class EtkinlikSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model  = EtkinlikModel
        fields = ('url','b_id', 'ogrenci_no', 'bisiklet_id', 'alinanTarih', 'verilenTarih')
