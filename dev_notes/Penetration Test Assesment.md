## Risk Identification
1. Identify assets (e.g. web application)
    1. Web application
    2. Api
    3. Docker Hub
    4. Github repository 
    5. Digital Ocean
    6. Grafana / Prometheus / Kibana
2. Identify threat sources 
    1. SQL injection 
    2. Cross-Site Scripting (XSS) attacks
    3. Denial of Service (DoS) attacks
    4. Password leakage
    5. Exposure of hard-coded passwords in public repositories (e.g., GitHub) 
    6. Unused open ports 
    7. Administrator’s passwords and their strength on all relevant platforms
    8. Vulnerabilities in frameworks or docker images used
3. Construct risk scenarios 
    1. Attacker performs SQL injection attack on the application to download, alter, or delete sensitive data.
    2. Attacker uploads a malicious script as a comment, which can affect the system when loaded by the application, potentially causing harm or enabling further attacks.
    3. Denial of Service (DoS) attack renders the system unavailable to users.
    Unauthorized access to pages or areas that have not been properly authorized.
    4. Developer mistakenly uploads hard-coded passwords for administrator accounts. 
## B. Risk Analysis
1. Determine likelihood
    1. The likelihood of encountering a SQL injection vulnerability in our application is minimal to none. We have thoroughly reviewed the app and identified only three forms that an attacker could potentially exploit: the login and registration forms, as well as the post message form. In order to ensure the safety of our application, we have implemented the following security measures:
        1. We have leveraged the robust user registration and authentication features provided by Django, utilizing their built-in functionality.
        2. Django's ORM (Object-Relational Mapping) system automatically parameterized queries, offering an additional layer of protection against SQL injection attacks.
    2. The likelihood of XSS attacks within our application remains minimal due to the following security measures we have implemented:
        1. We have enabled Django's built-in Cross-Site Request Forgery (CSRF) protection, which adds an extra layer of defense against malicious attacks.
        2. Django's template engine applies HTML escaping by default, ensuring that user-generated content rendered within HTML contexts is properly sanitized to prevent XSS vulnerabilities.
        3. The usage of the {{ message.text }} variable in our templates signifies that Django's auto-escape feature is active, automatically encoding special characters to prevent them from being interpreted as HTML entities. This further reduces the risk of XSS exploits.
    3. Our application is hosted on DigitalOcean, which offers robust DDoS protection mechanisms and network security features, including:
        1. Traffic filtering and mitigation: DigitalOcean employs advanced network-level traffic filtering and mitigation techniques to identify and neutralize potential DDoS attacks, safeguarding the availability and performance of our application.
        2. Anycast technology: DigitalOcean's global network leverages Anycast technology, distributing incoming traffic across multiple strategically located data centers. This ensures efficient load balancing and reduces the impact of targeted attacks, enhancing the overall resilience of our infrastructure.
        3. Cloud firewall service: DigitalOcean provides a comprehensive cloud firewall service that empowers us to define custom rules for filtering and controlling incoming and outgoing traffic. This allows us to proactively manage network access and fortify our application against unauthorized or malicious activities.
    4. The scenario of password leakage is highly unlikely due to our robust security measure in place. Secure password storage: All passwords are meticulously stored in the database using a strong hashing algorithm combined with the utilization of salt. This means that passwords are transformed into irreversible hashes, ensuring that no raw passwords are accessible to any potential adversary. By employing these rigorous security practices, we effectively mitigate the risk of password leakage and enhance the overall protection of user credentials. Rest assured that our commitment to safeguarding sensitive information remains steadfast.
    5. Hard-coded passwords exposed in public repositories pose a potential risk due to human error. Although we strive to maintain strict security practices, the possibility of such occurrences cannot be completely ruled out. We continually educate and emphasize the importance of safeguarding sensitive information to minimize the likelihood of this type of mistake.
    6. The presence of unused open ports is an improbable scenario as our application meticulously manages its port configurations. We maintain a strict policy of only opening and monitoring specific ports that are essential for the application's functionality. This proactive approach significantly reduces the risk of unauthorized access through unused ports.
    7. The potential compromise of administrator passwords is a valid concern, considering the shared nature of these credentials. As part of our operational procedures, administrator passwords were shared within either the lecture GitHub repository or our own GitHub repository. While efforts are made to ensure the security of these repositories, it is crucial to acknowledge the possibility of a compromise. To mitigate this risk, we regularly update and strengthen our password management protocols, enforcing strong passwords and encouraging regular password changes.
    8. The likelihood of vulnerabilities in frameworks or Docker images utilized in our system is a valid concern. With a diverse range of dependencies, the potential for vulnerabilities does exist. To address this, we adopt a proactive approach by actively monitoring and updating these components to ensure they remain secure and up to date. We regularly patch vulnerabilities, apply security updates, and conduct comprehensive vulnerability assessments to mitigate the risk associated with third-party dependencies.
