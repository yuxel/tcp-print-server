import socket
import threading
import win32print
from pystray import Icon, MenuItem as item, Menu
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

printed_texts = []  # Hafızada saklanan metinler

def create_image():
    # Tray iconu için basit siyah daire
    image = Image.new('RGB', (64, 64), color='white')
    dc = ImageDraw.Draw(image)
    dc.ellipse((16, 16, 48, 48), fill='black')
    return image

def start_socket_server():
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
                    try:
                        # Hafızaya yaz (görüntülemek için)
                        printed_texts.append(data.decode('utf-8', errors='ignore'))

                        printer_name = win32print.GetDefaultPrinter()
                        hPrinter = win32print.OpenPrinter(printer_name)
                        job = win32print.StartDocPrinter(hPrinter, 1, ("TCP Print Job", None, "RAW"))
                        win32print.StartPagePrinter(hPrinter)
                        win32print.WritePrinter(hPrinter, data)
                        win32print.EndPagePrinter(hPrinter)
                        win32print.EndDocPrinter(hPrinter)
                        win32print.ClosePrinter(hPrinter)
                    except Exception as e:
                        print(f"Yazdırma hatası: {e}")

def show_printed_texts():
    window = tk.Tk()
    window.title("Yazdırılanlar")
    window.geometry("600x400")

    text_area = ScrolledText(window, wrap=tk.WORD)
    text_area.pack(expand=True, fill='both')

    for t in printed_texts:
        text_area.insert(tk.END, t + '\n\n')

    window.mainloop()

def quit_app(icon, item):
    icon.stop()

def setup_tray():
    menu = Menu(
        item('Yazdırılanları Göster', lambda icon, item: show_printed_texts()),
        item('Çıkış', quit_app)
    )
    icon = Icon("YazıcıSunucusu", create_image(), "TCP Yazıcı Sunucusu", menu)
    icon.run()

if __name__ == '__main__':
    print(f"Main")
    # Socket sunucuyu ayrı bir thread’de başlat
    threading.Thread(target=start_socket_server, daemon=True).start()

    print(f"Tray Icon")
    # Tray iconu başlat
    setup_tray()

