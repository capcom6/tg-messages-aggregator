# Аггрегатор сообщений Telegram с нескольких аккаунтов (не завершен)

Разрабатывался для разнообразия и желания написать что-нибудь на Python.

## Исходное ТЗ

Нужно написать сервис, проверяющий входящие сообщения в Telegram-аккаунтах. 

Веб-админка сервиса (он должен работать на VPS и иметь полноценный фронтенд) должна состоять из: 

* странички со списком-таблицей подключенных контактов и их статусом, показывающим, “жива” ли сессия аккаунта. 
* странички для добавления нового аккаунта 
* странички с настройками 

При получении входящего сообщения на один из подключенных аккаунтов, сервис должен присылать уведомление через Телеграм-бот в отдельно указанный аккаунт. 

Также, уведомление должно приходить, если сессия одного из аккаунтов перестала работать по какой-то причине.

Источник: https://www.fl.ru/projects/5133010/python_js-servis-dlya-proverki-vhodyaschih-soobscheniy-v-telegram-akkauntah.html

## Не реализовано

* [ ] веб-UI;
* [ ] проблема с уведомлением о новой сессии - уведомление поступает в бот раньше, чем сессия оказывается записаной в БД;
* [x] пересылка сообщений через бота;
* [ ] обработка ошибок.
