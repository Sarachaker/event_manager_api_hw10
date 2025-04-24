# Event Manager API

A FastAPI-based REST API for user management with PostgreSQL, Docker, and JWT authentication.

## Closed Issues
- [Username Validation Enhancement](#issue-1)
- [Password Validation Enhancement](#issue-2)
- [Profile Update - Bio Only](#issue-3)
- [Profile Update - Picture URL Only](#issue-4)
- [Profile Update - Bio and Picture URL](#issue-5)
- [Fix OAuth Token Generation](#issue-6)

## Docker Hub
- Image: [sarachaker/event_manager_api](https://hub.docker.com/r/sarachaker/event_manager_api)

## Reflection
This assignment was a deep dive into backend development with FastAPI, SQLAlchemy, and Pydantic. I learned to implement robust validation, handle edge cases, and write comprehensive tests, achieving 90% coverage. Debugging OAuth issues taught me the importance of precise error handling. Collaborating via Git and GitHub honed my skills in branching, PRs, and code reviews, mirroring real-world workflows. Challenges like Docker setup and async programming pushed me to read documentation thoroughly and seek community support. This experience prepared me for professional API development and emphasized the value of automated testing.

## Setup
- Fork and clone the repository.
- Run `docker-compose up --build`.
- Access API at `http://localhost/docs` and PGAdmin at `http://localhost:5050`.
