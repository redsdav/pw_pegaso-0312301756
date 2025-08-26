# DATI DI BASE

#--------INIZIO IMPORT-------------
from models import ComponenteProdotto, Prodotto, ComponenteQuantificato, LottoProduzione, RigaLotto
#--------FINE IMPORT-------------

#-----VARIABILI-----
# Variabile per la funzione se impiega più della giornata lavorativa
label_risultato = None
# Variabili globali per salvare i parametri min e max delle linee produttive
min_val_linea_produttive = 1
max_val_linea_produttive = 6

# Variabili globali per salvare i parametri min e max delle linee di assemblaggio
min_val_linea_assemblaggio = 1
max_val_linea_assemblaggio = 3

# Variabili globali per salvare i parametri min e max delle ore giornata
min_val_ore_giornata = 4
max_val_ore_giornata = 16

#-----FINE VARIABILI-----

#---- Inizio Componenti----
componenteProdotto1 = ComponenteProdotto(
    codice = "C001",
    nome = "Scocca SCUN",
    tempo_produzione_unitario = 0.6,
    percentuale_scarto = 2
)

componenteProdotto2 = ComponenteProdotto(
    codice = "C002",
    nome = "Serbatoio SERB01",
    tempo_produzione_unitario = 1.2,
    percentuale_scarto = 3
)

componenteProdotto3 = ComponenteProdotto(
    codice = "C003",
    nome="Pulsante PULS001",
    tempo_produzione_unitario = 0.6,
    percentuale_scarto = 0.5
)

componenteProdotto4 = ComponenteProdotto(
    codice = "C004",
    nome = "Scocca SCDW",
    tempo_produzione_unitario = 1.0,
    percentuale_scarto = 1
)

componenteProdotto5 = ComponenteProdotto(
    codice = "C005",
    nome = "Scocca SCUP",
    tempo_produzione_unitario = 1.5,
    percentuale_scarto = 1.5
)

componenteProdotto6 = ComponenteProdotto(
    codice = "C006",
    nome = "Conchiglia P003",
    tempo_produzione_unitario = 0.8,
    percentuale_scarto = 3
)
#---- Fine Componenti----

#---- Inizio Prodotti----
prodotto1 = Prodotto(
    codice = "P001",
    nome = "Dispenser Sapone",
    componenti=[
        ComponenteQuantificato(componenteProdotto1,1),
        ComponenteQuantificato(componenteProdotto2,1),
        ComponenteQuantificato(componenteProdotto3,2)
    ],
    tempo_assemblaggio_unitario = 2
)

prodotto2 = Prodotto(
    codice = "P002",
    nome = "Dispenser Sacchetti Igienici",
    componenti=[
        ComponenteQuantificato(componenteProdotto4,1),
        ComponenteQuantificato(componenteProdotto5,1),
    ],
    tempo_assemblaggio_unitario = 1.5
)

prodotto3 = Prodotto(
    codice = "P003",
    nome = "Conchiglia Portagioie",
    componenti=[
        ComponenteQuantificato(componenteProdotto6,1)
    ],
    tempo_assemblaggio_unitario = 0
)
#---- Fine Prodotti----

#---- Inizio Righe Lotto----
rigaLotto1 = RigaLotto(
    prodotto = prodotto1,
    quantita = 50
)

rigaLotto2 = RigaLotto(
    prodotto = prodotto2,
    quantita = 70
)

rigaLotto3 = RigaLotto(
    prodotto = prodotto3,
    quantita = 150
)
#---- Fine Righe Lotto----

#---- Inizio Lotto di produzione----
lotto1 = LottoProduzione(
    id = "1",
    ordinativo = [
        rigaLotto1,
        rigaLotto2,
        rigaLotto3
    ]
)
#---- Fine Lotto di produzione----

#---- Inizio Liste ----
ListaComponenti = [componenteProdotto1,componenteProdotto2,componenteProdotto3,componenteProdotto4,componenteProdotto5,componenteProdotto6]
ListaProdotti = [prodotto1,prodotto2,prodotto3]
ListaLotti = [lotto1]
#---- Fine Liste ----