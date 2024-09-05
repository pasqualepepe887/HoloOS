import subprocess
import os

# Specifica la cartella da controllare
directory = '/home/HoloOS/GUI_TK/'  # Sostituisci con il percorso della tua cartella

# Costruisci il percorso completo del file config.txt
config_path = os.path.join(directory, 'config.txt')

# Controlla se il file config.txt esiste nella cartella
if os.path.isfile(config_path):
    # Se config.txt esiste, avvia main.py
    script_to_run = os.path.join(directory, 'main.py')
    print(f"Esecuzione di {script_to_run}")
else:
    # Se config.txt non esiste, avvia config.py
    script_to_run = os.path.join(directory, 'config.py')
    print(f"Esecuzione di {script_to_run}")

# Avvia lo script appropriato
subprocess.run(['python3', script_to_run])
