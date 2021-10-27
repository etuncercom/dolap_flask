import requests, time
from flask import Flask, render_template, request, url_for, session, redirect, abort
from flaskthreads import AppContextThread
import mysql.connector

app = Flask(__name__)
app.secret_key = b'u\x99;9}\xd73+\xfc\x1b-N\xdf\x07i1'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="dolap"
)

cursor = db.cursor(dictionary=True)

# app.jinja_env.globals.update(urunlerimi_getir=urunlerimi_getir)

url_list = {
    'kayit_url': 'https://api.dolap.com/member/',
    'dolap': 'https://api.dolap.com/member/closet',
    'followers_url': 'https://api.dolap.com/member/followers/',
    'followed_url': 'https://api.dolap.com/member/followedby/',
    'folllow_url': 'https://api.dolap.com/member/follow/',
    'unfolllow_url': 'https://api.dolap.com/member/unfollow/',
    'like_url': 'https://api.dolap.com/product/like/',
    'unlike_url': 'https://api.dolap.com/product/unlike/',
    'profil': 'https://dolap.com/profil/',
    'profil_oner': 'https://api.dolap.com/share/closet',
    'one_cikar': 'https://api-gateway.dolap.com/boost/product/',
    'one_cikar_eski': 'https://api.dolap.com/product/boost/',
    'urun_sil': 'https://api.dolap.com/product/close',
    'k_urun_ara': 'https://api.dolap.com/search',
    'urun_yorum': 'https://api.dolap.com/product/comment'
}

atoken = '10a5de2f-e2cc-40ff-b5f0-bcbf7aeeb915fc9540df-67da-4694-be52-9fa3bf53b3f0'

get_headers = {
    'Host': 'api.dolap.com',
    'Accept': '*/*',
    'X-Epoch-Seconds': '1633532488',
    'X-Signature': '5cab951838fadd0cfe570febf21b1a04aa71bff90faafc47e1d3a6b730d3da493f43d76a26fb4dd6c79930d145e5bfa8762466d9cc9ab983e5eb0872f7b8d1c0',
    'AppVersion': '253',
    'Accept-Language': 'tr-tr',
    'Accept-Encoding': 'gzip, deflate',
    'CategoryGroup': 'WOMAN',
    'Access-Token': atoken,
    'User-Agent': 'dolap/2 CFNetwork/1240.0.4 Darwin/20.6.0',
    'Connection': 'close',
    'AppPlatform': 'ios'
}

post_headers_one_cikar = {
    'Host': 'api-gateway.dolap.com',
    'Accept': '*/*',
    'X-Epoch-Seconds': '1633532488',
    'X-Signature': '5cab951838fadd0cfe570febf21b1a04aa71bff90faafc47e1d3a6b730d3da493f43d76a26fb4dd6c79930d145e5bfa8762466d9cc9ab983e5eb0872f7b8d1c0',
    'AppVersion': '253',
    'Accept-Language': 'tr-tr',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/json',
    'Content-Length': '46',
    'Access-Token': atoken,
    'User-Agent': 'dolap/2 CFNetwork/1240.0.4 Darwin/20.6.0',
    'Connection': 'close',
    'AppPlatform': 'ios'
}

post_headers = {
    'Host': 'api.dolap.com',
    'Accept': '*/*',
    'X-Epoch-Seconds': '1633532488',
    'X-Signature': '5cab951838fadd0cfe570febf21b1a04aa71bff90faafc47e1d3a6b730d3da493f43d76a26fb4dd6c79930d145e5bfa8762466d9cc9ab983e5eb0872f7b8d1c0',
    'AppVersion': '253',
    'Accept-Language': 'tr-tr',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/json',
    'Content-Length': '46',
    'Access-Token': atoken,
    'User-Agent': 'dolap/2 CFNetwork/1240.0.4 Darwin/20.6.0',
    'Connection': 'close',
    'AppPlatform': 'ios'
}

