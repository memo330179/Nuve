
Welcome to [name to be decided] the media server for the people. 

# Motivation
This project was created and designed for one purpose and one purpose only; to be useful. This philosophy makes this server one of the best options if you want something light weight and easy to use. The dream is for us to be able to handle our media the way that we want to with no string attached and no limitations.

# Get Started
This server is essential the backend for the UI of the project. This part takes care of storing things and sending out information about shows when needed. In order to run this at the moment(it is not functional yet) use the following steps

1. Clone the repository locally
   * ```git clone https://github.com/memo330179/pi-drive-flask.git ``
2. install dependencies using pip
   * ```pip install -r requirements.txt``
3. run the server:
   * ```python run.py``

inside of the repository you will find the following structure 

```
.
├── app 
│   ├── api # all of the api logic
│   │   ├── db_functs.py # functions used to interact with the database
│   │   ├── __init__.py
│   │   ├── models.py # the movie/episode models
│   │   ├── __pycache__
│   │   ├── tmdb_funcs.py # functions to interact with the movie database
│   │   ├── upload.py # functions that upload the media types
│   │   └── views.py # functions that return something to the client
│   ├── front_end # maybe where the front end will live
│   ├── __init__.py
│   ├── mod_auth # handling authorization
│   │   ├── __init__.py
│   │   ├── models.py # User models
│   │   ├── __pycache__
│   │   └── views.py # authentication views
│   └── __pycache__
├── config.py 
├── db.sqlite # the database (should not be committed)
├── __pycache__ 
├── README.md # This README
├── requirements.txt # the dependencies of the project
└── run.py

8 directories, 15 files
```
