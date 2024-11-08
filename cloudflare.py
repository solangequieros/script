import subprocess
import threading
import time
import socket
import sys

def iframe_thread(port):
    while True:
        time.sleep(0.5)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        if result == 0:
            break
        sock.close()
    
    print("\nComfyUI finished loading, trying to launch cloudflared (if it gets stuck here cloudflared is having issues)\n")

    try:
        p = subprocess.Popen(["cloudflared", "tunnel", "--url", f"http://127.0.0.1:{port}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for line in p.stderr:
            l = line.decode()
            if "trycloudflare.com " in l:
                print("This is the URL to access ComfyUI:", l[l.find("http"):], end='')
    except Exception as e:
        print(f"Failed to launch cloudflared: {e}")

def main(port):
    # Iniciar a thread que verifica a porta
    threading.Thread(target=iframe_thread, daemon=True, args=(port,)).start()

    # Executar o comando para iniciar o ComfyUI
    try:
        subprocess.run(["python", "main.py", "--dont-print-server"])
    except Exception as e:
        print(f"Failed to run ComfyUI: {e}")

if __name__ == "__main__":
    port = 8188  # Você pode alterar a porta conforme necessário
    main(port)
