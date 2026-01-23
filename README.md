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
- [ ] i01 - Improve environment variables and store passwords as secrets not in plain text
- [ ] i02 - Improve dependencies by adding health checks


