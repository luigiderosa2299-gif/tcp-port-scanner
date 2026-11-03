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

## V2 — Multithreading

La scansione ora distribuisce i controlli di porta su un pool di 100 thread paralleli (`concurrent.futures.ThreadPoolExecutor`), invece di testare le porte una alla volta in sequenza. Comportamento verificato empiricamente catturando il traffico generato: con il multithreading attivo, i pacchetti SYN mostrano timestamp identici fino al microsecondo e arrivano fuori dall'ordine numerico delle porte — entrambi segni inequivocabili di connessioni realmente concorrenti, non solo di un output più rapido.

## Verifica con cattura di pacchetti

Il comportamento dello scanner è stato validato catturando il traffico di rete reale generato durante l'esecuzione, non solo osservando l'output — vedi [`docs/packet-capture-verification.md`](docs/packet-capture-verification.md) per l'evidenza completa (cattura tcpdump V1 che conferma un pacchetto SYN per ogni porta testata, e cattura V2 che conferma l'esecuzione realmente parallela introdotta dal multithreading).

## Stack tecnico

- **Python 3** — nessuna libreria esterna oltre alla standard library (`socket`, `argparse`, `concurrent.futures`)
- **socket** — comunicazione di rete TCP a basso livello
- **argparse** — interfaccia a riga di comando (host e intervallo di porte come parametri, non valori fissi nel codice)
- **concurrent.futures.ThreadPoolExecutor** — esecuzione parallela dei controlli di porta

## Possibili estensioni future

- Banner grabbing dedicato per altri protocolli request-first (es. HTTPS via TLS, SMTP con comando EHLO esplicito).

## Nota etica

Scansioni eseguite esclusivamente contro macchine di mia proprietà in laboratorio locale isolato (VM Kali su rete domestica). Non utilizzare contro sistemi di cui non si ha autorizzazione esplicita.
