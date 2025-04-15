import socket
import cups

HOST = '0.0.0.0'
PORT = 9100

# CUPS bağlantısını oluştur
conn_cups = cups.Connection()
printer_name = conn_cups.getDefault()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Dinleniyor: {HOST}:{PORT}")
    
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Bağlandı: {addr}")
            data = b''
            while True:
                packet = conn.recv(4096)
                if not packet:
                    break
                data += packet
            
            if data:
                # Veriyi geçici bir dosyaya yaz
                with open("/tmp/tcp_print_job.txt", "wb") as f:
                    f.write(data)
                
                # Yazdırma işlemi
                conn_cups.printFile(printer_name, "/tmp/tcp_print_job.txt", "TCP Print Job", {})
                print(f"Yazdırma başlatıldı: {printer_name}")

