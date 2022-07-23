Nel file carlacfg.py si configura il path del sistema CARLA (variabile CARLA_LIB_PATH).
Questo path serve per l'import dinamico della libreria.

Il programma principale è su main.py.
Di seguito si descrivono le parti principali del main.

Sono impostate delle costanti di configurazione:
    FPS = 25                # fps del sistema
    USE_WHEEL = True        # si abilita uso dello volante G29
    USE_JOYSTICK = False    # si abilita il joystick (nota: è alternativo al volante).
    START_AUTOPILOT = True  # il veicolo si avvia in modo autopilot
    USE_WEBCAM = True       # si abilita il capture della webcam

    ROOTPATHRECORDING = "H:/_dataCollect/"   # base path ove salvare i dati raccolti

Ogni volta che si avvia una sessione di guida il sistema crea in automatico una cartella all'interno del base path
con una numerazione progressiva. In questo modo i dati di ogni sessione di guida sono salvati in modo distinto.

Il sistema consente di scgliere la mappa.


La registrazione di tutti i dati viene svolta da una classe che centralizza i salvataggi [recorder.py].

Nella fase preliminare di avvio del sistema vengono effettuate le seguenti azioni principali:
    - creazione del world
    - creazione del veicolo
    - creazione di tre camere semantiche (una posizionata a sinistra, una centrale e una a destra)
    - lidar con una scansione a 360° a frequenza FPS, in modo tale che ad ogni fotogramma ci sia una scansione totale
    - creazione di una camera floating per mostrare l'auto che si sta guidando con HUD
    - attivazione della webcam (a risoluzione 320x240)
    - attivazione dei controlli della tastiera e [volanteG29 OR joystick]


I controlli della tastiera sono:
  ARROW-UP:     accelerazione
  ARROW-DOWN:   freno
  ARROW-LEFT:   sterzare a sinistra
  ARROW-RIGHT:  sterzare a destra
  RETURN:       switch autopilot/manual (se manual il veicolo è sempre pilotabile da tastiera e, se attivo, da volante/joystick
  ESC:          terminazione del programma

Il salvataggio dei dati vengono salvati ad ogni frame in modo sincrono.
Tutti i dati fanno riferimento ad un timestamp che è uguale al numero dei millisecondi.

Formato di salvataggio dati:
    CAMERA SEMANTICA: fa 3 file in formato npz (sinistra, destra, centrale)
    WEB-CAMERA: crea una cartella "webcam" dove all'interno inserisce tutti i fotogrammi in formato png.
                Il nome del file riporta il timestamp.
    LIDAR: crea una cartella "lidar_sensor" dove all'interno inserisce un file per ogni timestamp in fomrato ply
    CONTROLLI DEL VEICOLO: crea un file "vehicle_controls.npy" che riporta il timestamp i dati dello sterzo,
                           accelerazione e freno.
    SPEED:  crea un file "vehicle.npy" che riporta la velocità della macchina in ogni timestamp.


Nella cartella "viewers" sono presente delle classi di utilità per leggere/visualizzare i dati.
In particolare la classe in vehicleDataViewer.py consente anche di esportare i dati del veicolo in formato EXCEL.

La fase finale del programma effettua il dispose di tutti gli oggetti, ed il programma si chiude regolarmente.

