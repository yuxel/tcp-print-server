import socket
import win32print

HOST = '0.0.0.0'
PORT = 9100

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Dinleniyor: {HOST}:{PORT}")
    
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Bağlandı: {addr}")
            data = conn.recv(10240)
            if data:
                printer_name = win32print.GetDefaultPrinter()
                hPrinter = win32print.OpenPrinter(printer_name)
                job = win32print.StartDocPrinter(hPrinter, 1, ("TCP Print Job", None, "RAW"))
                win32print.StartPagePrinter(hPrinter)
                win32print.WritePrinter(hPrinter, data)
                win32print.EndPagePrinter(hPrinter)
                win32print.EndDocPrinter(hPrinter)
                win32print.ClosePrinter(hPrinter)