put_headers = {
    'Host': 'api.dolap.com',
    'Accept': '*/*',
    'X-Epoch-Seconds': str(int(time.time())),
    'X-Signature': '5cab951838fadd0cfe570febf21b1a04aa71bff90faafc47e1d3a6b730d3da493f43d76a26fb4dd6c79930d145e5bfa8762466d9cc9ab983e5eb0872f7b8d1c0',
    'AppVersion': '253',
    'Accept-Language': 'tr-tr',
    'Accept-Encoding': 'gzip, deflate',
    'CategoryGroup': 'WOMAN',
    'Content-Type': 'application/json',
    'Content-Length': '234',
    'Access-Token': '',
    'User-Agent': 'dolap/2 CFNetwork/1240.0.4 Darwin/20.6.0',
    'Connection': 'close',
    'AppPlatform': 'ios',
}
def kucuk_yap(data):
    return str(data).strip().lower()

def nick_to_id(nickname):
    from lxml import html

    r = requests.get(url_list['profil'] + nickname)
    if r.status_code != 200:
        print('boyle bir kullanici yok: ' + str(r.status_code))
    else:
        html = html.fromstring(r.content)
        return str(html.xpath('//@data-member-id')[0])

def id_bul(kadi):
    sql_id = "select ID from kullanicilar where kadi=%s"
    cursor.execute(sql_id, (kadi,))
    sonuc = cursor.fetchone()
    return sonuc['ID']

def tum_hesaplar(kadi):
    kid = id_bul(kadi)
    hsql = "select * from hesaplar where kullanici_id = %s"
    cursor.execute(hsql, (int(kid),))
    hesaplar = cursor.fetchall()
    return hesaplar

def giris_yap(kadi, sifre):
    data = '{{"username":"{kadi}","password":"{sifre}","memberCookie":"43654195-E337-4BEA-B35C-59ECF9B97F58","advertisingId":"00000000-0000-0000-0000-000000000000"}}'.format(kadi=kadi, sifre=sifre)

    response = requests.post('https://api.dolap.com/member/login/', headers=put_headers, data=data)
    # print(response.text)
    sonuc = response.json()
    if response.status_code == 200:
        return str(sonuc['accessToken'])
    else:
        return "hata"

def profil_getir(hesap):
    hesap_id = nick_to_id(hesap)
    data = '{{"memberId":{hesap_id}}}'.format(hesap_id=hesap_id)
    print(data)
    print("hesap bilgileri getiriliyor...")

    r = requests.post(url_list['dolap'], headers=post_headers, data=data)
    sonuc = r.json()

    bilgiler = {
        "id": sonuc['member']['id'],
        "takip_eden": sonuc['followerCount'],
        "takip_ettigi": sonuc['followeeCount']
        }
    return bilgiler


def takip_et(t_hesap, atoken, page=0, zaman=0):
    print('Kullanici ID aliniyor...')
    user_id = nick_to_id(t_hesap)
    print('Kullanici ID Alindi.')
    get_headers['Access-Token'] = atoken
    takip_edilenler = []
    page = page
    while True:
        params = (
            ('page', page),
        )
        if page < 4:
            try:
                r = requests.get(url_list['followers_url'] + user_id, headers=get_headers, params=params)

                if r.status_code != 200:
                    print('sunucu farklı cevap veriyor status code: ' + str(r.status_code))
                    break
                else:
                    sonuc = r.json()
                    toplam_dizi = len(sonuc)

                    if toplam_dizi <= 0:
                        break
                    else:
                        for i in range(toplam_dizi):
                            f_id = str(sonuc[i]['id'])
                            f_nick = str(sonuc[i]['nickname'])
                            # print(folllow_url+f_id)
                            try:
                                rq = requests.post(url_list['folllow_url'] + f_id, headers=get_headers)
                                if rq.status_code == 200:
                                    print(f_nick + ' adli kullanici takip edildi.')
                                    takip_edilenler.append(f_nick + ' adlı kullanıcı takip edildi.')
                                    time.sleep(zaman)
                                else:
                                    print('sunucu farklı cevap veriyor status code: ' + str(rq.text))
                                    break
                            except requests.exceptions.HTTPError as errh:
                                print("Http Error:", errh)
                            except requests.exceptions.ConnectionError as errc:
                                print("Error Connecting:", errc)
                            except requests.exceptions.Timeout as errt:
                                print("Timeout Error:", errt)
                            except requests.exceptions.RequestException as err:
                                print("OOps: Something Else", err)
                    page += 1
                    print('--- Sayfa ' + str(page) + ' ---')
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
            time.sleep(5)
        else:
            print("Tebrikler, toplam 100 kişiyi takip ettiniz.")
            break


