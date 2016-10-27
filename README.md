# test-hopster
This is a simple app built with Google App Engine and Python using webapp2 framework. It uses an API created with Google Endpoints. Users just can login, write something on The Wall, filter Writings by Author name and delete it. Google Datastore used to keep data.

You can take a look at deployed application by following the link below<br>
https://hopster-test-wall.appspot.com


It's easy to run app locally. Just do the following:
* install Google Cloud API and configure it
* execute `pip install -r requirements.txt -t lib\` in your application folder to install required libs
* execute `dev_appserver.py .` also in application folder to launch it
