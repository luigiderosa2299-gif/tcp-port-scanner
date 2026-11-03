# TCP Port Scanner & Banner Grabber

Scanner di porte TCP scritto da zero in Python, con rilevamento del servizio in ascolto tramite banner grabbing (sia per protocolli "talk-first" come SSH, sia per HTTP tramite richiesta attiva).

## Obiettivo

Costruire da zero — senza usare librerie di scanning preconfezionate — uno strumento che replica i meccanismi fondamentali di `nmap`: verificare lo stato di una porta TCP e identificare il servizio in ascolto, capendo ogni passaggio invece di limitarsi a usare uno strumento esistente come scatola nera.

## Come funziona

1. **Connect scan TCP**: per ogni porta nell'intervallo richiesto, tenta una connessione TCP completa (`socket.connect_ex`). Se la connessione riesce (codice di ritorno `0`), la porta è aperta.
2. **Banner grabbing a doppio tentativo**:
   - Primo tentativo: ascolto passivo — funziona per servizi che inviano un banner spontaneo alla connessione (es. SSH).
   - Secondo tentativo (solo se il primo non produce nulla): invio di una richiesta HTTP minima (`GET / HTTP/1.0`) e lettura della risposta — funziona per servizi web che rispondono solo su richiesta esplicita.

## Utilizzo

```bash
python3 scanner.py <host> [--start PORTA_INIZIALE] [--end PORTA_FINALE]
```

Esempio:
```bash
python3 scanner.py 192.168.1.95 --start 1 --end 1024
```

## Esempio di output reale

```
Porta 22 aperta - Banner: SSH-2.0-OpenSSH_10.5p1 Debian-1
Porta 8000 aperta - Banner: HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.14.7
Date: Tue, 03 Nov 2026 00:15:06 GMT
Content-type: text/html; charset=utf-8
```

## Verifica con cattura di pacchetti

Il comportamento dello scanner è stato validato catturando il traffico di rete reale generato durante l'esecuzione, non solo osservando l'output — vedi [`docs/packet-capture-verification.md`](docs/packet-capture-verification.md) per l'evidenza completa (cattura tcpdump che conferma un pacchetto SYN per ogni porta effettivamente testata).

## Stack tecnico

- **Python 3** — nessuna libreria esterna, solo moduli standard (`socket`, `argparse`)
- **socket** — comunicazione di rete TCP a basso livello
- **argparse** — interfaccia a riga di comando (host e intervallo di porte come parametri, non valori fissi nel codice)

## Possibili estensioni future

- **Multithreading** (`concurrent.futures.ThreadPoolExecutor`) per velocizzare la scansione eseguendo più controlli di porta in parallelo, utile soprattutto contro bersagli remoti con latenza più alta o porte filtrate che vanno in timeout.
- Banner grabbing dedicato per altri protocolli request-first (es. HTTPS via TLS, SMTP con comando EHLO esplicito).

## Nota etica

Scansioni eseguite esclusivamente contro macchine di mia proprietà in laboratorio locale isolato (VM Kali su rete domestica). Non utilizzare contro sistemi di cui non si ha autorizzazione esplicita.
