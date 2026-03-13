import qrcode
from datetime import datetime
import csv
import os


def generate_qr_code(data, filename=None):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    if filename:
        img.save(filename)
    return img


def export_to_csv(data, headers, filename):
    if not os.path.exists('reports'):
        os.makedirs('reports')

    filepath = f'reports/{filename}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

    with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(headers)
        writer.writerows(data)

    return filepath


def get_status_color(status):
    colors = {
        'Новая заявка': 'blue',
        'В процессе ремонта': 'orange',
        'Ожидание запчастей': 'purple',
        'Готова к выдаче': 'green',
        'Завершена': 'gray'
    }
    return colors.get(status, 'black')