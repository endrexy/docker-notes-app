## This is intended as a DEVOps sample project(minimal functionaliy) 
## Focus is on using Docker and implementing best practices in Docker.

### Multi-Service Architecture:
- PostgreSQL (Database Layer)
- Flask API - (Application Layer)
- Nginx (Web Layer)

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


 
