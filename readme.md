## Тестовый проект музыкальной библиотеки

### Используемый стек:

- `django + drf`
- `postgresql`
- `celery`
- `redis`
- `docker`
- `swagger`

### Для развёртывания приложения необходимо:

- установить docker: https://www.docker.com/
- клонировать репозиторий: git clone https://github.com/DeadEye2501/django_report.git
- в корневой папке выполнить команду `docker-compose up -d --build`
- сервер должен быть доступен на https://localhost:8000
- для администрирования нужно создать суперпользователя `python manage.py createsuperuser`

### Доступные API:

- swagger доступен по адресу http://localhost:8000/api/schema/swagger-ui/ там вы найдёте все используемые в проекте эндпоинты
- админка доступна по адресу http://localhost:8000/admin/ для логина под суперюзером можно использовать `root` - `Somepass_123`
- получить список всех расчётов можно по адресу `GET` http://localhost:8000/oil_report/api/report/
- получить информацию по конкретному расчёту можно по адресу `GET` http://localhost:8000/oil_report/api/report/{report_id}/
также можно расширить получаемые данные при помощи аргумента `fields`, передаваемого в header'е запроса, таким образом
можно получить `name` и `calc_time`. пример использования `fields`: http://localhost:8000/oil_report/api/report/{report_id}?fields={name,calc_time}
- запросить новый расчёт можно по адресу `POST` http://localhost:8000/oil_report/api/report/ передав в теле запроса следующие параметры:
`date_start`, `date_fin`, `lag`

### Вопросы и ответы:

- было не очень понятно, каким образом лучше сохранять данные, получаемые из `kernel.py` в базу данных, решил, что наиболее
логично сделать несколько записей, ссылающихся на один расчёт.
- не очень понятно, должна ли очередь из расчетов идти строго последовательно, или можно ее распараллелить.