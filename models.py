# Classi
#--------INIZIO IMPORT-------------
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict
import random
#--------FINE IMPORT-------------


## LE COMPONENTI SONO UTILIZZATE PER DEFINIRE COSA COMPONE L'OGGETTO
@dataclass
class ComponenteProdotto:
    codice: str
    nome: str
    tempo_produzione_unitario: float
    percentuale_scarto: float
    ## LA QUANTITà DEI COMPONENTI NON SI PUò GENERARE

    @staticmethod
    def genera_tempo_produzione(min_val: float = 0.5, max_val: float = 3.0) -> float:
        """Genera un tempo realistico per la produzione di un componente"""
        return round(random.uniform(min_val, max_val), 2)

    @staticmethod
    def genera_percentuale_scarto(min_val: float = 1.0, max_val: float = 6.0) -> float:
        """Genera una percentuale di scarto realistica"""
        return round(random.uniform(min_val, max_val), 1)



# mi serve per quantificare il numero di componenti
# classe per definire quanti pezzi di un componente servono in un determinato prodotto
@dataclass
class ComponenteQuantificato:
    componente: ComponenteProdotto
    quantita: int  # quante unità servono per un prodotto


    
    def calcola_fabbisogno(self, numero_prodotti_finali: int) -> int:
        fabbisogno_lordo = self.quantita * numero_prodotti_finali
        # Accedi alla percentuale_scarto tramite l'oggetto 'componente'
        if 1 - (self.componente.percentuale_scarto / 100) <= 0: # <-- Dividi per 100 se la percentuale è 1-100
            raise ValueError("La percentuale di scarto deve essere inferiore al 100%")

        return int(fabbisogno_lordo / (1 - (self.componente.percentuale_scarto / 100)))


 ## I PRODOTTI SONO GLI OGGETTI FINALI
@dataclass
class Prodotto:
    codice: str
    nome: str
    componenti: List[ComponenteQuantificato] 
    tempo_assemblaggio_unitario: float = 0.0

    def tempo_totale_unitario(self): 
        tempo_componenti = sum(
            cq.quantita * cq.componente.tempo_produzione_unitario
            for cq in self.componenti
        )
        return tempo_componenti + self.tempo_assemblaggio_unitario
    
    def tempo_totale_componenti(self):
        tempo_componenti = sum(
            cq.quantita * cq.componente.tempo_produzione_unitario
            for cq in self.componenti
        )
        return tempo_componenti

    # Questo metodo controlla se il prodotto ha ALMENO UN componente quantificato
    def ha_componenti(self):
        return bool(self.componenti) # Restituisce True se la lista non è vuota, False altrimenti


    #Genera il tempo di assemblaggio unitario in minuti e lo assegna all’attributo.
    #Range personalizzabile tra min_sec e max_sec in secondi
    @staticmethod
    def genera_tempo_assemblaggio( min_sec=60, max_sec=300, decimale=True):
            if decimale:
                tempo_sec = random.uniform(min_sec, max_sec)
            else:
                tempo_sec = random.randint(min_sec, max_sec)

            return round(tempo_sec / 60, 2)
    
    
    def calcola_fabbisogno_componenti(self, numero_prodotti: int) -> Dict[str, int]:
        """
        Restituisce un dizionario con il CODICE di ogni componente e la quantità totale necessaria
        per il numero_prodotti specificato.
        """
        return {
            cq.componente.codice: cq.calcola_fabbisogno(numero_prodotti)
            for cq in self.componenti
        }

    def get_tempo_assemblaggio_unitario(self):
        return self.tempo_assemblaggio_unitario

# QUESTA DATACLASS SERVE PER ASSOCIARE I PRODOTTI CON LA QUANTITà DA PRODURRE
# la classe serve per ogni riga del lotto, è un oggetto che va a comporre una lista
@dataclass
class RigaLotto:
    prodotto: Prodotto
    quantita: int

## UN LOTTO DI PRODUZIONE SI COMPONE DI X PRODOTTI
# classe serve per avere un ID del lotto e la lista delle righe che lo compongono
@dataclass
class LottoProduzione:
    id: str
    ordinativo: List[RigaLotto]
