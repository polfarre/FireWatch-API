# FireWatch-API
FireWatch API es el componente backend de la plataforma FireWatch, diseñada para la monitorización y alerta de incendios a nivel mundial en tiempo real. Esta API proporciona los servicios necesarios para gestionar y manipular los datos de incendios obtenidos de la API de NASA FIRMS.


Como instalar el repo por primera vez:

- Clonar el repositorio de git

- Instalar Docker y Docker Compose:

    - Para ubuntu:
        sudo apt-get update
        sudo apt-get install \
        ca-certificates \
        curl \
        gnupg \
        lsb-release

        sudo mkdir -p /etc/apt/keyrings
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

        echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

        sudo apt-get update
        sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

    - Para Windows y macOS: 
        Descargar e instalar Docker Desktop desde Docker.

    - Instalar Docker Compose (si no está incluido):
        sudo curl -L "https://github.com/docker/compose/releases/download/v2.3.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose

    - Construir y Ejecutar la Aplicación con Docker:
        1. Construir y ejecutar los contenedores:
            docker-compose up --build
        2. Verificar que la API esté en funcionamiento:
            Abre tu navegador y navega a http://localhost:8000. Deberías ver la respuesta JSON {"Hello": "World"}.