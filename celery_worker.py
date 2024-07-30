from celery import Celery
import pytesseract
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()


celery = Celery('tasks', broker=os.getenv('CELERY_BROKER_URL'))
celery.conf.broker_connection_retry_on_startup = True
celery.conf.result_backend = 'rpc://'
celery.conf.task_serializer = 'json'
celery.conf.result_serializer = 'json'
celery.conf.accept_content = ['json']


@celery.task
def get_text(path) -> str:
    """
    Извлекает текст из изображения.

    Args:
        path (str): Путь к изображению.

    Returns:
        str: Извлеченный текст.
    """
    cut_app = len('/app/')
    short_path = path[cut_app:]
    image = Image.open(short_path)
    text = pytesseract.image_to_string(image, config='--oem 3 --psm 6')
    return text
