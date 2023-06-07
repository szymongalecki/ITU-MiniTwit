### ITU2023-DevOps
Project repository for "DevOps, Software Evolution and Software Maintenance, MSc" course given at ITU at 2023 Spring semester.

### Team members
- Dagmara Przygocka - dagp@itu.dk
- Marcus Gunnebo - mcru@itu.dk
- Petroula Stamou - petst@itu.dk
- Szymon Gałecki - sgal@itu.dk

### Available services
[Application](http://138.68.73.127:8000/)  
[API](http://138.68.73.127:8080/docs)  
[Monitoring](http://138.68.73.127:5003/login)  
[Logging](http://138.68.73.127:5000/app/dashboards#/view/a7d68a00-e5e5-11ed-9430-f1eb680f055e?_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:now-15m,to:now)))


### Group T - "our group name"
Project consisted of:
- refactoring existing codebase for twitter clone and migrating to modern techhologies, we used Django
- migrating from SQLite file-based database to more efficient one, in our case - PostgreSQL
- containerizeing services using Docker
- exposing an API for mimicking user-like interactions, we used FastAPI
- deploying to cloud, we used DigitalOcean
- testing the application, we used pytest and Selenium
- monitoring the state of API, we used Prometheus and Grafana
- logging, we used Elasticsearch, Filebeat and Kibana
- CI/CD pipeline, we used GitHub Actions workflow
- creating VM to host all services, we used Vagrant
- reverse proxy, we used NGINX
- distribute

### Deployment view
![Tux, the Linux mascot](/report/images/Deployment.png)

### Code quality tools
[Sonarcloud](https://sonarcloud.io/project/overview?id=szymongalecki_ITU-MiniTwit)  
[Code Climate](https://codeclimate.com/github/szymongalecki/ITU-MiniTwit)
