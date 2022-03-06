## SensorHub

SensorHub is a server to **collect and visualize** **sensor data**. That data could be a temperature measure from a sensor on an **Arduino** (or even better, a **NodeMCU** board) for example.

If you want to store that temperature and visualize it somewhere, SensorHub might be the right choice for you.

![](https://gitlab.com/salvatorelab/sensorhub/-/raw/master/screenshots/sensors.gif)


### How it works

SensorHub is made with **Django** (Python). You can install it on a remote server or locally on a computer at home, even on a **Raspberry Pi**. Yes, ARM is supported. As long as it can run Python it should work.

Once you have the server running, enter the admin panel and create a sensor. Give it a name, we will use that as an identifier for this sensor.

You can have a look at the **sensors/examples** folder on this repo to see what the code on a sensor looks like (currently we have an example for NodeMCU and a Raspberry Pi connected to a DHT22 temperture and humidity sensor).  
Basically what the sensor does (or the board to be more precise) is sending an HTTP request to the server every minute with a JSON payload containing the data. 

The server stores that data in a CSV file in the **data** folder of the repo.  
Why CSV? It is supported everywhere in case you want to do something else with it later. SensorHub focuses on simplicity and there is nothing more simple than a bunch of CSV files (one for each sensor and day).

There is a small SQLite database where the admin user and the sensor configuration is stored too.

### Installation

You will need Python3 and [pipenv](https://pypi.org/project/pipenv/) installed.  

- Clone this repo.  
- Enter the sensorhub root folder and run `pipenv install`.  
- Then, run `pipenv shell`.  
- Create the database with `python manage.py migrate`.  
- And now let's configure an admin user for you: `python manage.py createsuperuser`


That's it, the server is ready to start.

### Running the server

#### Manually

After running `pipenv shell` on the sensorhub root folder you can start the server with `python manage.py runserver` and open http://localhost:8000/ in your browser.

#### The easy but insecure way

Another option (not recommended for production) if you want to leave the server running, is using the [sensorhub.service file](https://gitlab.com/salvatorelab/sensorhub/-/blob/master/sensorhub.service) as a template to run it with `sudo systemctl start sensorhub` on a device that has systemd.  
You will have to adjust the _user_, _working directory_ and maybe the port too depending on your use case.  

This is not secure because it uses `python runserver` and that is a development server. If this is going to be on your home network it's fine, don't worry, otherwise see below.  

#### The secure way

But the best option, if your server is going to be public is to use NGINX and Gunicorn. 

- Installing Nginx: https://www.nginx.com/resources/wiki/start/topics/tutorials/install/
- Installing Gunicorn: https://docs.gunicorn.org/en/stable/install.html
- Nginx configuration: https://docs.gunicorn.org/en/stable/deploy.html
