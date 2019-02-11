import haravasto
import random
import time
import pyglet
from pyglet.window import key

NAPPAIN_Q = pyglet.window.key.Q #näppäimen q painaminen lopettaa käynnissä olevan pelin ja sulkee peli-ikkunan

def kysy_kentan_koko():
    """Kysyy käyttäjältä kentän koon. Maksimi koko on 20 x 20 Palauttaa leveys, korkeus"""
    while True:
        try:
            leveys = int(input("Anna kentän leveys: "))
            if leveys > 20:
                print("Kentän maksimi koko on 20 x 20.")
                continue
        except ValueError:
            print("Anna leveys kokonaislukuna!")
            continue
        while True:
            try:
                korkeus = int(input("Anna kentän korkeus: "))
                if korkeus > 20:
                    print("Kentän maksimi koko on 20 x 20.")
                    continue
            except ValueError:
                print("Anna korkeus kokonaislukuna!")
            else:
                return leveys, korkeus
                
def kysy_miinojen_maara():
    """Kysyy käyttäjältä miinojen määrän ja palauttaa sen"""
    while True:
        try:
            miinoja = int(input("Anna miinojen määrä: "))
        except ValueError:
            print("Miinojen määrän on oltava kokonaisluku!")
        else:
            return miinoja
            
def luo_tyhja_kentta(leveys, korkeus):
    """Luo tyhjan kentän, jonka dimensiot on leveys X korkeus"""
    kentta = []
    for rivi in range(korkeus):
        kentta.append([])
        for sarake in range(leveys):
            kentta[-1].append(" ")
    return kentta
    
def luo_lista_vapaista(leveys, korkeus):
    """Luo listan vapaista ruuduista, 
    eli listan jossa on kaikki x,y koordinaattiparit. Lista sisältää monikkoja (x, y).
    Kun kenttää miinoitetaan, koordinaattipari, johon miina sijoitetaan poistetaan vapaat_koordinaatit listasta"""
    
    vapaat_koordinaatit = []
    for x in range(leveys):
        for y in range(korkeus):
            vapaat_koordinaatit.append((x, y))
    return vapaat_koordinaatit
    
def miinoita(kentta, vapaat, miinojen_lkm):
    """Asettaa kentta muuttujaan, vapaat listassa oleviin koordinattipareihin satunnaisesti määrän n miinoja.
    Koordinaattipari poistetaan vapaat listasta, kun kyseiseen koordinaattipariin on asetettu miina"""
    miinotettavat = random.sample(vapaat, k=miinojen_lkm)
    for koordinaatti in miinotettavat:
        x = koordinaatti[0]
        y = koordinaatti[1]
        kentta[y][x] = "m"
        vapaat.remove(koordinaatti)

def tulvatayta(kentta, x, y):
    """Jos kentän x, y koordinaateissa ei ole miinoja aukaistaan kaikki ympäröivät ja niitä ympäröivät jne. ruudut
    joka suuntaan niin pitkälle että saavutettaan miinakentän raja tai ensimmäinen numeroruutu, joka myös aukaistaan.
    
    Aloittaa täytön koordinaateista x, y ja vaihtaa  " " -> "0". Lista muuttujassa on lista joka sisältää monikkoja 
    (x, y) koordinaattiparin. Monikko otetaan tarkasteluun, lasketaan koordinaatteja vastaavan ruudun ympäröivät 
    miinat, poistetaan monikko listasta ja merkitään ruudun arvoksi ympäröivien miinojen lukumäärä, eli aukaistaan 
    ruutu. Seuraavaksi katsotaan viereisten ruutujen ympäröivät 
    miinat ja merkitään niihin niiden ympärillä olevien miinoijen lukumäärä. Jos naapuri ruudun ympärillä on 0 miinaa,
    lisätään tämän koordinaattipari listaan, jolloin tulvatäyttö jatkuu niin pitkään kunnes saavutetaan alue,
    jonka ympäröi numeroruudut."""
    leveys = len(kentta[0])
    korkeus = len(kentta)
    if kentta[y][x] == " ":
        lista = [(x, y)]
        while len(lista) >= 1:
        
            x_koord = lista[-1][0]
            y_koord = lista[-1][1]
            lista.pop()
            kentta[y_koord][x_koord] = str(laske_ymparoivat_miinat(kentta, x_koord, y_koord))
            
            for j in range(-1, 2):
                for i in range(-1, 2):
                    if ((y_koord + j) > -1 and (y_koord + j) < korkeus) and ((x_koord + i) > -1 and (x_koord + i) < leveys):
                        if kentta[y_koord + j][x_koord + i] == " ":
                            miinoja_ymparilla = laske_ymparoivat_miinat(kentta, (x_koord + i), (y_koord + j))
                            if miinoja_ymparilla == 0:
                                kentta[y_koord + j][x_koord + i] = str(miinoja_ymparilla)
                                koordinaatti_pari = ((x_koord + i), (y_koord + j))
                                lista.append(koordinaatti_pari)
                            elif miinoja_ymparilla > 0:
                                kentta[y_koord + j][x_koord + i] = str(miinoja_ymparilla)
        
