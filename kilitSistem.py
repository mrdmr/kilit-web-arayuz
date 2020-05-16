#!/usr/bin/env python3
# - *- coding: utf- 8 - *-
from istek import postData, getData, putData
from datetime import datetime
import pytz


server_url='http://34.94.80.140:8000'

# payload={'response' : '','reason' : ''}

def bisikletAl(u_id, istasyon, rfid):
    alabilir = True
    print(server_url+"/bisiklet/?u_id={}".format(str(u_id)))
    bisiklet = getData(server_url+"/bisiklet/?u_id={}".format(str(u_id)))
    if bisiklet:
        bisiklet=bisiklet[0]
        print("bisiklet = {}".format(bisiklet))
        if bisiklet['istasyon'] == str(istasyon) and bisiklet['u_id'] == str(u_id):
            if bisiklet['istasyonda'] == False:
                print("Bisiklet istasyonda değil!")
                payload={'response' : 'Hata' ,'msg' : 'Bisiklet istasyonda değil!' }
                alabilir = False

            if bisiklet['arizali'] == True:
                payload={'response' : 'Hata' , 'msg' : 'Bisiklet arızalı, başka bir bisiklet dene! ' }
                print("Bisiklet arızalı, başka bir bisiklet dene!")
                alabilir = False

            bisiklet_uid = bisiklet['u_id']
            bisiklet_sta = bisiklet['istasyon']
            bisiklet_id  = bisiklet['b_id']
            bisiklet_url = bisiklet['url']

            if alabilir == True:
                print("Alabilir = True")
                ogrenci = getData(server_url+"/ogrenci/?rfid={}".format(str(rfid)))
                if ogrenci:
                    ogrenci=ogrenci[0]
                    print("ogrenci = {}".format(ogrenci))
                    if ogrenci['rfid'] == rfid:
                        if ogrenci['yasakli'] == True:
                            print("Öğrencinin bisiklet alması yasaklanmış.")
                            payload={'response' : 'Hata','msg' : 'Öğrencinin bisiklet alması yasaklanmış.'}
                            alabilir = False

                        if int(ogrenci['ceza']) > 0:
                            print("Öğrenci {} gün bisiklet alamaz.".format(ogrenci['ceza']))
                            ceza="Öğrenci {} gün bisiklet alamaz.".format(ogrenci['ceza'])
                            payload={'response' : 'Hata','reason' : ceza}
                            alabilir = False

                        if ogrenci['bisikletiVar'] == True:
                            print("Öğrencide zaten bisiklet var!")
                            payload={'response' : 'Hata','reason' : 'Öğrencide zaten bisiklet var!'}
                            alabilir = False

                        ogrenci_no    = ogrenci['okul_no']
                        ogrenci_ad    = ogrenci['ad']
                        ogrenci_soyad = ogrenci['soyad']
                        ogrenci_rfid  = ogrenci['rfid']
                        ogrenci_url   = ogrenci['url']

                        if alabilir == True:
                            putData(bisiklet_url,
                                    {"u_id": bisiklet_uid,
                                    "istasyon": bisiklet_sta,
                                    "son_alan": ogrenci_no,
                                    "istasyonda": False})

                            postData(server_url+"/etkinlik/",
                                    {"ogrenci_no": ogrenci_no,
                                    "bisiklet_id": bisiklet_id})

                            print("bisikletAl "+server_url+"/etkinlik/",
                                   {"ogrenci_no": ogrenci_no,
                                    "bisiklet_id": bisiklet_id})

                            etkinlik = getData(server_url+"/etkinlik/")
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
                            payload={'response': 'Basarili' , 'reason' : 'Bisiklet alındı.' ,'etkinlik': etkinlik}
                else:
                    payload={'response' : 'Hata','reason' : 'Ogrenci bulunamadi.'}
                    print("Ogrenci bulunamadi.")
            else:
                #payload={'response' : 'Hata','reason' : 'Ogrenci bisiklet alamaz.'}
                print("Alabilir = False")
        else:
            payload={'response' : 'Hata','reason' : 'Bisiklet istasyonda değil.' }
            print("Bisiklet istasyonda değil.")
    else:
        payload={'response' : 'Hata','reason' : 'Bisiklet sistemde bulunamadı.' }
        print('Bisiklet sistemde bulunamadı.')

    return payload