def takip_cikar(t_hesap, atoken, page=0, zaman=0):
    print('Kullanici ID aliniyor...')
    user_id = nick_to_id(t_hesap)
    print('Kullanici ID Alindi.')
    get_headers['Access-Token'] = atoken
    page = page
    while True:
        params = (
            ('page', page),
        )
        if page < 300:
            try:
                r = requests.get(url_list['followed_url'] + user_id, headers=get_headers, params=params)

                if r.status_code != 200:
                    print('sunucu farklı cevap veriyor status code: ' + str(r.status_code))
                    break
                else:
                    sonuc = r.json()
                    toplam_dizi = len(sonuc)

                    if toplam_dizi <= 0:
                        break
                    else:
                        for i in range(toplam_dizi):
                            f_id = str(sonuc[i]['id'])
                            f_nick = str(sonuc[i]['nickname'])
                            # print(folllow_url+f_id)
                            try:
                                rq = requests.post(url_list['unfolllow_url'] + f_id, headers=get_headers)
                                if rq.status_code == 200:
                                    print(f_nick + ' adli kullanici takipten cikarildi.')
                                    time.sleep(zaman)
                                else:
                                    print('sunucu farklı cevap veriyor status code: ' + str(rq.text))
                                    break
                            except requests.exceptions.HTTPError as errh:
                                print("Http Error:", errh)
                            except requests.exceptions.ConnectionError as errc:
                                print("Error Connecting:", errc)
                            except requests.exceptions.Timeout as errt:
                                print("Timeout Error:", errt)
                            except requests.exceptions.RequestException as err:
                                print("OOps: Something Else", err)
                    page += 1
                    print('--- Sayfa ' + str(page) + ' ---')
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
        else:
            print("Tebrikler! Tüm takipçilerinizi çıkardınız.")
            break

def urunlerimi_getir(hesap, atoken):
    print('Kullanici ID alınıyor...')
    user_id = nick_to_id(hesap)
    print('Kullanici ID Alindi.')
    page = 0
    urunler = []
    while True:
        data = '{{"clearFilter":false,"showSoldItems":false,"sortField":"ID","page": {page},"ascending":false,"mySizeSelection":false,"ownerId": {user_id},"aggregation":false}}'.format(
            page=page, user_id=user_id)
        post_headers['Access-Token'] = atoken
        r = requests.post(url_list['k_urun_ara'], headers=post_headers, data=data)
        print(hesap + " ait ürünler listenleniyor...")
        sonuc = r.json()
        toplam = len(sonuc["products"])
        if toplam <= 0:
            break
        else:
            print(str(toplam) + " adet ürün listelendi")
            for x in range(toplam):
                urunler.append(
                    {
                        "id": sonuc["products"][x]["id"],
                        "baslik": sonuc["products"][x]["title"],
                        "fiyat": sonuc["products"][x]["price"],
                        "foto": sonuc["products"][x]["thumbnailImage"]["path"],
                        "begeni": sonuc["products"][x]["likeCount"],
                        "yorum": sonuc["products"][x]["commentCount"]
                    }
                )
        page += 1
    print('toplam ' + str(len(urunler)) +' adet ürün listelendi')
    return (urunler)


