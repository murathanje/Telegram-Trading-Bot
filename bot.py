from binance import Client
import requests
import csv
import pandas as pd
from datetime import datetime as dt
import pandas_ta as ta
import time


metin = 0
cuzdan = 0
toplamCoin = 0
kontrol = 0
zam = 0
islem = 0
def calistir():

    mesaj = "Kontrol"
    requests.post(url="https://api.telegram.org/bot5430197913:AAGAuZLGp0_iJIvbC3z4qZQ_i6Up4s1wtp4/sendMessage", data={"chat_id":"615278769", "text": mesaj}).json()


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
        csvOlustur('FTMUSDT', verileriGetir('FTMUSDT', Client.KLINE_INTERVAL_15MINUTE, '17 September 2022', '24 July 2029'))
        print('FTMUSDT' + ' verileri getirildi')

    def zamanHesabi(timestamp):
        return dt.fromtimestamp(timestamp/1000)

    veriCekmeveOlustuma()

    def yaz(zama,cuz,co,t_islem):
        f = open("ac.txt","w")
        f.write(zama+"\n")
        f.write(cuz+"\n")
        f.write(co+"\n")
        f.write(t_islem+"\n")
        f.close()

    def oku():
        global metin
        global cuzdan
        global toplamCoin
        global islem
        dosya = open("ac.txt","r")
        d = dosya.readlines()
        metin = int(d[0])
        cuzdan = float(d[1])
        toplamCoin = float(d[2])
        islem = int(d[3])
        dosya.close()

    def alSat():
        global cuzdan
        global metin
        global toplamCoin
        global islem
        global kontrol
        global zam
        oku()
        okunacakCsv = 'FTMUSDT.csv'
        basliklar = ['open_time', 'open', 'high', 'low', 'close', 'vol', 'close_time', 'qav', 'nat', 'tbbbav', 'tbqav', 'ignore']
        df = pd.read_csv(okunacakCsv, names=basliklar)
        openp = df['open']
        close = df['close']
        high = df['high']
        low = df['low']
        acilisZamani = df['open_time']
        sma50 = ta.sma(close, 10)
        sma200 = ta.sma(close, 100)
        print('##################################')
        for i in range(len(close)):
            if pd.isna(sma50[i]) is False:
                if ((sma50[i-1] <= sma200[i-1] and sma50[i] >= sma200[i]) or (sma50[i-1] >= sma200[i-1] and sma50[i] <= sma200[i])) and cuzdan > 0:
                    # print(zamanHesabi(acilisZamani[i+1]), 'tarihinde', cuzdan/close[i], 'adet FTM alindi.')
                    kontrol = close[i]
                    zam = acilisZamani[i]

                    if acilisZamani[i] > metin:
                        islem+=1
                        toplamCoin +=  cuzdan/close[i]
                        mesaj = "----ALIŞ----\n\nTarih: {0}\n\nAlış Fiyatı fiyatı: {4}\n\nCuzdan: {1}\n\nToplam adet: {2}\n\nİslem: {3}".format(zamanHesabi(acilisZamani[i]),cuzdan,toplamCoin,islem,close[i])
                        requests.post(url="https://api.telegram.org/bot5430197913:AAGAuZLGp0_iJIvbC3z4qZQ_i6Up4s1wtp4/sendMessage", data={"chat_id":"615278769", "text": mesaj}).json()
                        cuzdan = 0
                        yaz(str(acilisZamani[i]),str(cuzdan),str(toplamCoin),str(islem))




                if ((sma50[i-1] <= sma200[i-1] and sma50[i] >= sma200[i]) or (sma50[i-1] >= sma200[i-1] and sma50[i] <= sma200[i])) and zam < acilisZamani[i]:
                    # print(zamanHesabi(acilisZamani[i+1]), 'tarihinde', toplamCoin, 'adet FTM satildi.')
                    # print(f"Bu iki islem sonucundaki cuzdan ederi: {cuzdan}\n")
                    # print('###################')
                    if acilisZamani[i] > metin:
                        islem+=1
                        fiyat = close[i]*toplamCoin
                        cuzdan = fiyat
                        mesaj = "----SATIŞ----\n\nTarih: {0}\n\nSatış fiyatı: {4}\n\nAdet: {1}\n\nCuzdan: {2}\n\nİşlem: {3}".format(zamanHesabi(acilisZamani[i]),toplamCoin,cuzdan,islem,close[i])
                        requests.post(url="https://api.telegram.org/bot5430197913:AAGAuZLGp0_iJIvbC3z4qZQ_i6Up4s1wtp4/sendMessage", data={"chat_id":"615278769", "text": mesaj}).json()
                        toplamCoin = 0
                        yaz(str(acilisZamani[i]),str(cuzdan),str(toplamCoin),str(islem))





    alSat()

while True:
    calistir()
    time.sleep(2)
