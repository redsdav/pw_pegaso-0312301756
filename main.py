# Main
# Davide Rossi
# PW - Traccia 1.5
# Versione Python 3.11

#--------IMPORT-------------
from gui import Applicazione
import tkinter as tk
#--------FINE IMPORT-------------
 
#---------ISTANZE------------------------------
# le istanze sono contenute nel file dati.py
#--------- FINE ISTANZE------------------------------

#--------- MAIN ---------------------

def main():
    print("Avvio dell'app...")

    print("--------------@----------------")
    
    # Parte di Avvio Applicazione
    root = tk.Tk()
    Applicazione(root)
    root.mainloop()


if __name__ == "__main__":
    main()


#--------- FINE MAIN ---------------------

