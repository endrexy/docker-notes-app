## This is intended as a DEVOps sample project(minimal functionaliy) 
## Focus is on using Docker and implementing best practices in Docker.

### Multi-Service Architecture:
- PostgreSQL (Database Layer)
- Flask API - (Application Layer)
- Nginx (Web Layer)

## Project Structure
```text
.
├── backend
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
├── init-db.sql
├── README.md
└── secrets
    ├── db_password.txt
    └── db_user.txt
```

### Details of implementation
#### 1. **PostgreSQL**
- [x] Create init-db.sql initialization script
- [x] Create docker-compose.yml for downloading the images and running the containers
- [x] Check db with adminer on localhost:8080 if db was initialized and new data can be inserted
- [x] Check PostgreSQL directly in the CLI using `psql -h localhost -p 5432 -U myuser -d mydb`
- [x] i01 - Improve environment variables and store passwords as secrets not in plain text
- [x] i02 - Improve dependencies by adding health checks
#### 1.1. Checking the functionality of PostgreSQL
- [x] Verify containers are running 
    `docker compose ps`
    **You should see:**
    ```text
    NAME            STATUS    PORTS
    todo-db         Up        0.0.0.0:5432->5432/tcp
    todo-adminer    Up        0.0.0.0:8080->8080/tcp
    ```
- [x] Go to  `http://localhost:8080`, and log in to adminer.
- [x] In adminer, go to 'Select data', the two entries generated from init-db.sql should be there.
- [x] Add data manually. Go to SQL command and enter `INSERT INTO todos (title, completed) VALUES ('Build Flask API', false);`
- [x] Check data persistence of volumes by stopping and restarting containers, then checking data in adminer.
    ```bash
    docker compose down
    docker compose up -d
    ```
- [x] Check PostgreSQL from within a container `docker exec -it todo-db psql -U myuser -d mydb`
- [x] Check PostgreSQL locally from the CLI `psql -h localhost -p 5432 -U myuser -d mydb` then enter password
- [x] Verify health status with `docker compose ps`. The status should show 'Up (healthy)'.
- [x] Verify secrets inside container:
    - Exec into PostgreSQL container `docker exec -it todo-db sh`
    - Check secret files exist:
    ```bash
    ls -la /run/secrets/
    cat /run/secrets/db_user
    cat /run/secrets/db_password
    ```
- [x] Check environment variables DON'T contain passwords `env | grep POSTGRES`
    **You should see no actual password in environment**
    ```text
    POSTGRES_USER_FILE=/run/secrets/db_user
    POSTGRES_PASSWORD_FILE=/run/secrets/db_password
    POSTGRES_DB=mydb
    ```
- [x] Test dependency orchestration
    - Simulate database failure `docker compose stop db`
    - Check adminer status `docker compose ps`
    - Adminer shows 'running' but will faile health checks because it can't reach the database.
    - Restart database `docker compose start db`
    - Health checks recover `docker compose logs -f db`
    - After 10 seconds, both services return healthy state

#### 2. **Flask API(Backend - Application Layer)**
- [x] Create project structure
- [x] Create ./backend/requirements.txt file  
- [x] Create the ./backend/app.py 
- [x] Create the Dockerfile 
- [x] Add the backend service to the  docker-compose.yml in parent folder
- [x] Build and start
#### 2.1. Check functionality of backend
- [x] Check logs after building the backend 
    ```
    docker compose up -d db backend
    docker compose logs -f
    ``` 
    Sould see:
    - PostgreSQL initializing and becoming healthy
    - Backend waiting for database
    - Backend starting Flask app on port 5000
- [x] Verify services are running `docker compose ps` 
    - Status should be up and healthy
    - Backend should have no exposed ports
- [x] Backend Health Check (Inside Container)
    - Exec into backend container `docker exec -it todo-backend sh`
    - Test the health endpoint `curl http://localhost:5000/health`
    - Output should be `{"status":"healthy"}`
- [x] Test the CRUD Operations(inside the container)
    - GET - read all todos `curl http://localhost:5000/api/todos`
    Output:
     ```
    [
        {"id": 1, "title": "Learn Docker", "completed": false},
        {"id": 2, "title": "Setup PostgreSQL", "completed": true}
    ]
    ```
    - POST - Create new todo
    ```
    curl -X POST http://localhost:5000/api/todos \
        -H "Content-Type: application/json" \
        -d '{"title": "Test Backend API"}'
    ```
    Output: `{"id": 3, "title": "Test Backend API", "completed": false}`
    - PUT - update todo
    ```
    curl -X PUT http://localhost:5000/api/todos/3 \
        -H "Content-Type: application/json" \
        -d '{"completed": true}'
    ```
    Output: `{"id": 3, "completed": true}`
    Verify with: `curl http://localhost:5000/api/todos`    
    - DELETE - Remove todo
    `curl -X DELETE http://localhost:5000/api/todos/3`
    No output means success(HTTP 204 status code)
    Verify deletion: `curl http://localhost:5000/api/todos` - should only show 2 entries again
    Exit container `exit`
- [x] Test from another container
    - Start temporary container on the same network
        `docker run --rm -it --network todo-app_app-network alpine sh`
    - Install curl inside the new container `apk add curl`
    - Test backend health `curl http://backend:5000/health`
- [x] Test from host machine(expose port temporarily)
    - Add the following to the backend service from docker-compose.yml 
    ```    
    ports:
        - "5003:5000"  # add this to test backend from the cli locally 
    ```
    - Restart backend `docker compose up -d backend`
    - Health check `curl http://localhost:5003/health`
    - Get all todos `curl http://localhost:5003/health`
    - Check backend logs `docker compose logs backend`
    Should see similar output:
    ```
    "GET /api/todos HTTP/1.1" 200
    "POST /api/todos HTTP/1.1" 201
    "PUT /api/todos/1 HTTP/1.1" 200
    "DELETE /api/todos/3 HTTP/1.1" 204
    ```
    - Delete the added port from the docker-compose.yml and restart container
- [x] Run a quick diagnostic to get full picture of containers, network and services
    ```
    docker compose ps
    docker network ls | grep docker-notes
    docker network inspect docker-notes-app_app-network | grep -A 20 "Containers"
- [x] Verify DNS works 
    - Open terminal in backend container `docker exec -it todo-backend sh`
    - Run `getent hosts db` - should return the container address of db(172.23.0.2      db)
    - Exit
- **How Docker DNS works**
    - Docker creates and embedded DNS server at 127.0.0.11 for each network
    - Containers on the same custom network can resolve each other by service name
    - The service name (db, backend) maps to the container's IP on the network
    - This only works on custom networks - default bridge doesn't support DNS resolution

 
