import sys
import qrcode
from dotenv import load_dotenv
import logging.config
from pathlib import Path
import os
import argparse
from datetime import datetime
import validators

load_dotenv()
SECRET_DIRECTORY=os.getenv('QR_SECRET_DIR','secret_qr_code')
SECRET_FILL_COLOR=os.getenv('SECRET_FILL_COLOR','black')
SECRET_BACK_COLOR=os.getenv('SECRET_BACK_COLOR','white')

def setup_logging():
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s',handlers=[logging.StreamHandler(sys.stdout)])

def create_secret_directory(path: Path):
    try:
        path.mkdir(parents=True,exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create dir {path}: {e}");sys.exit(1)

def is_valid_url(url):
    if validators.url(url):return True
    logging.error(f"Invalid URL: {url}");return False

def generate_secret_qr_code(data, path, fill_color='black', back_color='white'):
    if not is_valid_url(data):return
    try:
        qr=qrcode.QRCode(version=1,box_size=10,border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img=qr.make_image(fill_color=fill_color,back_color=back_color)
        with path.open('wb') as qr_file:
            img.save(qr_file)
        logging.info(f"Secret QR saved to {path}")
    except Exception as e:
        logging.error(f"Error while generating/saving secret QR: {e}")

def main():
    parser=argparse.ArgumentParser(description='Generate a secret QR code.')
    parser.add_argument('--url',help='URL to encode in the secret QR code',default='https://github.com/shyyyyny')
    args=parser.parse_args()
    setup_logging()
    timestamp=datetime.now().strftime('%Y%m%d%H%M%S')
    qr_filename=f"SecretQR_{timestamp}.png"
    qr_code_full_path=Path.cwd()/SECRET_DIRECTORY/qr_filename
    create_secret_directory(Path.cwd()/SECRET_DIRECTORY)
    generate_secret_qr_code(args.url,qr_code_full_path,SECRET_FILL_COLOR,SECRET_BACK_COLOR)

if __name__=="__main__":
    main()
