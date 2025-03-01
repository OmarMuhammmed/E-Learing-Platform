# eLearning Platform

## Overview
This eLearning platform is a full-featured online course management system built with Django. It allows instructors to create courses, manage content, and enroll students, while providing a seamless learning experience with real-time interactions.

## Features
- **Course Management**: Create, edit, and organize courses with structured chapters and lessons.
- **User Authentication**: Secure login, student enrollment, and role-based access control.
- **Content Management**: Supports various content types (text, images, videos) with polymorphic models.
- **Interactive Learning**: Drag-and-drop functionality for content reordering.
- **API Integration**: Built with Django REST Framework for flexible data access.
- **Real-Time Chat**: WebSocket-based chat using Django Channels and Redis.
- **Caching & Performance**: Optimized with Redis and Django cache framework.
- **Production-Ready Setup**: Dockerized deployment with PostgreSQL, Redis, Nginx, uWSGI, and Daphne.

## Tech Stack
- **Backend**: Django, Django REST Framework, Django Channels
- **Database**: PostgreSQL
- **Caching**: Redis
- **Containerization**: Docker, Docker Compose
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Authentication**: Django authentication with role-based access control
- **DevOps**: Nginx, uWSGI, Daphne

## Installation
### Prerequisites
- Docker & Docker Compose installed
- PostgreSQL & Redis setup (if not using Docker)

### Steps
```bash
# Clone the repository
git clone https://github.com/OmarMuhammmed/eLearning-Platform.git
cd eLearning-Platform

# Build and start the containers
docker-compose up --build
```
The application should now be running on `http://localhost:8000/`.

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).

