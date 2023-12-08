# Flask-MongoDB Sin Tracking App

All the code used to build our web app are within this project repository. Please see below for a guide on the file directories and their function in the project.
<br>
<br>
- The ```templates``` folder contains the HTML templates for each page on our web app. The style, formatting, and interactive elements of the project are all controlled by the code within these files.
- The ```app.py``` file contains the code that connects our app to a web-hosted MongoDB Atlas databse, as well as functions that update the database based on user interactions. The code used to establish the web connections were taken from the source code (see blow), but the functions nested within them were written by us.
- The ```credentials.py```, ```flask.cgi```, and ```requirements.txt``` files configure the credentials and prerequisite packages needed to establish and authenticate the database connection. This was taken verbatim from the source code and we have not made any modifications to it.
- The ```LICENSE``` file contains a license agreement establishing guidelines from the publisher of the source code on how we are allowed to utilize it.
<br>
<br>
The source code for our web app was provided to us by materials distributed in Professor Amos Bloomberg's Database Design and Implementation course at NYU. We only used it for the purposes of establishing the connection to the web-hosted database, and any code that executes the visual design, user interactivity, and calculations represents our own intellectual work.