def aukaise_ruutu(kentta, x, y):
    """Aukaisee kentän ruudun, jonka koordinaatit on x, y"""
    if kentta[y][x] == "m":
        #peli loppuu
        tila["klikkauksia"] = tila["klikkauksia"] + 1
        havia_peli(kentta, x, y)
    elif kentta[y][x] == " ":
        tila["klikkauksia"] = tila["klikkauksia"] + 1
        miinoja_ymparilla = laske_ymparoivat_miinat(kentta, x, y)
        if miinoja_ymparilla == 0:
            tulvatayta(kentta, x, y)
        elif miinoja_ymparilla > 0:
            kentta[y][x] = str(miinoja_ymparilla)
            
def laske_ymparoivat_miinat(kentta, x, y):
    """Laskee ja palauttaa miinojen määrän kentan koordinaattien x, y ympärillä."""
    leveys = len(kentta[0])
    korkeus = len(kentta)
    miinoja = 0
    for j in range(-1, 2):
        for i in range(-1, 2):
            if ((y + j) > -1 and (y + j) < korkeus) and ((x + i) > -1 and (x + i) < leveys):
                naapuri = kentta[y + j][x + i]
                if naapuri == "m":
                    miinoja = miinoja + 1
                if naapuri == "f":
                    if tarkista_lipun_oikeus((x + i), (y + j)):
                        miinoja = miinoja + 1
    return miinoja
    
    
def merkitse_miina(x, y):
    """Asettaa ruutuun lipun tai jos ruudussa on lippu poistaa lipun. tila[xy] kertoo onko ruudussa ollut miina 
    vai tyhjä ennen lippua. Näin ollen kun lippu poistetaan osataan ruutuun laittaa oikea arvo takaisin."""
    if tila["kentta"][y][x] == "m":
        xy = str(x) + str(y)
        tila[xy] = "m"
        tila["kentta"][y][x] = "f"
    elif tila["kentta"][y][x] == " ":
        xy = str(x) + str(y)
        tila[xy] = " "
        tila["kentta"][y][x] = "f"
    elif tila["kentta"][y][x] == "f":
        xy = str(x) + str(y)
        tila["kentta"][y][x] = tila[xy]
            
def havia_peli(kentta, x, y):
    """Peli loppuu häviöön. Kutsutaan kun pelaaja avaa ruudun jossa on miina"""
    kentta[y][x] = "x"
    tila["ohje"] = "Hävisit pelin (poistu q)"
    tila["pelitila"] = "off"
    tila["kelloloppuu"] = time.clock()

def voita_peli():
    """Kutsutaan, kun kaikki miinoittamattomat ruudut on aukaistu."""
    tila["ohje"] = "Voitit pelin! (poistu q)"
    tila["pelitila"] = "off"
    tila["kelloloppuu"] = time.clock()

