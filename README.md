# habraparser

###Запуск проекта
`docker-compose up`
###Остановка проекта
`docker-compose down`
###Запуск парсинга всех лучших статей за день
`curl --location --request GET 'http://127.0.0.1:8000/api/force_parsing/'`
###Парсинг конкретной статьи
`curl --location --request POST 'http://127.0.0.1:8000/api/force_parsing/' --form 'url=https://habr.com/ru/post/499358/'`
###Листинг статей
`curl --location --request GET 'http://127.0.0.1:8000/api/articles/'`
###Отдельная статья
`curl --location --request GET 'http://127.0.0.1:8000/api/articles/1/'`

Автоматический парсинг [запланирован](habraparser/celeryapp.py) на каждый день в 15:00