def eski_urun_one_cikar(urun_id: int, atoken):
    print(str(urun_id) + " nolu ürün id alındı")
    print("istek gönderiliyor...")
    get_headers['Access-Token'] = atoken
    r = requests.get(url_list['one_cikar'] + urun_id, headers=get_headers_one_cikar)
    print("istek gönderildi.")
    if r.status_code == 200:
        print("istek sonuc başarılı.")
        mesaj = 'ok'
    else:
        sonuc = r.json()
        mesaj = sonuc['message']
        print(sonuc['message'])
    return mesaj

def urun_one_cikar(urun_id: int, atoken):
    print(str(urun_id) + " nolu ürün id alındı")
    print("istek gönderiliyor...")
    data = '{}'
    post_headers_one_cikar['Access-Token'] = atoken
    r = requests.post(url_list['one_cikar'] + urun_id, headers=post_headers_one_cikar, data=data)
    print("istek gönderildi.")
    if r.status_code == 200:
        print("istek sonuc başarılı.")
        mesaj = 'ok'
    else:
        sonuc = r.json()
        mesaj = sonuc['message']
        print(sonuc['message'])
    return mesaj

def urun_sil(urun_id: int):
    data = '{{"productId": {urun_id} }}'.format(urun_id=urun_id)
    print("Ürün siliniyor...")

    r = requests.post(url_list['urun_sil'], headers=post_headers, data=data)
    if r.status_code == 200:
        print(str(urun_id) + ' idli urun silindi.')
        print(r.text)
        mesaj = "ok"
    else:
        print('urun silinemedi!!! sunucu farklı cevap veriyor status code: ' + str(r.text))
        mesaj = "hata"
    return mesaj

def profil_oner(hesap, atoken):
    print('Kullanici ID alınıyor...')
    user_id = nick_to_id(hesap)
    print('Kullanici ID Alindi.')
    print("Profil Öneriliyor ...")
    data = '{{"memberId":"{user_id}"}}'.format(user_id=user_id)
    print(data)
    post_headers['Access-Token'] = atoken
    r = requests.post(url_list['profil_oner'], headers=post_headers, data=data)
    if r.status_code == 200:
        print(str(hesap) + ' profili onerildi.')
        mesaj = "ok"
    else:
        sonuc = r.json()
        mesaj = sonuc['message']
        print(sonuc['message'])
    return mesaj


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'kadi' in session:
        return redirect(url_for('panel'))
    error = ''
    if request.method == 'POST':
        _kadi = kucuk_yap(request.form['kullanici_adi'])
        _sifre = request.form['sifre']
        if _kadi == None or _sifre == None:
            error = 'Kullanıcı adı veya şifre boş bırakılamaz!'
        else:
            sql = "select ID,kadi,sifre from kullanicilar where kadi=%s and sifre=%s;"
            cursor.execute(sql, (_kadi, _sifre,))
            if cursor.fetchone():
                up_sql = "update kullanicilar set giris_tarih = now() where kadi=%s;"
                cursor.execute(up_sql, (_kadi,))
                db.commit()
                session['kadi'] = _kadi
                return redirect(url_for('panel'))
            else:
                error = 'Yanlış kullanıcı adı veya şifre!'
    return render_template("index.html", error=error)


@app.route('/kayit-ol', methods=['GET', 'POST'])
def kayit_ol():
    error = ''
    ok = ''
    if request.method == 'POST':
        _kadi = kucuk_yap(request.form['kullanici_adi'])
        _sifre = request.form['sifre']
        _mail = kucuk_yap(request.form['mail'])

        if _kadi == None or _sifre == None or _mail == None:
            error = "tüm bilgileri eksiksiz doldurun!"
        else:
            sql = "insert into kullanicilar (kadi, sifre, mail, kayit_tarih, onay) values(%s, %s, %s, now(), 1)"
            cursor.execute(sql, (_kadi, _sifre, _mail,))
            db.commit()
            if cursor.rowcount:
                ok = "başarılı şekilde kayıt olundu. Panele yönlendiriliyorsunz, bekleyiniz..."
            else:
                error = "bekleyen bir hata oluştu!"
    return render_template("kayit.html", error=error, ok=ok)