def kasittele_hiiri(x, y, nappi, muokkausnapit):
    korkeus = len(tila["kentta"])
    x_korjattu = x // 40
    y_korjattu = y // 40
    y_uus_korjattu = korkeus - y_korjattu - 1
    if nappi == haravasto.HIIRI_OIKEA:
        if tila["pelitila"] == "on":
            merkitse_miina(x_korjattu, y_uus_korjattu)
    elif nappi == haravasto.HIIRI_VASEN:
        if tila["pelitila"] == "on":
            aukaise_ruutu(tila["kentta"], x_korjattu, y_uus_korjattu)
            if laske_aukaisemattomat() == 0:
                voita_peli()

def nappain_kasittelija(nappain, mod):
    if nappain == NAPPAIN_Q:
        haravasto.lopeta()
        if tila["pelitila"] == "on":
            tila["kelloloppuu"] = time.clock()
            tila["ohje"] = "jätetty kesken"
                
def piirra_kentta():
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()
    for j, rivi in enumerate(tila["kentta"]):
        for i, ruutu in enumerate(rivi):
            if ruutu != "m" and ruutu != "x":
                haravasto.lisaa_piirrettava_ruutu(ruutu, i * 40, ((ikkunan_korkeus - 90) - j * 40))
            elif ruutu == "m":
                haravasto.lisaa_piirrettava_ruutu(" ", i * 40, ((ikkunan_korkeus - 90) - j * 40))
            elif ruutu == "x":
                haravasto.lisaa_piirrettava_ruutu("x", i * 40, ((ikkunan_korkeus - 90) - j * 40))
    haravasto.piirra_ruudut()
    haravasto.piirra_tekstia(tila["ohje"], 0, korkeus * 40 + 5)

def tarkista_lipun_oikeus(x, y):
    """tarkistaa onko ruudussa x, y oleva lippu oikeasti miina, palauttaa totuus arvon"""
    if tila["kentta"][y][x] == "f":
        xy = str(x) + str(y)
        if tila[xy] == "m":
            return True
        else:
            return False

def laske_aukaisemattomat():
    """Laskee montako aukaisematonta ruutua on jäljellä. Voidaan käyttää pelin voiton määrittelemiseen"""
    aukaisemattomia = 0
    for j, rivi in enumerate(tila["kentta"]):
        lisattavat = rivi.count(" ")
        aukaisemattomia = aukaisemattomia + lisattavat
        for i, ruutu in enumerate(rivi):
            if ruutu == "f":
                if not tarkista_lipun_oikeus(i, j):
                    aukaisemattomia = aukaisemattomia + 1
    return aukaisemattomia

