#!/usr/bin/env python3
# - *- coding: utf- 8 - *-
from istek import postData, getData, putData
from datetime import datetime,timedelta

def istasyonEkle(ad, adres):
    postData("http://127.0.0.1:8000/istasyon/",
             {"ad": ad,
              "adres": adres})

def bisikletEkle(u_id, istasyon):
    postData("http://127.0.0.1:8000/bisiklet/",
             {"u_id": u_id,
              "istasyon": istasyon})

def bisikletAl(u_id, istasyon, rfid):
    alabilir = True
    print("http://127.0.0.1:8000/bisiklet/?u_id={}".format(str(u_id)))
    bisiklet = getData("http://127.0.0.1:8000/bisiklet/?u_id={}".format(str(u_id)))
    if bisiklet:
        bisiklet=bisiklet[0]
        print("bisiklet = {}".format(bisiklet))
        if bisiklet['istasyon'] == str(istasyon) and bisiklet['u_id'] == str(u_id):
            if bisiklet['istasyonda'] == False:
                print("Bisiklet istasyonda değil!")
                alabilir = False

            if bisiklet['arizali'] == True:
                print("Bisiklet arızalı, başka bir bisiklet dene!")
                alabilir = False

            bisiklet_uid = bisiklet['u_id']
            bisiklet_sta = bisiklet['istasyon']
            bisiklet_id = bisiklet['b_id']
            bisiklet_url = bisiklet['url']

            if alabilir == True:
                print("Alabilir = True")
                ogrenci = getData("http://127.0.0.1:8000/ogrenci/?rfid={}".format(str(rfid)))
                if ogrenci:
                    ogrenci=ogrenci[0]
                    print("ogrenci = {}".format(ogrenci))
                    if ogrenci['rfid'] == rfid:
                        if ogrenci['yasakli'] == True:
                            print("Öğrencinin bisiklet alması yasaklanmış.")
                            alabilir = False

                        if ogrenci['ceza'] != '-':
                            bugun = datetime.today()
                            ceza_tarihi = datetime.strptime(ogrenci['ceza'], "%d/%m/%Y, %H:%M")
                            (gun, saat, dakika, saniye) = dhms_from_seconds(date_diff_in_seconds(ceza_tarihi, bugun))
                            print("Cezalı olduğunuz için {} gün {} saat {} dakika bisiklet alamazsınız!".format( gun,saat, dakika))
                            alabilir = False

                        if ogrenci['bisikletiVar'] == True:
                            print("Öğrencide zaten bisiklet var!")
                            alabilir = False

                        ogrenci_no = ogrenci['okul_no']
                        ogrenci_ad = ogrenci['ad']
                        ogrenci_soyad = ogrenci['soyad']
                        ogrenci_rfid = ogrenci['rfid']
                        ogrenci_url = ogrenci['url']

                        if alabilir == True:
                            putData(bisiklet_url,
                                    {"u_id": bisiklet_uid,
                                    "istasyon": bisiklet_sta,
                                    "son_alan": ogrenci_no,
                                    "istasyonda": False})

                            postData("http://127.0.0.1:8000/etkinlik/",
                                    {"ogrenci_no": ogrenci_no,
                                    "bisiklet_id": bisiklet_id})

                            print("bisikletAl "+"http://127.0.0.1:8000/etkinlik/",
                                    {"ogrenci_no": ogrenci_no,
                                    "bisiklet_id": bisiklet_id})

                            etkinlik = getData("http://127.0.0.1:8000/etkinlik/")
                            etkinlik = etkinlik[len(etkinlik) - 1]
                            etkinlik = etkinlik['b_id']

                            print(putData(ogrenci_url,
                                        {'okul_no': ogrenci_no,
                                        'ad': ogrenci_ad,
                                        'soyad': ogrenci_soyad,
                                        'rfid': ogrenci_rfid,
                                        'bisikletiVar': True,
                                        'son_etkinlik': etkinlik}))
                            print('Bisiklet alındı.Etkinlik b_id: {}'.format(etkinlik))
                else:
                    print("Ögrenci bulunamadi.")
            else:
                print("Alabilir = False")
        else:
            print("Bisiklet istasyonda değil.")
    else:
        print('Bisiklet bulunamadı.')

