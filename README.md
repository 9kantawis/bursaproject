# bursaproject


Нужны Python и MySQL или MariaDB. Распаковываю архив, создаю окружение командой python -m venv .venv и ставлю зависимости командой .\.venv\Scripts\python.exe -m pip install -r requirements.txt. Файл chotochoto.sql импортирую в MySQL, например через phpMyAdmin. В нем уже есть таблицы и товары. Потом запускаю .\.venv\Scripts\python.exe manage.py runserver. Сайт открывается по адресу http://127.0.0.1:8000/, админка по адресу http://127.0.0.1:8000/admin/. Если у MySQL стоит пароль, перед запуском задаю DB_PASSWORD в окружении.