#    prodotto: Prodotto
#    quantita: int



    @classmethod
     # ???
    def genera(cls, prodotto: Prodotto, min_q: int = 500, max_q: int = 2000):
        qta = random.randint(min_q, max_q)
        return cls(prodotto=prodotto, quantita=qta)
     # ???

    # Calcola il tempo totale di produzione per tutto l'ordinativo
    def tempo_totale_ordinativo(self) -> float:
        tempo_totale = 0.0

        # Cicla ogni riga dell'ordinativo (ogni lotto da produrre)
        for riga in self.ordinativo:
            # Calcola il tempo totale per questo prodotto moltiplicando la quantità per il tempo unitario
            tempo_riga = riga.quantita * riga.prodotto.tempo_totale_unitario()

            # Somma al totale
            tempo_totale += tempo_riga

        # Restituisce il tempo totale richiesto per produrre tutto l'ordinativo
        return tempo_totale

    def tempo_per_prodotto_componenti(self) -> dict:
        # Dizionario che conterrà il tempo totale di produzione componenti per prodotto per ogni prodotto
        tempi_per_prodotto = {}

        # Cicla ogni riga dell'ordinativo (ogni riga rappresenta un prodotto da produrre in una certa quantità)
        for riga in self.ordinativo:
            prodotto = riga.prodotto  # Oggetto prodotto
            nome_prodotto = prodotto.nome  # Assumiamo che il prodotto abbia un attributo 'nome'

            # Calcola il tempo necessario per produrre tutti i componenti del prodotto
            tempo_componenti = prodotto.tempo_totale_componenti()

            # Moltiplica per la quantità di quel prodotto richiesta nell'ordinativo
            tempo_riga = riga.quantita * tempo_componenti

            # Salva nel dizionario usando il nome del prodotto come chiave
            tempi_per_prodotto[nome_prodotto] = tempo_riga

        # Restituisce il dizionario contenente i tempi per ciascun prodotto
        return tempi_per_prodotto
    

    def tempo_per_prodotto_assemblaggio(self) -> dict:
        # Dizionario che conterrà il tempo totale di assmblaggio per ogni prodotto
        tempi_per_prodotto = {}

        # Cicla ogni riga dell'ordinativo (ogni riga rappresenta un prodotto da produrre in una certa quantità)
        for riga in self.ordinativo:
            prodotto = riga.prodotto  # Oggetto prodotto
            nome_prodotto = prodotto.nome  # Assumiamo che il prodotto abbia un attributo 'nome'
            if prodotto.ha_componenti():
                # Se il prodotto ha componenti, calcola e aggiungi il suo tempo di assemblaggio
                tempo_assemblaggio = prodotto.get_tempo_assemblaggio_unitario()
                tempo_riga = riga.quantita * tempo_assemblaggio
                tempi_per_prodotto[nome_prodotto] = tempo_riga
            else:
                # Se il prodotto NON ha componenti, NON aggiungere nulla al dizionario.
                # Questo fa sì che non venga visualizzato nell'output della GUI.
                pass
        return tempi_per_prodotto



    def tempo_totale_stampaggio(self):
        return self.quantita * self.prodotto.tempo_totale_componenti()
    
    # ???
    def tempo_totale_assemblaggio(self):
        return self.quantita * self.prodotto.get_tempo_assemblaggio_unitario()
    
    # Calcola il fabbisogno totale 
    def calcola_fabbisogno_totale(self) -> Dict[str, int]:
        # Dizionario per accumulare il fabbisogno totale dei componenti
        fabbisogno_totale = {}

        # Cicla ogni riga dell'ordinativo (cioè ogni lotto da produrre)
        for riga in self.ordinativo:
            # Calcola il fabbisogno dei componenti per questo prodotto e quantità
            fabbisogno_prodotto = riga.prodotto.calcola_fabbisogno_componenti(riga.quantita)

            # Unisce il fabbisogno del prodotto al totale
            for nome_componente, quantita in fabbisogno_prodotto.items():
                # Se il componente è già presente, somma le quantità
                if nome_componente in fabbisogno_totale:
                    fabbisogno_totale[nome_componente] += quantita
                # Altrimenti, aggiungilo al dizionario
                else:
                    fabbisogno_totale[nome_componente] = quantita

        # Restituisce il fabbisogno totale aggregato per tutti i prodotti del lotto
        return fabbisogno_totale


    # Metodo per il calcolod el fabbisogno analitico
    def calcola_fabbisogno_analitico(self) -> Dict[str, Dict[str, int]]:
        """
        Calcola il fabbisogno di componenti per ciascun prodotto nel lotto.
        Restituisce un dizionario dove la chiave è il **CODICE** del prodotto
        e il valore è un altro dizionario con i componenti e le loro quantità.
        """
        fabbisogno_analitico = {}
        for riga in self.ordinativo:
            prodotto = riga.prodotto
            quantita_prodotto_nel_lotto = riga.quantita

            fabbisogno_per_singolo_prodotto = prodotto.calcola_fabbisogno_componenti(quantita_prodotto_nel_lotto)

            # Ora usiamo prodotto.codice come chiave
            fabbisogno_analitico[prodotto.codice] = fabbisogno_per_singolo_prodotto
        return fabbisogno_analitico
    # --- FINE METODO AGGIORNATO ---

