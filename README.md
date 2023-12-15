# TODO
 CUSTOME USER
 with docker container name Backend on ::9000
 and smtp4test platform for testing propose on ::5000

     # TODO-API-todo app
     created api v1 for todo apps create update delete tasks 
     swagger deployed on 127.0.0.1:9000/swagger
    
     # TODO-API-accounts app
     created v1 api for accounting activity like register verify token-auth topology confirm and reconfirm api
     created v2 api used djoser as main leader without customize 
     swagger deployed on 127.0.0.1:9000

     # TODO-TEST-APIs

          # API-TEST For API-restframwork V1 for todo app
              7 tests will be applied

          # API-TEST For API-restframwork V1 for accounts app
              14 test will be applied 

    # redis as service in docker-compose as redis
    # worker as service in docker-compose as worker
    # deploy celery in django backend todo for background proccessing to synchronise with redis
    # deploy celery django fo admin dashboard to mange schadualing tasks

    # API Request from outside and send to Cache Server Redis for Save in specific time to load from redis Db
    # for more speed loading

    # Live Weather API in TODO/API/V1
     {{localhost}}/api/v1/live/weather/?city={{CityName}}
     {{CityName}} : Name of city you want current weather specification like Tehran,London,Paris ...... Default is Tehran
     Example : http://127.0.0.1:9000/api/v1/live/weather/?city=london  


    # Live Crypto Price API in TODO/API/V1
    {{localhost}}/api/v1/live/crypto/?symbol={{CryptoAbbreviation}}
    {{CryptoAbbreviation}}: can vary like BTC,ETH,XRP.... Default is BTC
    Example : http://127.0.0.1:9000/api/v1/live/crypto/?symbol=XRP 

if u want ran the project in STAGE mode user docker-compose-stage.yml
     Specification of Stage mode:
         - change debug mode to False
         - Change database from sqlite to postgress with specific container
         - use gunicorn as requset server from nodejs to django
         - use nodejs as WebServer distributer with django and gunicorn  
         - config nodejs to handle requests to gunicorn for request and static and media files for django      