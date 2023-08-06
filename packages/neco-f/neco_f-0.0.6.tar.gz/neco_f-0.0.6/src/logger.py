import logging
from neco_f.os_time import get_date
from neco_f import always_used as au


def setup(file_name=get_date(),
          file_mode='a'):
    au.mkdir('Logs')
    work_dir = f'Logs/{file_name}.log'
    logging.basicConfig(filename=work_dir,
                        format='%(asctime)s %(message)s',
                        level=logging.INFO,
                        filemode=file_mode,
                        encoding='utf-8')


def info(msg):
    logging.info(msg)
# setup()