# Verifica con cattura di pacchetti (tcpdump)

Per confermare che lo scanner esegue davvero un tentativo di connessione per **ogni** porta dichiarata nell'intervallo (e non, ad esempio, si ferma prematuramente o salta porte per un bug silenzioso), il traffico generato durante l'esecuzione è stato catturato in tempo reale sulla macchina bersaglio.

## Setup

- **Sorgente scansione**: Mac (`192.168.1.196`)
- **Bersaglio**: VM Kali Linux (`192.168.1.95`)
- **Cattura eseguita su**: Kali, con il bersaglio stesso in ascolto del proprio traffico in ingresso

## Comando di cattura

```bash
sudo tcpdump -i eth0 -nn "tcp[tcpflags] & tcp-syn != 0 and src host 192.168.1.196"
```

Filtra solo i pacchetti con flag **SYN** attivo (il primo pacchetto del three-way handshake TCP, inviato per ogni tentativo di connessione) provenienti dal Mac che esegue lo scan.

## Evidenza raccolta

Estratto della cattura durante una scansione `--start 1 --end 1024`:

```
07:49:16.552954 IP 192.168.1.196.60527 > 192.168.1.95.1: Flags [S], seq 45900052, ...
07:49:16.553276 IP 192.168.1.196.60528 > 192.168.1.95.2: Flags [S], seq 1597598637, ...
07:49:16.553483 IP 192.168.1.196.60529 > 192.168.1.95.3: Flags [S], seq 3743083537, ...
...
07:49:16.556937 IP 192.168.1.196.60548 > 192.168.1.95.22: Flags [S], seq 2510801004, ...
...
```

Il pacchetto SYN verso la porta **22** (visibile nell'estratto) coincide esattamente con la porta che lo script riporta come aperta — conferma diretta, a livello di pacchetto di rete, che il risultato riportato dallo script corrisponde a un vero tentativo di connessione TCP e non a un valore inventato o cache.

## Conclusione

La sequenza di porte di destinazione osservata nella cattura (1, 2, 3, 4, ... in ordine, senza salti) corrisponde esattamente all'intervallo richiesto a riga di comando (`range(args.start, args.end)`), confermando che lo scanner tenta sistematicamente ogni porta dell'intervallo dichiarato, senza eccezioni silenziose.
