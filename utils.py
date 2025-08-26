# FUNZIONI
#--------INIZIO IMPORT-------------
import random
#--------FINE IMPORT-------------


# Funzione per generare l'ID ( codice prodotto) - parametri in ingresso tipo (L/P/C), lista (che è una lista di prodotti, componenti, o lotti)
def genera_codice_id(tipo, lista):
    # Se è Lotto
    if tipo == "L":
        # Lotto -> attributo 'id' numerico
        nuovo_id = max((int(item.id) for item in lista), default=0) + 1
        return str(nuovo_id)
    # Se è componente o Prodotto
    elif tipo in ("C", "P"):
        # Componente o Prodotto -> attributo 'codice' alfanumerico tipo 'C001'
        prefisso = tipo
        codici_numerici = []

        for item in lista:
            codice = getattr(item, "codice", "")
            if codice.startswith(prefisso):
                try:
                    numero = int(codice[len(prefisso):])
                    codici_numerici.append(numero)
                except ValueError:
                    continue  # Salta codici non convertibili

        nuovo_num = max(codici_numerici, default=0) + 1
        return f"{prefisso}{nuovo_num:03d}"  # formato tipo 'C003'

    else:
        raise ValueError("Tipologia non valida. Usa 'L', 'C' o 'P'")


# Funzione per generare un numero da un max a un min
def genera_random_int(min_val, max_val):
  if not isinstance(min_val, int) or not isinstance(max_val, int):
    raise TypeError("Sia min_val che max_val devono essere interi")
  if min_val > max_val:
    raise ValueError("min_val non può essere maggiore di max_val.")
  return random.randint(min_val, max_val)

# Funzione di supporto per mappare i componenti per codice, in ingresso riceve una lista
def get_dizionario_mappa_componenti(lista_di_tutti_i_lotti):
    all_components = {}
    for lotto in lista_di_tutti_i_lotti:
        if lotto.ordinativo:
            for riga in lotto.ordinativo:
                prodotto = riga.prodotto
                # Controllo che prodotto abbia una lista di componenti (prodotto.componenti)
                if hasattr(prodotto, 'componenti') and prodotto.componenti:
                    for comp_quant in prodotto.componenti:  # Assumendo che prodotto.componenti sia una lista di ComponenteQuantificato
                        componente = comp_quant.componente  # Ottieni l'oggetto Componente
                        if componente.codice not in all_components:
                            all_components[componente.codice] = componente

    # DEVE RITORNARE SEMPRE UN DIZIONARIO, ANCHE SE VUOTO!!
    return all_components


## ---- INIZIO FUNZIONI TKINTER ----
# Funzione Tkinter per Aggiornare il codice nella Label
# in essa richiama genera_codice_id
def aggiorna_codice_entry(tipo, lista, entry_codice):
    # Genera il nuovo codice/id
    nuovo_valore = genera_codice_id(tipo, lista)

    # Sbianca il campo e inserisce il nuovo valore
    entry_codice.delete(0, "end")
    entry_codice.insert(0, str(nuovo_valore))

# Funzione Tkinter per rendere modificabile una entryarea
def modifica_entry_on(entry):
    entry.config(state="normal")

# Funzione Tkinter per rendere una entry non più modificabile
def modifica_entry_off(entry):
    entry.config(state="disabled")

# Funzione Tkinter per mettere un valore dentro una entry
def valorizza_entry(valore, entry):
    entry.delete(0, "end")
    entry.insert(0, str(valore))

## ---- FINE FUNZIONI TKINTER ----