@app.route('/panel/')
def panel():
    if 'kadi' not in session:
        return redirect(url_for('index'))
    return render_template("panel.html")


@app.route('/hesaplarim/')
@app.route('/hesaplarim/<islem>', methods=['GET', 'POST'])
def hesaplarim(islem=None):
    if 'kadi' not in session:
        return redirect(url_for('index'))
    if islem == 'ekle':
        error = ''
        ok = ''
        if request.method == 'POST':
            kadi = kucuk_yap(request.form['kullanici_adi'])
            sifre = request.form['sifre']

            if kadi == '' and sifre == '':
                error = 'Tüm alanlarını doldurunuz'
            else:
                atoken = giris_yap(kadi, sifre)
                if atoken == "hata":
                    error = "Dolap kullanıcı adınız ya da şifreniz yanlış, lütfen doğru bilgilerini giriniz!"
                else:
                    kid = id_bul(session['kadi'])
                    sql = "insert into hesaplar (hesap_adi,hesap_sifre,kullanici_id) values(%s,%s,%s)"
                    cursor.execute(sql, (kadi, sifre, kid,))

                    if cursor.rowcount > 0:
                        id = cursor.lastrowid
                        profil_bilgiler = profil_getir(kadi)
                        dolap_id = str(profil_bilgiler['id'])
                        takip_eden = str(profil_bilgiler['takip_eden'])
                        takip_ettigi = str(profil_bilgiler['takip_ettigi'])

                        upsql = "update hesaplar set dolap_id = %s, dolap_takip_eden = %s, dolap_takip_ettigi = %s, atoken=%s where ID = %s"
                        cursor.execute(upsql, (dolap_id, takip_eden, takip_ettigi, atoken, id, ))
                        if cursor.rowcount > 0:
                            ok = 'kayıt başarılı'
                            db.commit()
                        else:
                            error = "beklenmeyen farklı bir sorun oluştu!"
                    else:
                        error = 'beklenmeyen bir sorun oldu!'

        return render_template("hesaplarim.html", islem=islem, error=error, ok=ok)
    elif islem == 'bilgileri-getir':
        ok = ""
        error = ""
        if request.method == 'POST':
            kadi = request.form['hesap_adi']
            id = request.form['hesap_id']
            profil_bilgiler = profil_getir(kadi)
            takip_eden = str(profil_bilgiler['takip_eden'])
            takip_ettigi = str(profil_bilgiler['takip_ettigi'])
            upsql = "update hesaplar set dolap_takip_eden = %s, dolap_takip_ettigi = %s where ID = %s"
            cursor.execute(upsql, (takip_eden, takip_ettigi, id,))
            print(profil_bilgiler)
            if cursor.rowcount > 0:
                ok = 'Bilgiler başarılı şekilde güncellendi. yönlendiriliyorsunuz...'
                db.commit()
            else:
                error = "bilgiler aynı olduğu için güncellenmedi ya da beklenmeyen farklı bir sorun oluştu!"
            return render_template("hesaplarim.html", islem=islem, error=error, ok=ok)
    elif islem == None:

        kid = id_bul(session['kadi'])
        hsql = "select * from hesaplar where kullanici_id = %s"
        cursor.execute(hsql, (int(kid),))
        hesaplar = cursor.fetchall()

        return render_template("hesaplarim.html", hesaplar=hesaplar, islem=islem)
    else:
        abort(404)

    return render_template("hesaplarim.html", islem=islem)


