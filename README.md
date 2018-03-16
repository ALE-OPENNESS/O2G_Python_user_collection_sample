# O2G Python user collection sample #


----------


Alcatel-Lucent Enterprise - OmniPCX Open Gateway (02G) - Python example collecting user information


The application takes 6 arguments:

- 	the O2G FQDN or IP address
- 	the O2G port to connect to
- 	the user login (either admin or "basic" user)
- 	the user password
- 	if the access mode to the O2G is public (internet) or not (local network)
- 	if the debug mode is activated
	
For **example**: myo2g-server.com 443 adminuser1 adminuserpassword1 False True
	

If the user is an **admin** user, the application will collect all the information of the users belonging to the same cost center as the admin user.
If the user is a "basic" user, only his information are collected.


The **debug mode** prints all the REST exchanges to the default output console.


The application builds a **csv file** (users.csv) containing the collected information.