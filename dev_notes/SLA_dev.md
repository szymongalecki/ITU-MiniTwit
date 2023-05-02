#SLA dev explanation
## Service Availability
We will measure/monitor service availability by looking at the dashboards wich displays count of request/respopnse we get in the application. If there are not response/requests than we will knwo the application is down.
## Response Time
We will measure average response time using grafana by running this query:
```
sum(rate(http_request_duration_seconds_sum{job="myapp"}[30d])) / sum(rate(http_request_duration_seconds_count{job="myapp"}[30d]))
```
The average from one month is around 55ms but to be make sure we uphold to the promise we will aim at 100ms response time.

## Security
We keep our security updates by using quality gates that scan our code and identify the threads. Addtioanly, we are usign hashing, salting of the passwords and haave firewall provided by the digital ocean 