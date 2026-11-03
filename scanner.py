import socket
import argparse

parser = argparse.ArgumentParser(description="Scanner di porte TCP")
parser.add_argument("host", help="indirizzo IP da scansionare")
parser.add_argument("--start", type=int, default=1, help="Porta iniziale")
parser.add_argument("--end", type=int, default=1024, help="Porta finale")
args = parser.parse_args()


def grab_banner(sock, port):
    try:
        banner = sock.recv(1024).decode(errors="ignore").strip()
        if banner:
            return banner
    except socket.timeout:
        pass
    except:
        return "nessun banner ricevuto"

    try:
        sock.send(b"GET / HTTP/1.0\r\n\r\n")
        banner = sock.recv(1024).decode(errors="ignore").strip()
        return banner
    except:
        return "nessun banner ricevuto"


def scan_port(host, port, timeout=1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    risultato = sock.connect_ex((host, port))
    if risultato == 0:
        banner = grab_banner(sock, port)
        sock.close()
        return True, banner
    else:
        sock.close()
        return False, None


for porta in range(args.start, args.end):
    aperta, banner = scan_port(args.host, porta)
    if aperta:
        print(f"Porta {porta} aperta - Banner: {banner}")
