from django.db import models
import hashlib
from datetime import datetime

class IstasyonModel(models.Model):
    # Istasyon adı
    ad    = models.CharField(max_length=255)
    # Istasyonun adresi
    adres = models.TextField()

    def save(self, *args, **kwargs):
        super(IstasyonModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.ad

class OgrenciModel(models.Model):
    # Okul numarası, 10 haneli
    okul_no      = models.CharField(max_length=12)
    ad           = models.CharField(max_length=255)
    soyad        = models.CharField(max_length=255)
    # rfid kart numarası
    rfid         = models.CharField(max_length=255)
    # Ceza kaç gün
    ceza         = models.CharField(max_length=64, default="0")
    # Sistemde yasaklı olma durumu
    yasakli      = models.BooleanField(default=False)
    bisikletiVar = models.BooleanField(default=False)
    son_etkinlik = models.CharField(max_length=8, default="00000000")
    
    def save(self, *args, **kwargs):
        super(OgrenciModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.okul_no

# Bisiklet Modeli
class BisikletModel(models.Model):
    # Her bisiklet için benzersiz id
    b_id        = models.CharField(max_length=255, blank=True, editable=False)
    # Istasyon üstündeki id'si
    u_id        = models.CharField(max_length=255)
    # Kayıtlı olduğu istasyon
    istasyon    = models.CharField(max_length=255)
    # Arıza durumu
    arizali     = models.BooleanField(default=False)
    # Son teslim alan/eden öğrenci
    son_alan    = models.CharField(max_length=12, blank=True, default="00000000000")
    # Bisikletin sisteme ilk giriş tarihi
    giris_tarih = models.CharField(max_length=255, blank=True, editable=False)
    # istasyon
    istasyonda  = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Tarihi çektik
        now              = datetime.today()
        tarih            = now.strftime("%d/%m/%Y, %H:%M")
        self.giris_tarih = tarih

        # sha256 kodlamasıyla şifreledik, ve ilk 8 hanesini aldık
        hashObj   = hashlib.sha512("{}<+>{}".format(self.u_id,tarih).encode("utf8"))
        hashObj   = hashObj.hexdigest()
        hashObj   = str(hashObj)[0:8]
        # Benzersiz id'mizi atadık
        self.b_id = hashObj
        super(BisikletModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.b_id

class EtkinlikModel(models.Model):
    # Benzersiz id
    b_id         = models.CharField(max_length=255, blank=True, editable=False)
    ogrenci_no   = models.CharField(max_length=12)
    bisiklet_id  = models.CharField(max_length=8)
    alinanTarih  = models.CharField(max_length=255, blank=True)
    verilenTarih = models.CharField(max_length=255, default="-")

    def save(self, *args, **kwargs):
        # Tarihi çektik
        now              = datetime.today()
        tarih            = now.strftime("%d/%m/%Y, %H:%M")
        self.alinanTarih = tarih

        # sha256 kodlamasıyla şifreledik, ve ilk 8 hanesini aldık
        hashObj   = hashlib.sha512("{}".format(tarih).encode("utf8"))
        hashObj   = hashObj.hexdigest()
        hashObj   = str(hashObj)[0:8]
        # Benzersiz id'mizi atadık
        self.b_id = hashObj
        super(EtkinlikModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.b_id
