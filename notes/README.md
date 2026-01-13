# Important notes about the project

### docker
Isolate your project!!
docker pull python:3.11 - download image from docker hub
docker run -it python:3.11 - run it interactively

Sooner we get our app working with docker the better as it is closest to production and actually sharing it with the world! 
```
#!/bin/bash

RUN_PORT="${PORT:-8000}"

gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind "[::]:$RUN_PORT"

```
- 1. gunicorn master process starts -> gunicorn doesnt handle async by itself, so, uvicorn is needed
- 2. master starts 2 worker processes
- 3. each worker runs one instance of fast app in its own memory -> they dont share memory
- 4. master listens on port 8000 and routs requests to the workers
- 5. FastApi handles requests async via uvicorn inside each worker

So, gunicorn manages workers inside containers and loadbalancer handles containers!

#### docker commands
- `docker build -t analytics-api .`
- `docker run analytics-api`

- `docker compose up --watch`
- `docker compose up --build`
- `docker compose down -v` (remove volumes)
- `docker compose run app /bin/bash` or `docker compose run app python`

with build version docker rebuilds all the images (uses cashing so it doesnt build all the layers - only the ones that changed - each `RUN`, `ADD` and `COPY` are layers)
without build it will use already existing images!

!!! CMD in Dockerfile is the default command.
command: in docker-compose.yml overrides CMD when you run with Compose.
That’s why you see uvicorn running in dev even though Dockerfile says gunicorn.

dockerfile helps us with prod env while compose file helps us with dev env, but both give us prod ready env.