def bisikletVer(u_id, istasyon, rfid):
    ogrenci = getData(server_url+"/ogrenci/?rfid={}".format(str(rfid)))
    print('bisikletVer ogrenci {}'.format(ogrenci))
    if ogrenci:
        ogrenci=ogrenci[0]
        if ogrenci['rfid'] == rfid:
            if ogrenci['bisikletiVar'] == False:
                payload={'response' : 'Hata','reason' : 'Bu öğrencide zaten bisiklet yok!'}
                print("Bu öğrencide zaten bisiklet yok!")

            ogrenci_no = ogrenci['okul_no']
            son_etkinlik = ogrenci['son_etkinlik']
            print('son etkinlik ' + son_etkinlik)
            etkinlik = getData(server_url+"/etkinlik/?b_id={}".format(str(son_etkinlik)))
            print('etkinlik: '.format(etkinlik))
            if etkinlik:
                etkinlik=etkinlik[0]
                print('bisikletVer etkinlik {}'.format(etkinlik))
                bisiklet_id = etkinlik['bisiklet_id']
                alinanTarih=etkinlik['alinanTarih']
                pst = pytz.timezone('Asia/Istanbul')
                now = pst.localize(datetime.now())
                print(now)
                tarih = now.strftime("%d/%m/%Y, %H:%M")
                print('now.strftime {}'.format(tarih))
                alinanT = datetime.strptime(alinanTarih, "%d/%m/%Y, %H:%M")
                verilenT = datetime.now()
                print('verilenT: {}'.format(verilenT))
                (gun,saat,dakika,saniye)=dhms_from_seconds(date_diff_in_seconds(verilenT,alinanT))
                print("%d gun, %d saat, %d dakika %d saniye" % (gun,saat,dakika,saniye))
                print('Gün {}'.format(gun))
                ceza='0'
                if gun>=1:
                    now = datetime.today()
                    ceza_tarihi = now + timedelta(days=1)
                    ceza = ceza_tarihi.strftime("%d/%m/%Y, %H:%M")
                    print(ceza)
                    payload={'response' : 'Hata','reason' : 'Geç teslim ettiginiz için 1 gün ceza aldınız.'}

                print(etkinlik['url'],
                        {"ogrenci_no": ogrenci_no,
                        "bisiklet_id": bisiklet_id,
                        "verilenTarih": tarih})

                #print(etkinlik['url']
                #        {"ogrenci_no": ogrenci_no,
                #        "bisiklet_id": bisiklet_id,
                #        "verilenTarih": tarih})

                putData(etkinlik['url'],
                        {"ogrenci_no": ogrenci_no,
                        "bisiklet_id": bisiklet_id,
                        "verilenTarih": tarih})
                            
                bisiklet = getData(server_url+"/bisiklet/?u_id={}".format(u_id))
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
                                   'son_etkinlik': son_etkinlik} )
                    putData(ogrenci['url'],
                                  {'okul_no': ogrenci_no,
                                   'ad': ogrenci['ad'],
                                   'soyad': ogrenci['soyad'],
                                   'rfid': ogrenci['rfid'],
                                    'ceza':ceza,
                                   'bisikletiVar': False,
                                   'son_etkinlik': son_etkinlik})
                    payload={'response' : 'Basarili','reason' : 'Bisiklet teslim edildi.'}
                else:
                    payload={'response' : 'Hata','reason' : 'Bisiklet sistemde bulunamadı.'}
                    print("Bisiklet bulunamadı.")
    return payload


def date_diff_in_seconds(dt2, dt1):
  timedelta = dt2 - dt1
  return timedelta.days * 24 * 3600 + timedelta.seconds

def dhms_from_seconds(seconds):
	minutes, seconds = divmod(seconds, 60)
	hours, minutes = divmod(minutes, 60)
	days, hours = divmod(hours, 24)
	return (days, hours, minutes, seconds)

