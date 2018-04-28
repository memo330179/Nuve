
Welcome to Nuve the media server for the people. 

# Motivation
This project was created and designed for one purpose and one purpose only; to be useful. This philosophy makes this server one of the best options if you want something light weight and easy to use. The dream is for us to be able to handle our media the way that we want to with no string attached and no limitations.

# Get Started
This server is essential the backend for the UI of the project. This part takes care of storing things and sending out information about shows when needed. In order to run this at the moment(it is not functional yet) use the following steps

1. Clone the repository locally
    * `git clone https://github.com/memo330179/Nuve.git `
2. install dependencies using pip
    * `pip install -r requirements.txt `
3. run the server:
    * `python run.py`

inside of the repository you will find the following structure 

```
.
├── README.md
├── __pycache__
├── app
│   ├── __init__.py
│   ├── __pycache__
│   ├── api # all of the api logic
│   │   ├── __init__.py
│   │   ├── db_functs.py # functions used to interact with the database
│   │   ├── models.py # models for media 
│   │   ├── tmdb_funcs.py # functions that interact with the movie database
│   │   ├── upload.py # function that uploads the files to the server
│   │   └── views.py # function that return something to the server
│   ├── db_base.py # ties the various models files together
│   ├── mod_auth # handles authorization
│   │   ├── __init__.py
│   │   ├── models.py # holds user models
│   │   └── views.py # send out the token
│   └── secrets.py # holds our secrets (not in the repository)
├── config.py 
├── db.sqlite (should not be committed)
├── requirements.txt
└── run.py
```
