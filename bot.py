from binance import Client
import requests
import csv
import pandas as pd
from datetime import datetime as dt
import pandas_ta as ta
import time
import talib as fa

metin = 0
cuzdan = 0
toplamCoin = 0
alimSayisi = 0
satimSayisi = 0
kontrol = 0
def calistir():
    mesaj = "Kontrol"
    requests.post(url="############", data={"chat_id":"###########", "text": mesaj}).json()

    client = Client(None, None)

    def verileriGetir(sembol, periyot, baslangic,bitis):
        mumlar = client.get_historical_klines(sembol, periyot, baslangic,bitis)
        return mumlar

    def csvOlustur(sembol, mumlar):
        csvDosya = open(sembol+'.csv','w',newline='')
        yazici = csv.writer(csvDosya,delimiter=',')
        for mumVerileri in mumlar:
            yazici.writerow(mumVerileri)
        csvDosya.close()

    def veriCekmeveOlustuma():
        # coinler = ['BTCUSDT', 'FTMUSDT', 'MINAUSDT']                    #18 February 2022 FOR 1 HOUR OR 11 JULY 2021 //MA-100 23 AGUST 2021 1HOUR------ 1 JULY 2021 4 HOUR MA100
        # for coin in coinler:
        csvOlustur('FTMUSDT', verileriGetir('FTMUSDT', Client.KLINE_INTERVAL_15MINUTE, '17 July 2022', '27 October 2029'))
        print('FTMUSDT' + ' verileri getirildi')

    def zamanHesabi(timestamp):
        return dt.fromtimestamp(timestamp/1000)

    veriCekmeveOlustuma()

    def yaz(zama,cuz,co,al,sat):
        f = open("ac.txt","w")
        f.write(zama+"\n")
        f.write(cuz+"\n")
        f.write(co+"\n")
        f.write(al+"\n")
        f.write(sat)
        f.close()

    def oku():
        global metin
        global cuzdan
        global toplamCoin
        dosya = open("ac.txt","r")
        d = dosya.readlines()
        metin = int(d[0])
        cuzdan = float(d[1])
        toplamCoin = float(d[2])
        alimSayisi = int(d[3])
        satimSayisi = int(d[4])
        dosya.close()

    def alSat():
        global cuzdan
        global metin
        global toplamCoin
        global alimSayisi
        global satimSayisi
        global kontrol
        oku()
        okunacakCsv = 'FTMUSDT.csv'
        basliklar = ['open_time', 'open', 'high', 'low', 'close', 'vol', 'close_time', 'qav', 'nat', 'tbbbav', 'tbqav', 'ignore']
        df = pd.read_csv(okunacakCsv, names=basliklar)
        openp = df['open']
        close = df['close']
        high = df['high']
        low = df['low']
        acilisZamani = df['open_time']
        sma50 = fa.SMA(close, 10)
        sma200 = fa.SMA(close, 100)
        print('##################################')
        for i in range(len(close)):
            if pd.isna(sma50[i]) is False:
                if ((sma50[i-1] <= sma200[i-1] and sma50[i] >= sma200[i]) or (sma50[i-1] >= sma200[i-1] and sma50[i] <= sma200[i])) and cuzdan > 0:
                    # print(zamanHesabi(acilisZamani[i+1]), 'tarihinde', cuzdan/close[i], 'adet FTM alindi.')
                    kontrol = close[i]
                    zam = acilisZamani[i]
                    
                    if acilisZamani[i] > metin:
                        alimSayisi+=1
                        yaz(str(acilisZamani[i]),str(cuzdan),str(toplamCoin),str(alimSayisi),str(satimSayisi))
                        toplamCoin +=  cuzdan/openp[i]
                        mesaj = "----ALIŞ----\n\n{0} tarihinde {1} tutar ile {2} adet FTM alindi.\n\nİslem: {3}".format(zamanHesabi(acilisZamani[i]),cuzdan,toplamCoin,alimSayisi+satimSayisi)
                        requests.post(url="###########", data={"chat_id":"#########", "text": mesaj}).json()
                        cuzdan = 0
                        zam = metin
                        
                        



                if ((sma50[i-1] <= sma200[i-1] and sma50[i] >= sma200[i]) or (sma50[i-1] >= sma200[i-1] and sma50[i] <= sma200[i])) and zaman < acilisZamani[i]:
                    # print(zamanHesabi(acilisZamani[i+1]), 'tarihinde', toplamCoin, 'adet FTM satildi.')
                    # print(f"Bu iki islem sonucundaki cuzdan ederi: {cuzdan}\n")
                    # print('###################')
                    if acilisZamani[i] > metin:
                        satimSayisi+=1
                        yaz(str(acilisZamani[i]),str(cuzdan),str(toplamCoin),str(alimSayisi),str(satimSayisi))
                        fiyat = openp[i]*toplamCoin
                        cuzdan = fiyat
                        mesaj = "----SATIŞ----\n\n{0} tarihinde {1} adet FTM satildi.\n\nİşlem: {3}\n\nİslem sonucundaki cuzdan ederi: {2}\n".format(zamanHesabi(acilisZamani[i]),toplamCoin,cuzdan,alimSayisi+satimSayisi)
                        requests.post(url="################", data={"chat_id":"############", "text": mesaj}).json()
                        toplamCoin = 0
                        zam = metin    
        

    

    alSat()   

while True:
    calistir()
    time.sleep(900)