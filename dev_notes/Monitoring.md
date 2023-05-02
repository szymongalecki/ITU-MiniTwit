**Author: Marcus Gunnebo**

# Prometheus and Grafana 
We have made changes to our system by adding two new docker containers: Prometheus and Grafana. A new package `prometheus_fastapi_instrumentator` for the API is responsible for sharing metrics about the APIs endpoints, which Prometheus views on `/metrics`. Grafana then collects these metrics from Prometheus with a 15 second interval and displays them on four different dashboards. Grafana visualises the number of requests and responses for each endpoint, and also shows whether it is connected to Prometheus. To login to Grafana, please use the credentials supplied by Helge on the Teams course channel. The Prometheus image was pulled from the Prometheus Dockerhub and supplied with a configuration file, while the Grafana image was built locally and uploaded to Dockerhub. All the images currently used in the docker-compose are available on the `petrastm` Dockerhub.

## Prometheus
Prometheus is an open source monitoring system used for scraping metrics from a wide variety of sources, including APIs. It is designed to be reliable, efficient, and highly scalable, allowing users to easily monitor not only their own applications, but also those of third parties. It is used to collect time-series metrics, such as uptime, latency, and throughput, and provides a powerful query language for analyzing and visualizing the data. Prometheus can also be used to alert users when certain thresholds are exceeded or when certain conditions are met.

## Grafana
Grafana is an open source data visualization and monitoring platform used for creating dashboards and graphs. It is used for a variety of applications, such as monitoring and alerting and for displaying real-time data from sources such as Prometheus. Grafana allows users to explore their data, visualize their metrics, and gain insights into their data. It also provides a powerful query editor, allowing users to quickly query and explore their data. Grafana is used by many organizations to monitor and visualize their data.

### Dashboard
Grafana was manually configured by creating four dashboards to the specific needs of our project. The configuration was then exported as a JSON file, enabling automated set up each time the application is re-deployed. This also includes setting up a user with username and password given in the teams channel by Helge. This streamlines the process of monitoring endpoints in the API, decreasing the amount of manual tasks required.

### datasource.yml
Setting up Prometheus allows the Grafana instance to get requests from the Prometheus instance. This allows Grafana to access the Prometheus data source without exposing it directly to the internet.

```datasources:
-  access: 'proxy'
   editable: true
   is_default: true
   name: 'prometheus'
   org_id: 1
   type: 'prometheus'
   url: 'http://prometheus:9090'
   version: 1
   uid: 'prometheus'```