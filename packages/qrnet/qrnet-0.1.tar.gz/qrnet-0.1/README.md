# qrnet

A simple command-line tool to generate QR codes for Wi-Fi credentials.

## Installation

Install `qrnet` using pip:

```
pip install qrnet
```

## Usage

To generate a QR code for your Wi-Fi:

```
qrnet <SSID> <Password> <Encryption Type> [-f filename.png]
```

### Arguments
- SSID: The SSID of your Wi-Fi network.
- Password: The password for your Wi-Fi network.
- Encryption Type: Choose from WEP, WPA, or WPA2.
- filename (optional): Specify the filename for the QR code image. If not provided, the default is `wifi_qr.png`.

## Contributing
Pull requests are welcome.
