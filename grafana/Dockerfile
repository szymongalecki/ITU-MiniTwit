FROM grafana/grafana:latest
COPY datasource.yml /etc/grafana/provisioning/datasources/datasource.yml
COPY dashboard.json /etc/grafana/provisioning/dashboards/dashboard.json
ENV GF_DASHBOARDS_DEFAULT_HOME_DASHBOARD_PATH="/etc/grafana/provisioning/dashboards/dashboard.json"
ENV GF_AUTH_ANONYMOUS_ENABLED=true
EXPOSE 3000
USER 1000