2. Determine impact
    1. SQL injection: Moderate
    In the event of a potential successful SQL injection attack, the impact would be of moderate significance. We employ industry-standard practices to ensure the secure storage of passwords by applying hashing algorithms along with the utilization of salt. This approach transforms passwords into irreversible hashes, making it extremely difficult for any potential adversary to retrieve the original passwords
    2. Cross-Site Scripting (XSS) attacks: Severe
    In the event of a Cross-Site Scripting (XSS) attack, the impact can be severe, potentially resulting in unauthorized access and various detrimental consequences. The attackers have the potential to hijack users' sessions, allowing them to carry out unauthorized actions on behalf of the user, this can lead to identity theft.
    3. Denial of Service (DoS) attacks: Significant
    The impact of a Denial of Service (DoS) attack can be significant, as it can render a system or network unavailable to legitimate users
    4. Password leakage: Severe
    The impact of password leakage can be severe, posing a significant risk to user accounts and sensitive information. When passwords are leaked or exposed, unauthorized individuals may gain access to user accounts, potentially leading to identity theft, unauthorized access to personal data, and compromised systems.
    5. Exposure of hard-coded passwords: Severe/Negligible
    The exposure of hard-coded passwords can have serious consequences, as it provides a direct pathway for unauthorized access to systems or sensitive data. The impact can include unauthorized access, data breaches, and potential compromise of critical systems or accounts.
    6. Unused open ports: Significant 
    Open ports that are not actively monitored or utilized increase the attack surface of a system, allowing attackers to target and exploit any vulnerabilities associated with those ports. The impact is considered significant because in case of a successful attack the system risks a potential compromise of the connected systems and data breaches.
    7. Administrator’s passwords and their strength on all relevant platforms: Severe/Negligible
    The risk associated with compromised administrator passwords is severe. It exposes sensitive information and grants unauthorized access to the system, posing a significant threat to its integrity and confidentiality.  
    8. Vulnerabilities in frameworks or docker images used: Moderate
    The extent of the impact hinges primarily on the image or framework involved, as well as the specific type of vulnerability at hand.
3. Discuss what are you going to do about each of the scenarios
    1. SQL injection:
    Users should be notified immediately via emails in the event of personal information leakage. It's important to inform the users that their passwords are securely stored, utilizing hashing techniques instead of plain text. 
    2. Cross-Site Scripting (XSS) attacks:
    To effectively address the attack, the website should go temporarily offline or restrict access to it until the issue is resolved. Furthermore, it is crucial to promptly notify all affected users and provide them with guidance on changing their passwords, while encouraging them to remain vigilant against any malicious activities.
    3. Denial of Service (DoS) attacks:
    We are using monitoring tools like Prometheus to detect unusual patterns or sudden spikes in network traffic in order to identify and respond to a potential DoS attack in real time.
    4. Password leakage:
    The stored password are in hashed form but nevertheless the affected users will be notified and will be prompt to change their passwords 
    5. Exposure of hard-coded passwords:
    Upon finding any such password the developers should immediately change the compromised password and assess the system for possible security issues.
    6. Unused open ports: 
    Any open port to the system should be closed immediately after discovery, and assess any possible security bridges.
    7. Administrator’s passwords 
    All administrator pages should use two factor authentication in combination with strong passwords.


4. Use a Risk Matrix to prioritize risk of scenarios
![](https://github.com/szymongalecki/ITU-MiniTwit/blob/main/dev_notes/RistMatrix.png)


## C. Pen-Test Your System
During our Pen-Test, we initiated the assessment by employing the nmap command with the flags -v -A -sV -Pn. This allowed us to identify any open ports that might pose a threat to our system. As anticipated, the scan revealed only the intended open ports, all of which were diligently monitored by Prometheus to ensure system security.

Next, we proceeded to execute the OWASP ZAP 2.12.0 tool on our website, which provided us with a comprehensive list of vulnerabilities requiring attention. This allowed us to prioritize our tasks and address each vulnerability accordingly. Please refer to the picture bellow for the complete list, with alert levels ranging from medium priority to information.

For the final phase, we conducted targeted attacks on our application using custom scripts and various scenarios, such as SQL injections and XSS attacks. Through this process, we identified a key vulnerability that demanded immediate attention: cross-site scripting attacks. To fortify our application, we implemented CSRF tokens in all forms susceptible to this vulnerability, thus enhancing the overall security of our app.

![](https://github.com/szymongalecki/ITU-MiniTwit/blob/main/dev_notes/Alerts.png)



