# Flask-MongoDB Web App

For this exercise, I created a web app called **Bike Snitches**, which allows users to submit reports of cars parked illegally in bike lanes in NYC, as well as view documents containing reports made by other users. The link to the web app can be found [here](https://i6.cims.nyu.edu/~ol544/web-app-ohding11/flask.cgi/).
</br>
</br>
I have submitted an example report, which is visible in the '/reports' page. For demonstration purposes, anyone can edit or delete any reports from the database - however, if this app was deployed for practical use, I would add a feature that only allows authorized users to do so. The data is stored in a MongoDB collection titles ```bikeapp```. I checked that it was storing the data properly by running the query ```db.bikeapp.find()``` in the mongo shell, which gave me the following results:
```
[
  {
    _id: ObjectId("644c30082c6d48b9535d926d"),
    location: '14th and First Ave',
    borough: 'Manhattan',
    plate: '26562',
    model: 'Honda Odyssey',
    color: 'Silver',
    email: 'ol544@nyu.edu',
    notes: 'On northeast corner of intersection.',
    created_at: ISODate("2023-04-28T20:43:52.130Z")
  }
]
```
I worked indpendently on this project.