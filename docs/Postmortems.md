**Author: Dagmara Przygocka**
# Logging postmortems

Team O - the Ops team / Team D - the Dev team

Team D - (Dagmara, Petra) 
Introduced a bug in the deployed system and notifies Team O. The bug will be a result of the enforced quality gates rules which complained about the lack of restiction on login/logout and other method in view.py file. The restriction was introduced by implementing decorator in the application that allows only POST requests to be sent to login/logout methods. As the result the user could not reached the login/logout site of the system. 

Team O - (Simon, Marcus) 
Is only allowed to look at the logs in order to isolate the component in which the bug is. The logging system is accesible on http://138.68.73.127:5000 with credentials given by the teacher. The team O searched through the logs knowing that the user is not able to get to login/logout page. 
The steps they took are as follows:
- go to kibana (http://138.68.73.127:5000) service to the discover tab
- they go to open option in the discover tab and choose the logs from the application (Team O knows that the bug is in the application since the user can not open       login page)
![](https://github.com/szymongalecki/ITU-MiniTwit/blob/main/dev_notes/app_logs.png)
- after they applied searching filter they add addtional filed called 'message' and they filter the logs which are comming from application
![](https://github.com/szymongalecki/ITU-MiniTwit/blob/main/dev_notes/error_log.png)
- team O limits the logs to a day and looks for the login/logout requests
- the logs shows the message: "Method Not Allowed" for the GET request to the login/logout method which allows to identified the error in the code. Morevoer, they discove that also unfllowing method do not allow the GET requests and report itr to the team O.