def bisikletVer(u_id, istasyon, rfid):
    ogrenci = getData("http://127.0.0.1:8000/ogrenci/?rfid={}".format(str(rfid)))
    print('bisikletVer ogrenci {}'.format(ogrenci))
    if ogrenci:
        ogrenci=ogrenci[0]
        if ogrenci['rfid'] == rfid:
            if ogrenci['bisikletiVar'] == False:
                print("Bu öğrencide zaten bisiklet yok!")
            ogrenci_no = ogrenci['okul_no']
            son_etkinlik = ogrenci['son_etkinlik']
            print('son etkinlik ' +son_etkinlik)

            etkinlik = getData("http://127.0.0.1:8000/etkinlik/?b_id={}".format(str(son_etkinlik)))
            print('etkinlik: '.format(etkinlik))
            if etkinlik:
                etkinlik=etkinlik[0]
                print('bisikletVer etkinlik {}'.format(etkinlik))
                bisiklet_id = etkinlik['bisiklet_id']
                alinanTarih=etkinlik['alinanTarih']
                now = datetime.today()
                tarih = now.strftime("%d/%m/%Y, %H:%M")
                print('now.strftime {}'.format(tarih))
                alinanT = datetime.strptime(alinanTarih, "%d/%m/%Y, %H:%M")
                verilenT = datetime.today()
                print('verilenT: {}'.format(verilenT))
                (gun,saat,dakika,saniye)=dhms_from_seconds(date_diff_in_seconds(verilenT, alinanT))
                print("%d gun, %d saat, %d dakika %d saniye" % (gun,saat,dakika,saniye))
                print('Gün {}'.format(gun))
                ceza='-'
                if gun>1:
                    print('Ceza aldınız.')
                    now = datetime.today()
                    ceza_tarihi = now + timedelta(days=1)
                    ceza = ceza_tarihi.strftime("%d/%m/%Y, %H:%M")
                    print(ceza)

                print(etkinlik['url'],
                        {"ogrenci_no": ogrenci_no,
                        "bisiklet_id": bisiklet_id,
                        "verilenTarih": tarih})

                putData(etkinlik['url'],
                        {"ogrenci_no": ogrenci_no,
                        "bisiklet_id": bisiklet_id,
                        "verilenTarih": tarih})
                bisiklet = getData("http://127.0.0.1:8000/bisiklet/?u_id={}".format(u_id))
                if bisiklet:
                    bisiklet=bisiklet[0]
                    print('bisikletVer bisiklet {}'.format(bisiklet))

                    putData(bisiklet['url'],
                            {"u_id": u_id,
                            "istasyon": istasyon,
                            "son_alan": ogrenci_no,
                            "istasyonda": True})

                    print("putdata "+ogrenci['url'],
                                  {'okul_no': ogrenci_no,
                                   'ad': ogrenci['ad'],
                                   'soyad': ogrenci['soyad'],
                                   'rfid': ogrenci['rfid'],
                                   'bisikletiVar': False,
                                   'son_etkinlik': son_etkinlik}
                          )
                    putData(ogrenci['url'],
                                  {'okul_no': ogrenci_no,
                                   'ad': ogrenci['ad'],
                                   'soyad': ogrenci['soyad'],
                                   'rfid': ogrenci['rfid'],
                                    'ceza':ceza,
                                   'bisikletiVar': False,
                                   'son_etkinlik': son_etkinlik})
                else:
                    print("Bisiklet bulunamadı.")

def date_diff_in_seconds(dt2, dt1):
    timedelta = dt2 - dt1
    return timedelta.days * 24 * 3600 + timedelta.seconds

def dhms_from_seconds(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return (days, hours, minutes, seconds)

