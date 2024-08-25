# Тестовое задание ДИТ
# Бронирование переговрных
## Используемые технологии

- Django 
- Drf 
- Swagger = для документирования Api и его ручек

## Подготовка к запуску

В корневой директории создайте файл `.env` и пропишите там настройки

## Запуск приложения
Перейдите в папку meeting_room
Установите виртуральное окружение `python3 venv venv`
Установите зависимости `python3 -m pip install -r requirements.txt`
Сделайте миграции в бд `python3 manage.py migrate`
Запустите приложение `python3 manage.py runserver`


## Доступные API методы

get /api/LogViewSet/get_report/ - создает на сервере отчет в формате word о всех переговорных комнатах

get/post/put/delete /api/LogViewSet - получения/создание/обновление/удаление лога

get/post/put/delete /api/MeetingRoom/ - получения/создание/обновление/удаление переговорной комнаты

get/post/put/delete  /api/ReservationMeetingRoom/ - получения/создание/обновление/удаление бронирования комнаты

get /api/ReservationMeetingRoom/get_booking/ - получения бронированных комнта по дате и времени
