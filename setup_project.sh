#!/bin/bash

# Crear estructura de carpetas
mkdir -p myproject/app/api
mkdir -p myproject/app/config
mkdir -p myproject/app/domain/entities
mkdir -p myproject/app/domain/services
mkdir -p myproject/app/infrastructure/repository
mkdir -p myproject/app/interface/controllers
mkdir -p myproject/app/tests/domain
mkdir -p myproject/app/tests/interface

# Crear archivos necesarios
touch myproject/app/api/__init__.py
touch myproject/app/api/routes.py
touch myproject/app/config/__init__.py
touch myproject/app/config/config.py
touch myproject/app/domain/__init__.py
touch myproject/app/domain/entities/user.py
touch myproject/app/domain/services/user_service.py
touch myproject/app/infrastructure/__init__.py
touch myproject/app/infrastructure/firebase_client.py
touch myproject/app/infrastructure/repository/user_repository.py
touch myproject/app/interface/__init__.py
touch myproject/app/interface/controllers/user_controller.py
touch myproject/app/tests/__init__.py
touch myproject/app/tests/domain/test_user_service.py
touch myproject/app/tests/interface/test_user_controller.py

touch myproject/Dockerfile
touch myproject/docker-compose.yml
touch myproject/requirements.txt
touch myproject/README.md

echo "Estructura de proyecto creada con éxito."