@app.route('/urunlerim/')
@app.route('/urunlerim/<islem>', methods=['GET', 'POST'])
def urunlerim(islem=None):
    if 'kadi' not in session:
        return redirect(url_for('index'))
    if islem == 'getir':
        if request.method == 'POST':
            hesap_id = request.form['hesap']
            hesap_sql = "select * from hesaplar where ID=%s"
            cursor.execute(hesap_sql, (int(hesap_id),))
            hesap = cursor.fetchone()
            atoken = str(hesap['atoken'])
            hesap_adi = str(hesap['hesap_adi'])
            urunler = urunlerimi_getir(hesap_adi, atoken)

            return render_template("urunlerim.html", urunler=urunler, islem=islem, hesap_adi=hesap_adi)
    elif islem == 'one-cikar':

        if request.method == 'POST':
            urun_id = request.form['urun_id']
            hesap_adi = request.form['hesap_adi']
            hesap_sql = "select * from hesaplar where hesap_adi=%s"
            cursor.execute(hesap_sql, (hesap_adi,))
            hesap = cursor.fetchone()
            atoken = str(hesap['atoken'])
            one_cikar = urun_one_cikar(urun_id, atoken)
            return render_template("urunlerim.html", one_cikar=one_cikar, islem=islem)
    elif islem == 'sil':
        if request.method == 'POST':
            urun_id = request.form['urun_id']
            sonuc = urun_sil(urun_id)

            return render_template("urunlerim.html", sonuc=sonuc, islem=islem)
    elif islem == None:
        hesaplar = tum_hesaplar(session['kadi'])
        return render_template("urunlerim.html", islem=islem, hesaplar=hesaplar)
    else:
        abort(404)
    return render_template("urunlerim.html", islem=islem)


@app.route('/takipci_islemlerim/')
@app.route('/takipci_islemlerim/<islem>', methods=['GET', 'POST'])
def takipci_islemlerim(islem=None):
    if 'kadi' not in session:
        return redirect(url_for('index'))
    if islem == 'takip-et':
        error = ''
        mesaj = ''

        hesaplar = tum_hesaplar(session['kadi'])

        if request.method == 'POST':
            p_adi = request.form['profil_adi']
            hesap_id = request.form['hesap']
            if p_adi == '':
                error = "boş bırakmayınız!"
            else:
                mesaj = "takip etmeye başlandı"
                hesap_sql = "select * from hesaplar where ID=%s"
                cursor.execute(hesap_sql, (int(hesap_id), ))
                hesap = cursor.fetchone()
                atoken = str(hesap['atoken'])
                t = AppContextThread(takip_et(p_adi, atoken, zaman=10))
                t.start()
                t.join()
        return render_template("takipci-islemlerim.html", islem=islem, error=error, mesaj=mesaj, hesaplar=hesaplar)
    elif islem == 'takip-cikar':
        error = ''
        mesaj = ''

        hesaplar = tum_hesaplar(session['kadi'])

        if request.method == 'POST':
            hesap_id = request.form['hesap']

            if hesap_id == '':
                error = "boş bırakmayınız!"
            else:
                mesaj = "takipten çıkarılmaya başlandı"
                hesap_sql = "select * from hesaplar where ID=%s"
                cursor.execute(hesap_sql, (int(hesap_id), ))
                hesap = cursor.fetchone()
                hesap_adi = str(hesap['hesap_adi'])
                atoken = str(hesap['atoken'])
                t = AppContextThread(takip_cikar(hesap_adi, atoken, zaman=10))
                t.start()
                t.join()

        return render_template("takipci-islemlerim.html", islem=islem, error=error, mesaj=mesaj, hesaplar=hesaplar)
    elif islem == 'profil-oner':
        mesaj = ''
        hesapar = tum_hesaplar(session['kadi'])
        if request.method == 'POST':
            hesap_id = request.form['hesap']
            profil_adi = kucuk_yap(request.form['profil_adi'])

            if profil_adi == '':
                mesaj = "bos"
            else:
                hesap_sql = "select * from hesaplar where ID=%s"
                cursor.execute(hesap_sql, (int(hesap_id), ))
                hesap = cursor.fetchone()
                atoken = str(hesap['atoken'])
                mesaj = profil_oner(profil_adi, atoken)

        return render_template("takipci-islemlerim.html", islem=islem, hesaplar=hesapar, mesaj=mesaj)
    else:
        abort(404)
    return render_template("takipci-islemlerim.html", islem=islem)


@app.route('/cikis-yap/')
def cikis_yap():
    session.clear()
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('panel'))
