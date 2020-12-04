==================================
Test Services APIs (Case : Pokemons)
==================================

--------
Overview
--------

**Test API services with Django REST Framework**

-----
Goals
-----

As a API services data with Django REST Framework we are trying to address following goals:

1. Get detailed information of species pokemons by their id 

2. Get information on the regions, localities and areas where Pokémon species are located 

3. Get detailed information on the Pokémon species that have been caught by the user and are in storage

4. Save information about new pokemons captured by the user

5. Change nickname of user-captured pokemons

6. Release user-captured pokemons

7. Get information from the pokemons members of the party by the user

8. Exchange the pokemon members of the user's party


------------
Requirements
------------

1. Python (3.7.5)
2. Django (3.0)
3. Django REST Framework (3.10, 3.11)
4. postgreSQL (10.21)

We **highly** recommend and only officially support the latest patch release of each Python, Django and REST Framework series.

------------
Installation
------------

::
	  # Use pip or pip3 (execute as superuser or administrator)
    
  $ pip install virtualenv

    # creating and activate virtual environments with python version 3.7.5
    
      # example:
    
        # sudo virtualenv -p "/usr/bin/python3.7" my_env
      
        # cd my_env
      
        # source activate
   
    # Recommended to run in virtual environments
    
  $ pip install Django==3.0 

  $ pip install djangorestframework
  
  $ pip install psycopg2 

    # for optional package integrations
		  
      $ pip install markdown
      
      $ pip install django-filter 


Running the app
^^^^^^^^^^^^^^^

It is recommended to create a virtualenv for testing. Assuming it is already
installed and activated:

::

    $ git clone https://github.com/lefhiro-s/test-api-django-pokemons.git
    $ cd Turpial-test-django-pokemons

    # 	configure database settings
      	edit turpial_project/settings.py
    	  section DATABASES -> default configure 
	        'NAME'          : 'name previously configured in postgreSQL'     ,
	        'USER'          : 'user previously configured in postgreSQL'     ,
	        'PASSWORD'      : 'password previously configured in postgreSQL' ,
	        'HOST'          : 'host previously configured in postgreSQL'     ,
	        'DATABASE_PORT' : 'port previously configured in postgreSQL'
          
        run located in the app folder
		      example: (~/my_env/test-api-django-pokemons)

    $ python3 makemigrations pokemon
    $ python3 migrate

    # 	run to insert all the records from the database

    $ psql -U <db_user> <db_name> -h <db_host> < data.sql

    # run to start the server
    $ python3 manage.py runserver

Browse to http://localhost:8000

