# GUI
#--------INIZIO IMPORT-------------
import tkinter as tk
from utils import aggiorna_codice_entry, modifica_entry_on, valorizza_entry, genera_codice_id, genera_random_int, get_dizionario_mappa_componenti
from dati import *
from tkinter import ttk, messagebox
#--------FINE IMPORT-------------

class Applicazione:
    def __init__(self, master):

        # Creazione della finestra principale
        self.master = master
        master.title("Menù Principale")
        master.geometry("500x300")
        master.configure(bg="#f0f0f0")

        # Titolo
        self.titolo = tk.Label(master, text="Simulatore di Produzione - PW 1.5", font=("Arial", 16, "bold"), bg="#f0f0f0")
        self.titolo.pack(pady=(20, 5))

        # Sottotitolo
        self.sottotitolo = tk.Label(master, text="Rossi Davide - matr: 0312301756", font=("Arial", 12), bg="#f0f0f0")
        self.sottotitolo.pack(pady=(0, 20))

        # Pulsante principale - simulazione di produzione
        self.btn_simulatore = tk.Button(master, text="Simulatore Produzione", font=("Arial", 14), width=30, height=2, bg="#4CAF50", fg="white", command=self.simulatore_produzione)
        self.btn_simulatore.pack(pady=20)

        # Frame inferiore per pulsanti disposti in orizzontale
        bottom_frame = tk.Frame(master, bg="#f0f0f0")
        bottom_frame.pack(side=tk.BOTTOM, pady=10)

        # Etichetta sopra bottoni
        etichetta_soprabottoni = tk.Label(bottom_frame, text="Un lotto è composto da prodotti che a sua volta sono composti da componenti")
        etichetta_soprabottoni.pack(pady=5)

        # Pulsanti orizzontali in basso
        btn_info = [
            ("Prodotti", self.mostra_prodotti),
            ("Componenti", self.mostra_componenti),
            ("Lotti", self.mostra_lotti)
        ]
        
        # Ciclo per inserire i bottoni
        for nome, funzione in btn_info:
            btn = tk.Button(bottom_frame, text=nome, font=("Arial", 12), width=12, height=2, bg="#2196F3", fg="white", command=funzione)
            btn.pack(side=tk.LEFT, padx=10)

    # ========== Sezione 1 - Simulatore di Produzione ==========
    def simulatore_produzione(self):
        # Creazione finestra
        finestra = tk.Toplevel(self.master)
        finestra.title("Simulatore di Produzione")
        finestra.geometry("950x550")

        # Creazione frame sx
        frame_sx = ttk.Frame(finestra, padding=10)
        frame_sx.grid(row=0, column=0, sticky="nswe")
        finestra.grid_columnconfigure(0, weight=1)
        finestra.grid_rowconfigure(0, weight=1)
        
        # Selezione lotto tra lotti disponibili in ListaLotti
        ttk.Label(frame_sx, text="Seleziona un lotto:", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
        opzioni = [str(e.id) for e in ListaLotti]
        var_selezione = tk.StringVar()
        dropdown = ttk.Combobox(frame_sx, textvariable=var_selezione, values=opzioni, state="readonly", width=15)
        dropdown.grid(row=1, column=0, pady=5, sticky="we")
        
        #Sezione che mostra una tabella contenente le righe lotto, ovvero la quantità prodotti da produrre
        ttk.Label(frame_sx, text="Righe del Lotto", font=("Arial", 12)).grid(row=2, column=0, pady=(15, 5), sticky="w")
        tabella = ttk.Treeview(frame_sx, columns=("Codice", "Nome", "Quantità"), show="headings", height=15)
        for col in ("Codice", "Nome", "Quantità"):
            tabella.heading(col, text=col)
            tabella.column(col, width=120, anchor="center")
        tabella.grid(row=3, column=0, sticky="nsew")
        frame_sx.grid_rowconfigure(3, weight=1)
        frame_sx.grid_columnconfigure(0, weight=1)

        # Creazione frame di dx  con la funzione Notebook per avere più sezioni
        frame_dx = ttk.Notebook(finestra)
        frame_dx.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
        finestra.grid_columnconfigure(1, weight=2)


        # Tab Esito Simulazione
        tab_riepilogo = ttk.Frame(frame_dx, padding=10)
        frame_dx.add(tab_riepilogo, text="Esito Simulazione")

        output_riepilogo = tk.Text(tab_riepilogo, height=20, width=40, wrap="word")
        output_riepilogo.grid(row=0, column=0, sticky="nswe")
        tab_riepilogo.grid_rowconfigure(0, weight=1)
        tab_riepilogo.grid_columnconfigure(0, weight=1)

        # Aggiunta di una scrollbar al tab
        scrollbar_riep = ttk.Scrollbar(tab_riepilogo, command=output_riepilogo.yview)
        scrollbar_riep.grid(row=0, column=1, sticky="ns")
        output_riepilogo.config(yscrollcommand=scrollbar_riep.set)

        # Tab fabbisogno
        tab_fabbisogno = ttk.Frame(frame_dx, padding=10)
        frame_dx.add(tab_fabbisogno, text="Fabbisogno")

        output_text = tk.Text(tab_fabbisogno, height=20, width=40, wrap="word")
        output_text.grid(row=0, column=0, sticky="nswe")
        tab_fabbisogno.grid_rowconfigure(0, weight=1)
        tab_fabbisogno.grid_columnconfigure(0, weight=1)

        # Aggiunta di una scrollbar al tab
        scrollbar_fabb = ttk.Scrollbar(tab_fabbisogno, command=output_text.yview)
        scrollbar_fabb.grid(row=0, column=1, sticky="ns")
        output_text.config(yscrollcommand=scrollbar_fabb.set)

        # Tab parametri - contiene alcun parametri da impostare che saranno usati durante i calcoli della sezione
        tab_parametri = ttk.Frame(frame_dx, padding=10)
        frame_dx.add(tab_parametri, text="Parametri")

        # Linee Produttive
        ttk.Label(tab_parametri, text="Linee produttive (componenti):").grid(row=0, column=0, sticky="w", pady=5)
        entry_linee_prod = ttk.Entry(tab_parametri, width=10)
        entry_linee_prod.grid(row=0, column=1, pady=5)
        entry_linee_prod.insert(0, "1")

        # Bottone Genera Valore
        btn_genera_linee_prod = ttk.Button(tab_parametri, text="Genera", command=lambda: valorizza_entry(
            genera_random_int(min_val_linea_produttive, max_val_linea_produttive), entry_linee_prod))
        btn_genera_linee_prod.grid(row=0, column=2, pady=5)

        # Bottone Parametri definizione range (min - max)
        btn_genera_linee_prod = ttk.Button(tab_parametri, text="Parametri Genera",
                                           command=lambda: apri_finestra_range("produttive"))
        btn_genera_linee_prod.grid(row=0, column=3, pady=5)

        # Linee di Assemblaggio
        ttk.Label(tab_parametri, text="Linee assemblaggio:").grid(row=1, column=0, sticky="w", pady=5)
        entry_linee_assem = ttk.Entry(tab_parametri, width=10)
        entry_linee_assem.grid(row=1, column=1, pady=5)
        entry_linee_assem.insert(0, "1")
        # Bottone Genera Valore
        btn_genera_linee_assem = ttk.Button(tab_parametri, text="Genera", command=lambda: valorizza_entry(
            genera_random_int(min_val_linea_assemblaggio, max_val_linea_assemblaggio), entry_linee_assem))
        btn_genera_linee_assem.grid(row=1, column=2, pady=5)

        # Bottone Parametri definizione range (min - max)
        btn_genera_linee_prod = ttk.Button(tab_parametri, text="Parametri Genera",
                                           command=lambda: apri_finestra_range("assemblaggio"))
        btn_genera_linee_prod.grid(row=1, column=3, pady=5)

        # Durata Giornata Lavorativa
        ttk.Label(tab_parametri, text="Durata giornata lavorativa (ore):").grid(row=2, column=0, sticky="w", pady=5)
        entry_giorno_ore = ttk.Entry(tab_parametri, width=10)
        entry_giorno_ore.grid(row=2, column=1, pady=5)
        entry_giorno_ore.insert(0, "8")

        # Bottone Genera Valore
        btn_genera_giorno_ore = ttk.Button(tab_parametri, text="Genera", command=lambda: valorizza_entry(
            genera_random_int(min_val_ore_giornata, max_val_ore_giornata), entry_giorno_ore))
        btn_genera_giorno_ore.grid(row=2, column=2, pady=5)

        # Bottone Parametri definizione range (min - max)
        btn_genera_linee_prod = ttk.Button(tab_parametri, text="Parametri Genera",
                                           command=lambda: apri_finestra_range("ore_giornata"))
        btn_genera_linee_prod.grid(row=2, column=3, pady=5)

        for i in range(3):
            tab_parametri.grid_rowconfigure(i, weight=0)
        tab_parametri.grid_columnconfigure(1, weight=1)

        # Funzione per aggiornare la tabella delle righe lotto a ogni selezione di un lotto differente
        def aggiorna_tabella(event=None):
            selezionato = var_selezione.get()
            lotto = next((e for e in ListaLotti if str(e.id) == selezionato), None)
            tabella.delete(*tabella.get_children())
            if lotto:
                for riga in lotto.ordinativo:
                    p = riga.prodotto
                    if p and hasattr(p, "codice") and hasattr(p, "nome"):
                        tabella.insert("", "end", values=(p.codice, p.nome, riga.quantita))
                    else:
                        messagebox.showerror("Errore", "WARN - Una riga non contiene un prodotto valido.")

            output_text.delete("1.0", tk.END)
            # ELIMINARE outputtempo_text.delete("1.0", tk.END)
            output_riepilogo.delete("1.0", tk.END)

        # Richiamo della funzione di aggiornamento della tabella
        dropdown.bind("<<ComboboxSelected>>", aggiorna_tabella)


        # Funzione necessaria per il calcolo del fabbisogno - ovvero della quantità di componenti necessaria
        def calcola_fabbisogno():
            selezionato = var_selezione.get()
            lotto = next((e for e in ListaLotti if str(e.id) == selezionato), None)
            output_text.delete("1.0", tk.END)

            if lotto:
                # Prepara la mappa dei componenti una volta
                dizionario_mappa_componenti = get_dizionario_mappa_componenti(ListaLotti)

                # --- Stampa nella box l'inizio della sezione del fabbisogno analitica ---
                output_text.insert(tk.END, "-- FABBISOGNO ANALITICO PER PRODOTTO --\n")

                if lotto.ordinativo:
                    for riga in lotto.ordinativo:
                        prodotto = riga.prodotto
                        quantita_prodotto_nel_lotto = riga.quantita

                        # Ottiene il fabbisogno per i componenti di questo specifico prodotto (codice_componente: quantità)
                        fabbisogno_per_singolo_prodotto = prodotto.calcola_fabbisogno_componenti(
                            quantita_prodotto_nel_lotto)

                        # Stampa Codice e Nome del Prodotto
                        output_text.insert(tk.END,f"\n{prodotto.codice} - {prodotto.nome} (Quantità nel lotto: {quantita_prodotto_nel_lotto})\n")
                        if fabbisogno_per_singolo_prodotto:
                            for componente_codice, quantita in fabbisogno_per_singolo_prodotto.items():
                                # Usa un dizionare che mappa i componenti per trovare l'oggetto Componente e recuperare il nome
                                componente_obj = dizionario_mappa_componenti.get(componente_codice)
                                if componente_obj:
                                    output_text.insert(tk.END,
                                                       f"  {componente_obj.codice} - {componente_obj.nome}: {quantita}\n")
                                else:
                                    # Fallback - recupero dell'errore se per qualche motivo il componente non è nella mappa
                                    output_text.insert(tk.END,
                                                       f"  {componente_codice}: {quantita} (Nome non disponibile)\n")
                        else:
                            output_text.insert(tk.END, "  Nessun componente richiesto per questo prodotto.\n")
                    output_text.insert(tk.END, "\n")
                else:
                    output_text.insert(tk.END, "Nessun prodotto nell'ordinativo per il fabbisogno analitico.\n\n")

                # Stampa nella box l'instestazione della sezione del fabbisogno totale
                output_text.insert(tk.END, "-- FABBISOGNO TOTALE COMPONENTI --\n")
                fabbisogno_totale = lotto.calcola_fabbisogno_totale()
                fabbisogno_totale_int = sum(fabbisogno_totale.values())
                if fabbisogno_totale:
                    for componente_codice, quantita in fabbisogno_totale.items():
                        # Usa la mappa per trovare l'oggetto Componente e recuperare il nome
                        componente_obj = dizionario_mappa_componenti.get(componente_codice)
                        if componente_obj:
                            output_text.insert(tk.END, f"{componente_obj.codice} - {componente_obj.nome}: {quantita}\n")
                        # Fallback come il blocco sopra
                        else:
                            output_text.insert(tk.END, f"{componente_codice}: {quantita} (Nome non disponibile)\n")

                    output_text.insert(tk.END, f"Totale Complessivo --> {fabbisogno_totale_int}pz <--\n")
                else:
                    output_text.insert(tk.END, "Nessun fabbisogno totale di componenti calcolato.\n")
            else:
                output_text.insert(tk.END, "Lotto non trovato.\n")

        # Funzione per calcolare il riepilogo della produzione, per il tab Riepilogo
        def calcola_riepilogo():
            selezionato = var_selezione.get()
            lotto = next((e for e in ListaLotti if str(e.id) == selezionato), None)
            output_riepilogo.delete("1.0", tk.END)

            if lotto:
                try:
                    # Recupero dei valori presenti enlla sezione dei parametri
                    # In particolare il numero di linee prod e assemblaggio deve essere almeno 1, quindi prende il massimo tra 1 e il contenuto della variabile
                    linee_prod = max(1, int(entry_linee_prod.get()))
                    linee_assem = max(1, int(entry_linee_assem.get()))
                    ore_giornata = float(entry_giorno_ore.get())
                except ValueError:
                    messagebox.showerror("Errore input", "Inserisci valori numerici validi nei parametri.")
                    return

                # Calcolo dei vari tempi totale
                tempo_componenti = sum(lotto.tempo_per_prodotto_componenti().values())
                tempo_assemblaggio = sum(lotto.tempo_per_prodotto_assemblaggio().values())

                # Calcolo del tempo reale diviso per linee produttive e assemblaggio
                tempo_componenti_eff = tempo_componenti / max(1, linee_prod)
                tempo_assemblaggio_eff = tempo_assemblaggio / max(1, linee_assem)
                tempo_totale_eff = tempo_componenti_eff + tempo_assemblaggio_eff
                ore_totali = tempo_totale_eff / 60

                # Verifica se la produzione supera la giornata lavorativo
                supera_giornata = ore_totali > ore_giornata

                # Calcolo della quantità totale di componenti da produrre
                fabbisogno_totale_dizionario = lotto.calcola_fabbisogno_totale()
                fabbisogno_totale = sum(fabbisogno_totale_dizionario.values())
                tot_quantita = sum(riga.quantita for riga in lotto.ordinativo)

                # Stampa del riepilogo nella teztarea
                output_riepilogo.insert(tk.END, f"========= RIEPILOGO LOTTO =========\n")
                output_riepilogo.insert(tk.END, f"ID Lotto: {lotto.id}\n")
                output_riepilogo.insert(tk.END, f"Numero righe lotto: {len(lotto.ordinativo)}\n")
                output_riepilogo.insert(tk.END, f"Quantità totale componenti da produrre: {fabbisogno_totale}\n")
                output_riepilogo.insert(tk.END, f"Quantità totale prodotti: {tot_quantita}\n\n")

                output_riepilogo.insert(tk.END, f"=========== PARAMETRI ============\n")
                output_riepilogo.insert(tk.END, f"Linee produttive: {linee_prod}\n")
                output_riepilogo.insert(tk.END, f"Linee assemblaggio: {linee_assem}\n")
                output_riepilogo.insert(tk.END, f"Durata giornata lavorativa: {ore_giornata} ore\n\n")

                output_riepilogo.insert(tk.END, f"========= TEMPO TOTALE ===========\n")
                output_riepilogo.insert(tk.END, f"Tempo componenti (minuti): {tempo_componenti:.2f}\n")
                output_riepilogo.insert(tk.END, f"Tempo assemblaggio (minuti): {tempo_assemblaggio:.2f}\n")
                output_riepilogo.insert(tk.END, f"Tempo componenti effettivo (minuti): {tempo_componenti_eff:.2f}\n")
                output_riepilogo.insert(tk.END, f"Tempo assemblaggio effettivo (minuti): {tempo_assemblaggio_eff:.2f}\n\n")

                output_riepilogo.insert(tk.END, f"============= ESITO ==============\n")
                output_riepilogo.insert(tk.END,f"Tempo totale effettivo: {tempo_totale_eff:.2f} minuti ({ore_totali:.2f} ore)\n")
                output_riepilogo.insert(tk.END, f"Supera giornata lavorativa? {'Sì' if supera_giornata else 'No'}\n\n")

                # Mostra la Label di avviso sotto alla textarea di riepilogo se il tempo di produzione supera la durata della giornata lavorativa
                avviso_supera_giornata(supera_giornata)
            else:
                output_riepilogo.insert(tk.END, "Lotto non trovato.\n")

        # Funzione per invocare sia la funzione calcolo del fabbisogno, sia del riepilogo
        def calcolo_produzione():
            calcola_fabbisogno()
            calcola_riepilogo()

        # Pulsante per invocare il calcolo della produzione, entrambe le funzioni combinante
        btn_simula_prod = ttk.Button(frame_sx, text="Avvio Calcolo - Simula Produzione", command=calcolo_produzione)
        btn_simula_prod.grid(row=4, column=0, pady=(15, 5), sticky="we")

        btn_reset = ttk.Button(frame_sx, text="Reset", command=lambda: (
            var_selezione.set(""),
            tabella.delete(*tabella.get_children()),
            output_text.delete("1.0", tk.END),
            output_riepilogo.delete("1.0", tk.END),
            entry_linee_prod.delete(0, tk.END),
            entry_linee_prod.insert(0, "1"),
            entry_linee_assem.delete(0, tk.END),
            entry_linee_assem.insert(0, "1"),
            entry_giorno_ore.delete(0, tk.END),
            entry_giorno_ore.insert(0, "8"),
            avviso_supera_giornata_reset()

        ))
        btn_reset.grid(row=5, column=0, pady=15, sticky="we")

        for i in range(8):
            frame_sx.grid_rowconfigure(i, weight=0)
        frame_sx.grid_rowconfigure(3, weight=1)

        # Funzione per creare la label di avviso del fatto che viene superata la singola giornata di produzione
        def avviso_supera_giornata(supera_giornata: bool):
            global label_risultato

            risultato = supera_giornata
            testo = "Supera la giornata lavorativa -> ✔️ Vero" if risultato else "Supera la giornata lavorativa -> ❌ Falso"
            colore = "green" if risultato else "red"

            # Se è già stata creata, aggiorna solo il contenuto
            if label_risultato:
                label_risultato.config(text=testo, foreground=colore)
            else:
                label_risultato = ttk.Label(tab_riepilogo, text=testo, foreground=colore)
                label_risultato.grid(row=2, column=0, sticky="w", pady=5)

        # Funzione per far sparire la label, se si preme il bottone di reset
        def avviso_supera_giornata_reset():
            global label_risultato
            if label_risultato:
                label_risultato.destroy()
                label_risultato = None

        # Funzione per aprire una finestra di dialogo per impostare il range di valori
        # Serve per permettere all'utente di definire i limiti minimi e massimi per la generazione casuale dei valori
        def apri_finestra_range(linea_target):
            global min_val_linea_assemblaggio, max_val_linea_assemblaggio, \
                min_val_linea_produttive, max_val_linea_produttive, \
                min_val_ore_giornata, max_val_ore_giornata

            # Impostazione dei valori predefiniti da visualizzare nella finestra
            minimo_corrente = None
            massimo_corrente = None
            nome_linea = ""

            if linea_target == 'assemblaggio':
                minimo_corrente = min_val_linea_assemblaggio
                massimo_corrente = max_val_linea_assemblaggio
                nome_linea = "Linea di Assemblaggio"
            elif linea_target == 'produttive':
                minimo_corrente = min_val_linea_produttive
                massimo_corrente = max_val_linea_produttive
                nome_linea = "Linea Produttiva"
            elif linea_target == 'ore_giornata':
                minimo_corrente = min_val_ore_giornata
                massimo_corrente = max_val_ore_giornata
                nome_linea = "Ore per Giornata"
            else:
                messagebox.showerror("Errore Interno", "Linea specificata non riconosciuta.")
                return

            # Creazione della finestra di input personalizzata
            finestra_dialogo = FinestraInputMinMax(finestra, f"Imposta intervallo per {nome_linea}", minimo_corrente,
                                                   massimo_corrente)
            valori_inseriti = finestra_dialogo.mostra()

            if valori_inseriti:  # L'utente ha confermato e i valori sono validi
                valore_minimo, valore_massimo = valori_inseriti

                # Assegna i valori ai parametri globali corretti
                if linea_target == 'assemblaggio':
                    minimo_linea_assemblaggio = valore_minimo
                    massimo_linea_assemblaggio = valore_massimo
                elif linea_target == 'produttive':
                    minimo_linea_produttive = valore_minimo
                    massimo_linea_produttive = valore_massimo
                elif linea_target == 'ore_giornata':
                    minimo_ore_giornata = valore_minimo
                    massimo_ore_giornata = valore_massimo


                messagebox.showinfo("Valori Salvati",
                                    f"{nome_linea}:\nMinimo = {valore_minimo}, Massimo = {valore_massimo}")
                finestra.focus_set()
            else:
                # L'utente ha annullato l'operazione
                messagebox.showinfo("Annullato", "Impostazione dell'intervallo annullata.")
                finestra.focus_set()

        # Classe per la finestra di dialogo che permette all'utente di inserire un valore minimo e massimo
        class FinestraInputMinMax(tk.Toplevel):
            def __init__(self, finestra_principale, titolo, valore_minimo_iniziale, valore_massimo_iniziale):
                super().__init__(finestra_principale)
                self.title(titolo)
                self.transient(finestra_principale)
                self.grab_set()
                self.risultato = None

                self.valore_minimo = valore_minimo_iniziale
                self.valore_massimo = valore_massimo_iniziale

                # Calcolo per centrare la finestra
                self.update_idletasks()
                posizione_x = finestra_principale.winfo_x() + (finestra_principale.winfo_width() // 2) - (
                            self.winfo_width() // 2)
                posizione_y = finestra_principale.winfo_y() + (finestra_principale.winfo_height() // 2) - (
                            self.winfo_height() // 2)
                self.geometry(f"+{posizione_x}+{posizione_y}")

                # Etichetta e campo per il valore minimo
                tk.Label(self, text="Valore Minimo:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
                self.campo_minimo = tk.Entry(self)
                self.campo_minimo.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
                if self.valore_minimo is not None:
                    self.campo_minimo.insert(0, str(self.valore_minimo))

                # Etichetta e campo per il valore massimo
                tk.Label(self, text="Valore Massimo:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
                self.campo_massimo = tk.Entry(self)
                self.campo_massimo.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
                if self.valore_massimo is not None:
                    self.campo_massimo.insert(0, str(self.valore_massimo))

                # Pulsante per confermare
                bottone_ok = tk.Button(self, text="OK", command=self._conferma)
                bottone_ok.grid(row=2, column=0, pady=10)

                # Pulsante per annullare
                bottone_annulla = tk.Button(self, text="Annulla", command=self._annulla)
                bottone_annulla.grid(row=2, column=1, pady=10)

                # Permette all'entry di espandersi in orizzontale
                self.grid_columnconfigure(1, weight=1)

                # Focus automatico sul primo campo
                self.campo_minimo.focus_set()

                # Gestione della chiusura della finestra
                self.protocol("WM_DELETE_WINDOW", self._annulla)

            def _conferma(self):
                try:
                    minimo = int(self.campo_minimo.get())
                    massimo = int(self.campo_massimo.get())

                    if minimo < 1:
                        messagebox.showerror("Errore", "Il valore minimo deve essere almeno 1.", parent=self)
                        return

                    if minimo > massimo:
                        messagebox.showerror("Errore", "Il valore minimo non può essere maggiore del valore massimo.",
                                             parent=self)
                        return

                    self.risultato = (minimo, massimo)
                    self.destroy()
                except ValueError:
                    messagebox.showerror("Errore", "Inserisci solo numeri interi.", parent=self)

            def _annulla(self):
                # L'utente ha scelto di non salvare
                self.risultato = None
                self.destroy()

            def mostra(self):
                # Attende che la finestra venga chiusa
                self.wait_window()
                return self.risultato

    # ========== Sezione 2 - Prodotti ==========
    def mostra_prodotti(self):
        # Creazione finestra
        finestra = tk.Toplevel(self.master)
        finestra.title("Prodotti")
        finestra.geometry("650x400")

        # Creazione tabella con prodotti disponibili
        label = tk.Label(finestra, text="Prodotti Disponibili", font=("Arial", 14))
        label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        tabella_prodotti = ttk.Treeview(finestra, columns=("Codice", "Nome", "Componenti", "Tempo Assemblaggio"),
                                             show="headings")
        for col in ("Codice", "Nome", "Componenti", "Tempo Assemblaggio"):
            tabella_prodotti.heading(col, text=col)
            tabella_prodotti.column(col, width=150)
        tabella_prodotti.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        def aggiorna_tabella():
            tabella_prodotti.delete(*tabella_prodotti.get_children())
            for p in ListaProdotti:
                componenti_descritti = [f"{cq.quantita}x{cq.componente.codice}" for cq in p.componenti]
                elenco_codici = ", ".join(componenti_descritti)
                tabella_prodotti.insert("", "end",
                                             values=(p.codice, p.nome, elenco_codici, p.tempo_assemblaggio_unitario))

        aggiorna_tabella()

        # Funzione per il popup invocato dai tasti di inserimento o modifica di un prodotto dopo averlo selezionato nella tabella
        def popup_prodotto(modifica=False):
            riga_selezionata = None
            prodotto_sel = None
            if modifica:
                selected = tabella_prodotti.selection()
                if not selected:
                    messagebox.showwarning("Attenzione", "Seleziona un prodotto da modificare")
                    finestra.focus_set()
                    return
                riga_selezionata = selected[0]
                valori = tabella_prodotti.item(riga_selezionata, "values")
                codice_sel = valori[0]
                prodotto_sel = next((p for p in ListaProdotti if p.codice == codice_sel), None)
                if prodotto_sel is None:
                    messagebox.showerror("Errore", "Prodotto non trovato")
                    finestra.focus_set()
                    return

            # Avvio del popup di modifica / inserimento
            popup = tk.Toplevel(finestra)
            popup.title("Modifica Prodotto" if modifica else "Aggiungi Prodotto")
            popup.geometry("400x400")

            # Etichetta Codice Prodotto
            tk.Label(popup, text="Codice:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            entry_codice = tk.Entry(popup)
            entry_codice.grid(row=0, column=1, padx=5, pady=5)
            # Genera il codice nel caso di nuovo prodotto e lo rende non modificabile
            if not modifica:
                aggiorna_codice_entry("P", ListaProdotti, entry_codice)
                entry_codice.config(state="disabled")

            # Bottone per modificare il codice prodotto - se si vuole != da quello generato
            btn_modcodice = ttk.Button(popup, text="Modifica", command=lambda: modifica_entry_on(entry_codice))
            btn_modcodice.grid(row=0, column=2, pady=5, sticky="we")

            # Se nella sezione modifica impedisce di
            # 1. modificare il codice prodotto
            # 2. generare codice prodotto
            if modifica:
                entry_codice.insert(0, prodotto_sel.codice)
                entry_codice.config(state="disabled")
                btn_modcodice.grid_remove()

            # Etichetta Nome Prodotto
            tk.Label(popup, text="Nome:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
            entry_nome = tk.Entry(popup)
            entry_nome.grid(row=1, column=1, padx=5, pady=5)

            # Se in modifica inserisce il nome del prodotto
            if modifica:
                entry_nome.insert(0, prodotto_sel.nome)

            # Etichetta Tempod di Assemblaggio Unitario
            tk.Label(popup, text="Tempo Assemblaggio Unitario:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
            entry_tempo = tk.Entry(popup)
            entry_tempo.grid(row=2, column=1, padx=5, pady=5)

            # Bottone per generare il Tempo di Assemblaggio Unitario
            btn_gentempo = ttk.Button(popup, text="Genera",
                                      command=lambda: valorizza_entry(Prodotto.genera_tempo_assemblaggio(),
                                                                      entry_tempo))
            btn_gentempo.grid(row=2, column=2, pady=5, sticky="we")

            # Se in modifica inserisce il valore nel campo di testo
            if modifica:
                entry_tempo.insert(0, str(prodotto_sel.tempo_assemblaggio_unitario))

            # Frame componenti con checkbox e quantità
            frame_comp = tk.LabelFrame(popup, text="Componenti", padx=10, pady=10)
            frame_comp.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

            # Per ogni componente della lista, crea checkbox + entry quantità
            var_comp = {}
            entries_quantita = {}

            # Funzione per gestire la spunta della checkbox
            def checkbox_spunta(codice):
                if var_comp[codice].get():
                    entries_quantita[codice].config(state="normal")
                    if entries_quantita[codice].get() == "":
                        entries_quantita[codice].insert(0, "1")
                else:
                    entries_quantita[codice].delete(0, "end")
                    entries_quantita[codice].config(state="disabled")

            # Intestazione dentro frame_comp
            listacomp_intestazione = tk.Label(frame_comp, text="- Nome Componente        Quantità",
                                              font=("Arial", 10, "normal"))
            listacomp_intestazione.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))

            row_idx = 1  # Inizia da riga 1 perché la riga 0 ora è intestazione

            for c in ListaComponenti:
                var = tk.BooleanVar()
                var_comp[c.codice] = var
                chk = tk.Checkbutton(frame_comp, text=f"{c.codice} - {c.nome}", variable=var,
                                     command=lambda cod=c.codice: checkbox_spunta(cod))
                chk.grid(row=row_idx, column=0, sticky="w")

                ent_q = tk.Entry(frame_comp, width=5)
                ent_q.grid(row=row_idx, column=1, padx=5)
                ent_q.config(state="disabled")
                entries_quantita[c.codice] = ent_q

                # Se in modifica, precompila checkbox e quantità
                if modifica and prodotto_sel:
                    found_cq = next((cq for cq in prodotto_sel.componenti if cq.componente.codice == c.codice), None)
                    if found_cq:
                        var_comp[c.codice].set(True)
                        ent_q.config(state="normal")
                        ent_q.insert(0, str(found_cq.quantita))
                row_idx += 1

            # Funzione per salvare il prodotto modificato o nuovo inserimento
            def salva_prodotto():
                codice = entry_codice.get().strip()
                nome = entry_nome.get().strip()
                try:
                    tempo_assemblaggio = float(entry_tempo.get())
                    finestra.focus_set()
                except ValueError:
                    messagebox.showerror("Errore", "Tempo Assemblaggio deve essere un numero valido")
                    return

                if not codice or not nome:
                    messagebox.showerror("Errore", "Codice e Nome sono obbligatori")
                    return
                if not modifica and any(p.codice == codice for p in ListaProdotti):
                    messagebox.showerror("Errore", "Codice prodotto già esistente")
                    return

                # Costruisci lista componenti selezionati
                comp_selezionati = []
                for cod, var in var_comp.items():
                    if var.get():
                        qtxt = entries_quantita[cod].get()
                        if not qtxt.isdigit() or int(qtxt) <= 0:
                            messagebox.showerror("Errore",
                                                 f"Quantità per componente {cod} deve essere un intero positivo")
                            return
                        quantita = int(qtxt)
                        componente = next((c for c in ListaComponenti if c.codice == cod), None)
                        if componente:
                            comp_selezionati.append(ComponenteQuantificato(componente=componente, quantita=quantita))

                if modifica and prodotto_sel:
                    prodotto_sel.nome = nome
                    prodotto_sel.tempo_assemblaggio_unitario = tempo_assemblaggio
                    prodotto_sel.componenti = comp_selezionati
                else:
                    nuovo_prodotto = Prodotto(codice=codice, nome=nome, componenti=comp_selezionati,
                                              tempo_assemblaggio_unitario=tempo_assemblaggio)
                    ListaProdotti.append(nuovo_prodotto)

                aggiorna_tabella()
                popup.destroy()
                finestra.focus_set()

            btn_salva = tk.Button(popup, text="Salva", command=salva_prodotto)
            btn_salva.grid(row=4, column=0, columnspan=2, pady=15)

        # Funzione per eliminare un prodotto
        def elimina_prodotto():
            selected = tabella_prodotti.selection()
            if not selected:
                messagebox.showwarning("Attenzione", "Seleziona un prodotto da eliminare")
                return
            item = selected[0]
            valori = tabella_prodotti.item(item, "values")
            codice_sel = valori[0]

            if messagebox.askyesno("Conferma", f"Eliminare prodotto {codice_sel}?"):
                global ListaProdotti
                ListaProdotti = [p for p in ListaProdotti if p.codice != codice_sel]
                aggiorna_tabella()
                finestra.focus_set()

        # Bottini a fondo tabella
        button_aggiungi = ttk.Button(finestra, text="Aggiungi Prodotto", command=lambda: popup_prodotto(modifica=False))
        button_aggiungi.grid(row=2, column=0, padx=10, pady=10)
        button_modifica = ttk.Button(finestra, text="Modifica Prodotto", command=lambda: popup_prodotto(modifica=True))
        button_modifica.grid(row=2, column=1, padx=10, pady=10)
        button_elimina = ttk.Button(finestra, text="Elimina Prodotto", command=elimina_prodotto)
        button_elimina.grid(row=2, column=2, padx=10, pady=10)

    # ========== Sezione 3 - Componenti ==========
    def mostra_componenti(self):
        # Creazione Finestra
        finestra = tk.Toplevel(self.master)
        finestra.title("Componenti")
        finestra.geometry("700x400")

        # Label titolo
        label = tk.Label(finestra, text="Componenti Disponibili", font=("Arial", 14))
        label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # Tabella componenti
        self.tabella_componenti = ttk.Treeview(finestra,
                                               columns=("Codice", "Nome", "Tempo Produzione (min)", "Scarto (%)"),
                                               show="headings")
        for col in ("Codice", "Nome", "Tempo Produzione (min)", "Scarto (%)"):
            self.tabella_componenti.heading(col, text=col)
            self.tabella_componenti.column(col, width=150)
        self.tabella_componenti.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Popola tabella
        def aggiorna_tabella():
            self.tabella_componenti.delete(*self.tabella_componenti.get_children())
            for c in ListaComponenti:
                self.tabella_componenti.insert("", "end", values=(c.codice, c.nome, c.tempo_produzione_unitario,
                                                                  c.percentuale_scarto))

        aggiorna_tabella()

        # Funzione analoga a sezione 2 senza la parte di componenti selezionabili
        def popup_componente(modifica=False):
            riga_selezionata = None
            componente_sel = None
            if modifica:
                selected = self.tabella_componenti.selection()
                if not selected:
                    messagebox.showwarning("Attenzione", "Seleziona un componente da modificare")
                    finestra.focus_set()
                    return
                riga_selezionata = selected[0]
                valori = self.tabella_componenti.item(riga_selezionata, "values")
                codice_sel = valori[0]
                componente_sel = next((c for c in ListaComponenti if c.codice == codice_sel), None)
                if not componente_sel:
                    messagebox.showerror("Errore", "Componente non trovato")
                    return

            popup = tk.Toplevel(finestra)
            popup.title("Modifica Componente" if modifica else "Aggiungi Componente")
            popup.geometry("450x250")

            # Codice
            tk.Label(popup, text="Codice").grid(row=0, column=0, padx=5, pady=5)
            entry_codice = tk.Entry(popup)
            entry_codice.grid(row=0, column=1, padx=5, pady=5)
            # Genera il codice nel caso di nuovo prodotto e lo rende non modificabile
            if not modifica:
                aggiorna_codice_entry("C", ListaComponenti, entry_codice)
                entry_codice.config(state="disabled")

            btn_modcodice = ttk.Button(popup, text="Modifica", command=lambda: modifica_entry_on(entry_codice))
            btn_modcodice.grid(row=0, column=2, pady=5)

            if modifica:
                entry_codice.insert(0, componente_sel.codice)
                entry_codice.config(state="disabled")
                btn_modcodice.grid_remove()

            # Nome
            tk.Label(popup, text="Nome").grid(row=1, column=0, padx=5, pady=5)
            entry_nome = tk.Entry(popup)
            entry_nome.grid(row=1, column=1, padx=5, pady=5)

            # Tempo Produzione
            tk.Label(popup, text="Tempo Produzione Unitario (min)").grid(row=2, column=0, padx=5, pady=5)
            entry_tempo = tk.Entry(popup)
            entry_tempo.grid(row=2, column=1, padx=5, pady=5)
            # Bottone per generare il Tempo di Produzione
            btn_gentempo = ttk.Button(popup, text="Genera",
                                      command=lambda: valorizza_entry(ComponenteProdotto.genera_tempo_produzione(),
                                                                      entry_tempo))
            btn_gentempo.grid(row=2, column=2, pady=5, sticky="we")

            # Scarto
            tk.Label(popup, text="Percentuale Scarto (%)").grid(row=3, column=0, padx=5, pady=5)
            entry_scarto = tk.Entry(popup)
            entry_scarto.grid(row=3, column=1, padx=5, pady=5)
            # Bottone per generare lo scarto
            btn_gentempo = ttk.Button(popup, text="Genera",
                                      command=lambda: valorizza_entry(ComponenteProdotto.genera_percentuale_scarto(),
                                                                      entry_scarto))
            btn_gentempo.grid(row=3, column=2, pady=5, sticky="we")

            if modifica:
                entry_nome.insert(0, componente_sel.nome)
                entry_tempo.insert(0, str(componente_sel.tempo_produzione_unitario))
                entry_scarto.insert(0, str(componente_sel.percentuale_scarto))

            # Funzione analoga a sez.2
            def salva_componente():
                codice = entry_codice.get().strip()
                nome = entry_nome.get().strip()
                try:
                    tempo = float(entry_tempo.get())
                    scarto = float(entry_scarto.get())
                    finestra.focus_set()
                except ValueError:
                    messagebox.showerror("Errore", "Tempo e Scarto devono essere numeri validi")
                    return

                if not codice or not nome:
                    messagebox.showerror("Errore", "Codice e Nome sono obbligatori")
                    return
                if not modifica and any(c.codice == codice for c in ListaComponenti):
                    messagebox.showerror("Errore", "Codice componente già esistente")
                    return

                if modifica:
                    componente_sel.nome = nome
                    componente_sel.tempo_produzione_unitario = tempo
                    componente_sel.percentuale_scarto = scarto
                else:
                    nuovo = ComponenteProdotto(
                        codice=codice,
                        nome=nome,
                        tempo_produzione_unitario=tempo,
                        percentuale_scarto=scarto
                    )
                    ListaComponenti.append(nuovo)

                aggiorna_tabella()
                popup.destroy()

            tk.Button(popup, text="Salva", command=salva_componente).grid(row=4, column=0, columnspan=2, pady=15)

        # Funzione elimina componente - analoga  a sez.2
        def elimina_componente():
            selected = self.tabella_componenti.selection()
            if not selected:
                messagebox.showwarning("Attenzione", "Seleziona un componente da eliminare")
                return
            item = selected[0]
            valori = self.tabella_componenti.item(item, "values")
            codice_sel = valori[0]

            if messagebox.askyesno("Conferma", f"Eliminare componente {codice_sel}?"):
                global ListaComponenti
                ListaComponenti = [c for c in ListaComponenti if c.codice != codice_sel]
                aggiorna_tabella()
                finestra.focus_set()

        # Bottoni
        button_aggiungi = ttk.Button(finestra, text="Aggiungi Componente",
                                     command=lambda: popup_componente(modifica=False))
        button_aggiungi.grid(row=2, column=0, padx=10, pady=10)
        button_modifica = ttk.Button(finestra, text="Modifica Componente",
                                     command=lambda: popup_componente(modifica=True))
        button_modifica.grid(row=2, column=1, padx=10, pady=10)
        button_elimina = ttk.Button(finestra, text="Elimina Componente", command=elimina_componente)
        button_elimina.grid(row=2, column=2, padx=10, pady=10)

    # ========== Sezione 4 - Lotti ==========
    def mostra_lotti(self):
        # Creazione finestra
        finestra = tk.Toplevel(self.master)
        finestra.title("Gestione Lotti")
        finestra.geometry("800x450")

        # Creazione frame
        sinistra = tk.Frame(finestra)
        sinistra.pack(side="left", fill="y", padx=10, pady=10)

        destra = tk.Frame(finestra)
        destra.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Lista lotti
        # Sezione SX
        tk.Label(sinistra, text="Lotti", font=("Arial", 12, "bold")).pack()
        lista_lotti = tk.Listbox(sinistra, height=20, width=30)
        lista_lotti.pack(fill="y")

        # CREA UN FRAME PER LE ETICHETTE SUPERIORI
        header_frame = tk.Frame(destra)
        # Impacchetta il frame in alto, riempi l'asse X. Questo pack non cambia.
        header_frame.pack(side="top", fill="x", pady=5)

        # --- Etichetta Testata Lotto (dentro il nuovo frame, usa grid) ---
        lbl_testata_lotto = tk.Label(header_frame, text="Testata Lotto", font=("Arial", 16, "bold"))
        # Posiziona l'etichetta al centro del frame usando grid
        lbl_testata_lotto.grid(row=0, column=0, columnspan=2, pady=(15, 5), sticky="nsew")
        # column=0, columnspan=2 permette all'etichetta di centrare su due colonne logiche

        lotto_selezionato_var = tk.StringVar(
            value=f"Lotto Selezionato: Nessun Lotto Selezionato")  # Imposta un valore iniziale
        lbl_lotto_selezionato = tk.Label(header_frame, textvariable=lotto_selezionato_var,
                                              font=("Arial", 12))
        lbl_lotto_selezionato.grid(row=1, column=0, columnspan=2, pady=(0, 5), sticky="nsew")

        ttk.Button(header_frame, text="Modifica Righe", command=lambda: apri_editor_righe()).grid(row=1, column=2,
                                                                                                       pady=10)

        # Configura l'espansione delle colonne nel header_frame per centrare il contenuto
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=1)

        for lotto in ListaLotti:
            lista_lotti.insert("end", f"Lotto {lotto.id}")

        def aggiungi_lotto():
            codice = genera_codice_id("L", ListaLotti)
            #nuovo_lotto = LottoProduzione(id=int(codice), ordinativo=[])
            nuovo_lotto = LottoProduzione(id=codice, ordinativo=[])
            ListaLotti.append(nuovo_lotto)
            lista_lotti.insert("end", f"Lotto {codice}")
            messagebox.showinfo("Nuovo Lotto", f"ID assegnato: {codice}")
            finestra.focus_set()

        def elimina_lotto():
            selection = lista_lotti.curselection()
            if not selection:
                return
            idx = selection[0]
            if messagebox.askyesno("Conferma", "Eliminare questo lotto?"):
                del ListaLotti[idx]
                lista_lotti.delete(idx)
                tabella_righe.delete(*tabella_righe.get_children())
                finestra.focus_set()

        tk.Button(sinistra, text="Aggiungi Lotto", command=aggiungi_lotto).pack(pady=5, fill="x")
        tk.Button(sinistra, text="Elimina Lotto", command=elimina_lotto).pack(pady=5, fill="x")



        # Tabella righe lotto
        tabella_righe = ttk.Treeview(destra, columns=("Codice", "Nome", "Quantità"), show="headings")
        for col in ("Codice", "Nome", "Quantità"):
            tabella_righe.heading(col, text=col)
            tabella_righe.column(col, width=180)
        tabella_righe.pack(fill="both", expand=True)

        def mostra_righe_lotto(event=None):
            selection = lista_lotti.curselection()
            if not selection:
                tabella_righe.delete(*tabella_righe.get_children())
                lotto_selezionato_var.set(f"Lotto Selezionato: Nessun Lotto Selezionato")
                return
            indice = selection[0]
            lotto = ListaLotti[indice]
            tabella_righe.delete(*tabella_righe.get_children())
            for riga in lotto.ordinativo:
                p = riga.prodotto
                tabella_righe.insert("", "end", values=(p.codice, p.nome, riga.quantita))

            # Valorizza la Label dell'ID del lotto:

            lotto_selezionato_var.set(f"Lotto Selezionato: {lotto.id}")

        lista_lotti.bind("<<ListboxSelect>>", mostra_righe_lotto)

        def apri_editor_righe():
            selection = lista_lotti.curselection()
            if not selection:
                return
            idx = selection[0]
            lotto = ListaLotti[idx]

            editor = tk.Toplevel(finestra)
            editor.title(f"Modifica Righe - Lotto {lotto.id}")
            editor.geometry("800x400")

            # Variabili e riferimenti per i controlli min/max (NON usano self)
            min_qty_var = tk.StringVar(value="1")
            max_qty_var = tk.StringVar(value="10")
            edit_confirm_btn_text = tk.StringVar(value="Modifica Parametri")

            # Riferimenti ai widget (servono per configurarne lo stato)
            min_qty_entry_ref = None
            max_qty_entry_ref = None
            edit_confirm_btn_ref = None  # Questo sarà il bottone Modifica/Conferma

            tk.Label(editor, text=f"ID Lotto (in modifica): {lotto.id}").grid(row=0, column=0, padx=5, pady=5,
                                                                              sticky="w")
            tk.Label(editor, text=f"Parametri Genera Qty: min / max").grid(row=0, column=1, padx=5, pady=5, sticky="w")
            min_qty_entry_ref = tk.Entry(editor, textvariable=min_qty_var, width=5)
            min_qty_entry_ref.grid(row=0, column=2, padx=2, pady=5, sticky="ew")

            tk.Label(editor, text="/").grid(row=0, column=3, padx=0, pady=5, sticky="w")

            max_qty_entry_ref = tk.Entry(editor, textvariable=max_qty_var, width=5)
            max_qty_entry_ref.grid(row=0, column=4, padx=2, pady=5, sticky="ew")

            colonne = ["Codice", "Nome", "Quantità", "Azioni"]
            for col_index, label in enumerate(colonne):
                tk.Label(editor, text=label, font=("Arial", 10, "bold")).grid(row=1, column=col_index, padx=5, pady=5)

            entry_rows = []

            def aggiorna_nome_quantita(event, nome_entry, quantita_entry, prodotto_var):
                codice = prodotto_var.get()
                prodotto = next((p for p in ListaProdotti if p.codice == codice), None)
                if prodotto:
                    nome_entry.delete(0, tk.END)
                    nome_entry.insert(0, prodotto.nome)
                    quantita_entry.delete(0, tk.END)
                    quantita_entry.insert(0, "1")

            def aggiungi_riga(p=None, q=None):
                row_index = len(entry_rows) + 2

                prodotto_var = tk.StringVar()
                codice_menu = ttk.Combobox(editor, textvariable=prodotto_var)
                codice_menu["values"] = [p.codice for p in ListaProdotti]
                if p:
                    prodotto_var.set(p.codice)
                codice_menu.grid(row=row_index, column=0, padx=5, pady=2)

                nome_entry = tk.Entry(editor)
                nome_entry.insert(0, p.nome if p else "")
                nome_entry.grid(row=row_index, column=1, padx=5, pady=2)
                quantita_entry = tk.Entry(editor)
                quantita_entry.insert(0, str(q) if q else "")
                quantita_entry.grid(row=row_index, column=2, padx=5, pady=2)

                btn_elimina = tk.Button(editor, text="Elimina")
                btn_elimina.grid(row=row_index, column=3, padx=5, pady=2)

                btn_genera_qty = tk.Button(editor, text="Genera Quantità", command=lambda: valorizza_entry(
                    genera_random_int(int(min_qty_var.get()), int(max_qty_var.get())), quantita_entry))
                btn_genera_qty.grid(row=row_index, column=4, padx=5, pady=2)

                # Funzione pr eliminare la una riga - invocata da btn
                def elimina_corrente():
                    codice_menu.destroy()
                    nome_entry.destroy()
                    quantita_entry.destroy()
                    btn_elimina.destroy()
                    entry_rows.remove(row)
                    btn_genera_qty.destroy()

                btn_elimina.config(command=elimina_corrente)

                codice_menu.bind("<<ComboboxSelected>>",
                                 lambda e: aggiorna_nome_quantita(e, nome_entry, quantita_entry, prodotto_var))

                row = (prodotto_var, nome_entry, quantita_entry)
                entry_rows.append(row)

            for riga in lotto.ordinativo:
                aggiungi_riga(riga.prodotto, riga.quantita)

            def salva_modifiche():
                nuove_righe = []
                for row in entry_rows:
                    if not row:
                        continue
                    codice = row[0].get()
                    nome = row[1].get()
                    try:
                        quantita = int(row[2].get())
                    except ValueError:
                        continue
                    prodotto = next((p for p in ListaProdotti if p.codice == codice), None)
                    if prodotto:
                        nuove_righe.append(RigaLotto(prodotto=prodotto, quantita=quantita))
                lotto.ordinativo = nuove_righe
                editor.destroy()
                mostra_righe_lotto()
                finestra.focus_set()

            tk.Button(editor, text="Aggiungi Riga", command=aggiungi_riga).grid(row=999, column=0, pady=15)
            tk.Button(editor, text="Salva", command=salva_modifiche).grid(row=999, column=1, pady=15)
            tk.Button(editor, text="Chiudi", command=editor.destroy).grid(row=999, column=2, pady=15)

            # Funzione nidificata per gestire lo stato del bottone e delle entry min/max
            def toggle_min_max_edit_mode_nested():
                current_text = edit_confirm_btn_text.get()
                if current_text == "Modifica Parametri":
                    min_qty_entry_ref.config(state="normal")
                    max_qty_entry_ref.config(state="normal")
                    edit_confirm_btn_text.set("Conferma Parametri")
                else:  # current_text == "Conferma Parametri"
                    try:
                        min_val = int(min_qty_var.get())
                        max_val = int(max_qty_var.get())

                        if min_val <= 0 or max_val <= 0:
                            messagebox.showerror("Errore Input",
                                                 "I valori min e max devono essere numeri interi positivi.")
                            return

                        if min_val > max_val:
                            messagebox.showerror("Attenzione",
                                                 "Il valore minimo non può essere maggiore del valore massimo. ")
                            min_qty_entry_ref.config(state="normal")  # Lascia editabile per correzione
                            max_qty_entry_ref.config(state="normal")
                            edit_confirm_btn_text.set("Conferma Parametri")
                            return

                        min_qty_entry_ref.config(state="readonly")
                        max_qty_entry_ref.config(state="readonly")
                        edit_confirm_btn_text.set("Modifica Parametri")
                    except ValueError:
                        messagebox.showerror("Errore Input", "I valori min e max devono essere numeri interi validi.")
                        min_qty_entry_ref.config(state="normal")  # Lascia editabile per correzione
                        max_qty_entry_ref.config(state="normal")
                        edit_confirm_btn_text.set("Conferma Parametri")

            edit_confirm_btn_ref = tk.Button(editor, textvariable=edit_confirm_btn_text,
                                             command=toggle_min_max_edit_mode_nested)
            edit_confirm_btn_ref.grid(row=0, column=5, padx=5, pady=5, sticky="w")

            # Imposta le Entry min/max come readonly inizialmente
            min_qty_entry_ref.config(state="readonly")
            max_qty_entry_ref.config(state="readonly")


# =========================
# Main
# =========================
#if __name__ == "__main__":
#    root = tk.Tk()
#    app = Applicazione(root)
#    root.mainloop()