def tallenna_peli_tilastoon(tilastot):
    """Kutsutaan pelin lopuksi ja tallennetaan tietoja pelistä tilastoon"""
    alotus = tila["alotus"]
    
    alotus_vuosi = alotus.tm_year
    alotus_kuukausi = alotus.tm_mon
    alotus_paiva = alotus.tm_mday
    alotus_tunti = alotus.tm_hour
    alotus_min = alotus.tm_min
    alotus_sec = alotus.tm_sec
    
    aloitus_aika = "{}.{}.{} {:02}:{:02}:{:02}".format(alotus_paiva, alotus_kuukausi, alotus_vuosi, alotus_tunti, alotus_min, alotus_sec)
    
    tila["kesto"] = tila["kelloloppuu"] - tila["kelloalkaa"]
    kesto_tot_sec = tila["kesto"]
    kesto_min = int(kesto_tot_sec // 60)
    kesto_sec = int(kesto_tot_sec % 60)
    
    kesto = "Kesto: {:02}:{:02}".format(kesto_min, kesto_sec)
    
    kesto_vuoroissa = "Klikkauksia: {}".format(tila["klikkauksia"])
    
    if tila["ohje"] == "Hävisit pelin (poistu q)":
        lopputulos = "Lopputulos: Häviö. Kentän koko: leveys: {} korkeus: {} miinoja: {}".format(leveys, korkeus, miinoja)
    elif tila["ohje"] == "Voitit pelin! (poistu q)":
        lopputulos = "Lopputulos: Voitto. Kentän koko: leveys: {} korkeus: {} miinoja: {}".format(leveys, korkeus, miinoja)
    elif tila["ohje"] == "jätetty kesken":
        lopputulos = "Lopputulos: Jätetty kesken. Kentän koko: leveys: {} korkeus: {} miinoja: {}".format(leveys, korkeus, miinoja)

    tiedot = [lopputulos, aloitus_aika, kesto, kesto_vuoroissa]
    tilastot.append(tiedot)

def tallenna_tilastot_tiedostoon(tilastot):
    """Tallentaa tilastot tiedostoon. Kutsutaan ohjelman sulkeutuessa."""
    try:
        with open("tilastot.txt", "w") as kohde_tiedosto:
            for lopputulos, aloitus_aika, kesto, kesto_vuoroissa in tilastot:
                kohde_tiedosto.write("{}, {}, {}, {}\n".format(lopputulos, aloitus_aika, kesto, kesto_vuoroissa))
    except IOError:
        print("Kohdetiedostoa ei voitu avata. Tallennus epäonnistui")
        

def nayta_tilastot():
    """Kutsutaan päävalikosta. Tulostaa tilastot"""
    for i, rivi in enumerate(tilastot):
        print(tilastot[i][0])
        print(tilastot[i][1], tilastot[i][2], tilastot[i][3])
        print(" ")

def lataa_tilastot_tiedostosta():
    """Lataa ja palauttaa tilastot tiedostosta. Kutsutaan ohjelman alussa."""
    tilastot = []
    try:
        with open("tilastot.txt") as lahde:
            for tiedot in lahde.readlines():
                lopputulos, aloitus_aika, kesto, kesto_vuoroissa = tiedot.split(",")
                lopputulos = lopputulos.strip()
                aloitus_aika = aloitus_aika.strip()
                kesto = kesto.strip()
                kesto_vuoroissa = kesto_vuoroissa.strip()
                tilastot.append([lopputulos, aloitus_aika, kesto, kesto_vuoroissa])
    except IOError:
        print("Aiempia tilastoja ei löytynyt.")
        
    return tilastot


print("Tervetuloa pelaamaan miinaharavaa!")
tilastot = lataa_tilastot_tiedostosta()

while True:
    print("Voit valita jonkin seuraavista vaihtoehdoista: ")
    print(" ")
    print("(U)usi peli")
    print("(N)äytä tilastot")
    print("(R)esetoi tilastot")
    print("(L)opeta")
    print(" ")
    
    valinta = input("Tee valintasi: ").strip().lower()
    if valinta == "l":
        tallenna_tilastot_tiedostoon(tilastot)
        break
    elif valinta == "u":
        leveys, korkeus = kysy_kentan_koko()
        ikkunan_leveys = leveys * 40
        ikkunan_korkeus = korkeus * 40 + 50

        tila = {
        "kentta": luo_tyhja_kentta(leveys, korkeus),
        "pelitila": "on", #kertoo onko peli on vai off, kun avataan miinoitettu ruutu pelitila vaihtuu off.
        "ohje": "Peli käynnissä",
        "klikkauksia": 0
        
        }
        miinoja = kysy_miinojen_maara()
        vapaat = luo_lista_vapaista(leveys, korkeus)
        miinoita(tila["kentta"], vapaat, miinoja)
        haravasto.lataa_kuvat("spritet")
        tila["alotus"] = time.localtime()
        print("Avataan peli-ikkuna. Voit poistua pelistä painamalla näppäintä \"q\"")
        tila["kelloalkaa"] = time.clock()
        haravasto.luo_ikkuna(leveys=ikkunan_leveys, korkeus=ikkunan_korkeus)
        haravasto.aseta_piirto_kasittelija(piirra_kentta)
        haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)
        haravasto.aseta_nappain_kasittelija(nappain_kasittelija)
        haravasto.aloita()
        tallenna_peli_tilastoon(tilastot)
        
        
        
    elif valinta == "n":
        nayta_tilastot()
    elif valinta == "r":
        tilastot = []
        print("Tilastot nollattu")
    else:
        print("Valitsemaasi toimintoa ei ole olemassa")
        











 

