import qrcode
import argparse

def generate_wifi_qr(ssid, password, encryption, filename):
    qr_info = f"WIFI:T:{encryption};S:{ssid};P:{password};;"
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(qr_info)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print(f"QR code saved as {filename}")

def main():
    parser = argparse.ArgumentParser(description="Generate a QR code for Wi-Fi credentials.")
    parser.add_argument("ssid", help="SSID of the Wi-Fi network")
    parser.add_argument("password", help="Password of the Wi-Fi network")
    parser.add_argument("encryption", choices=["WEP", "WPA", "WPA2"], help="Encryption type of the Wi-Fi network")
    parser.add_argument("-f", "--filename", default="wifi_qr.png", help="Filename to save the QR code image (default: wifi_qr.png)")

    args = parser.parse_args()
    generate_wifi_qr(args.ssid, args.password, args.encryption, args.filename)

if __name__ == "__main__":
    main()
