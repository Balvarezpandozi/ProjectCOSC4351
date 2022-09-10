COSC 4351 - Fundamentals of Software Engineering. 
Dr. Raj Singh
Authors:
Bryan Alvarez
Caleb Rogers

	SEMESTER PROJECT

Description: 
A restaurant chain has reached out to your team to build a reservation system. 

Here are the details:
-	Two categories of users / customers: guest user or registered user.
-	Users should be able to search for a table and reserve. 
o	User doesn’t need to login to the system to reserve a table. If registered users, they can login.
o	User enters name, phone, email, date and time (date picker), and # of guests for dining and system presents available tables.
o	Tables have maximum capacity limit i.e., 2, 4, 6, or 8.
o	Different combinations are allowed, and owner accommodates the seating, for example: someone requests 8 guests and table for 8 is not available but 2 + 6, or 4+4 is available. System should combine the tables and notify owner they need to combine tables. In this case System reserves both tables.
-	If a guest user i.e., not a registered user, system should prompt user to register (Optional) before finalizing the reservation.
-	Registered users will have these fields:
o	Name, mailing address, billing address (checkbox if same as mailing address), Preferred Diner # (system generated), Earned points (based on $ spent i.e., $1 is 1 point), preferred payment method (cash, credit, check).
-	System should track high traffic days / weekends and a hold fee is required i.e. July 4th will require valid credit card on system to reserve the table.
o	Notify user no show will have minimum $10 charge.

Assumptions:
If you make any assumptions to provide good user experience, please list it.

Running Instructions:
1. Install flask using the following command: 
												pip install flask
2. Install module flask-login using the following command:
												pip install flask-login
3. Install module flask-sqlalchemy using following command:
												pip install flask-sqlalchemy
4. To run the web server locally, you have to run the main.py file on the website folder

File Structure:
	main.py > this file is the index file for the application and the one used to run the server

	assigments > contains all the written assigments of the class since they are all related to this project.

	website > contains all the code pertaining to the web server
			files:
				__init__.py -> makes the parent folder a python package
				auth.py -> contains all the routes for the application's authentication
				models.py -> contains all the schemas for the data to be saved on the database
				views.py -> contains all other routes for the application (likely to change)
			> static > contains all the static assets, such as images, stylesheets (css), and scripts (javascript) for the views
			> templates > contains all the html files for every view

Technical Details:
- Flask is the framework used to build the web server in python
- flask-login is a flask python module to handle user authentication
- flask-sqlalchemy is a flask python module to wrap sql to make easier the creation and management of the database
