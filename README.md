<div align="center">
  <h1>Task Manager</h1>
  
  [![Actions Status](https://github.com/lovedr6s/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/lovedr6s/python-project-52/actions)
  [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=lovedr6s_python-project-52&metric=alert_status)](https://sonarcloud.io/dashboard?id=lovedr6s_python-project-52)

  ### [Url to the site](https://python-project-52-ptxg.onrender.com)
</div>


## About
Task Manager is a web application built with Python and Django framework. It allows you to make tasks, change their statues. The app can be used with more than just one person.

## Installation

### _Easy Mode:_

Why not just let [Docker Compose](https://docs.docker.com/compose/) do all the work, right? Of course, for the magic to happen, [Docker](https://docs.docker.com/desktop/) must be installed and running. 

Clone the project:
```bash
>> git clone https://github.com/ivnvxd/python-project-52.git && cd python-project-52
```

Create `.env` file in the root folder and add following variables:
```dotenv
DATABASE_URL=postgresql://postgres:password@db:5432/postgres
SECRET_KEY={your secret key} # Django will refuse to start if SECRET_KEY is not set
LANGUAGE=en-us # By default the app will use ru-ru locale
```

And run:
```shell
>> docker-compose up
```

Voila! The server is running at http://0.0.0.0:8000 and you can use it.