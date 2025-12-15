# Bilabonnement.dk – Microservice Architecture

## Project Overview
This repository contains a **fictional case project** developed by Team Runddelens Ridere, as part of the 3rd semester IT Architecture course, based on **Bilabonnement.dk**.

The project translates **business processes (BPMN TO-BE)** and a **domain model** into a concrete **microservice-based system architecture** implemented as an MVP with test data.

---

## System Architecture and Docker-Based Development Environment
The system is designed as a **microservice architecture** running in Docker Compose. Each microservice is deployed in its own container with its own database, ensuring clear separation of responsibilities and data ownership.

The API Gateway acts as the single entry point, routing requests to relevant backend services. The frontend communicates exclusively through the gateway.

![System Architecture and Development Environment](https://github.com/user-attachments/assets/b879761c-12e5-4ec6-bf94-8cb6ddf59d7e)

---

## Microservices

| Service | Responsibility | Documentation |
|--------|---------------|---------------|
| **AuthorizationService** | Handles authentication and issues JWT tokens with role-based claims. | [README](./AuthorizationService/README.md) |
| **CarFleetService** | Manages cars in the fleet, including availability, status and vehicle information. | [README](./CarFleetService/README.md) |
| **ContractService** | Orchestrates contract creation by coordinating data from customer and car fleet services. | [README](./ContractService/README.md) |
| **CustomerInformationService** | Manages customer data and supports future business analytics use cases. | [README](./CustomerInformationService/README.md) |
| **DamageReportService** | Handles damage reporting, including image-based damage assessment (AI-assisted). | [README](./DamageReportService/README.md) |
| **FrontendService** | Streamlit-based frontend acting purely as a client and communicating via the API Gateway. | [README](./FrontendService/README.md) |

---

## API Gateway

### Available Endpoints
| Endpoint | Method | Description |
|--------|--------|-------------|
| `/auth/login` | POST | Authenticate user and issue JWT |
| `/cars` | GET / POST | Retrieve or create cars |
| `/customers` | GET / POST | Retrieve or create customers |
| `/contracts` | GET / POST | Retrieve or create contracts |
| `/damagecheck` | POST | Create damage report from images |
| `/reports` | GET | Retrieve damage reports |

---

## Communication Between Microservices
Microservices communicate via **synchronous REST (HTTP)** calls through the API Gateway. Selected services (e.g. ContractService) perform internal service-to-service communication to support coordinated business workflows.

---

## Database Design
Each microservice owns its own **MySQL** database. Relations across services are handled at application level using shared identifiers (e.g. `car_id`, `customer_id`).

---

## Installation and Running the System

### Prerequisites
- Docker Desktop
- (Optional) Visual Studio Code

### Running the System
First make sure Docker Desktop is running, it should look something like this:

![Docker Desktop](https://github.com/user-attachments/assets/820ad8f3-3b34-42dd-a886-6480e4a5271c)

Now go to the repository on the master branch and copy the web URL:

![Copy repo URL](https://github.com/user-attachments/assets/f0702f20-44e8-40c6-8c4a-cbc593ef3b7b)

You may download the ZIP file and run the project from a terminal.  
We prefer to run it in VS Code and will guide you through that.

Press **Clone Git Repository**, insert the repository URL and clone from:  
https://github.com/njgroenbech/Bilabonnement

![Clone repo](https://github.com/user-attachments/assets/ca3b446d-7796-4aa4-8d83-fb3aa546e21d)

Create a new `.env` file in the project root and add:
```
JWT_SECRET=supersecretkey
```

The value does not matter – only the variable name is required. Remember to save the file.

![.env file](https://github.com/user-attachments/assets/22d86b46-9f03-4e91-a740-d818aad0b49c)

Open a new terminal and run:
```bash
docker compose up --build
```

![Docker compose](https://github.com/user-attachments/assets/0dda07e5-9dcb-43fb-baca-7b73b121ef2b)

Go to: http://localhost:3000

**(Beware: If you have any other service running on port 3000, you will get errors)**

**Login credentials:**
- Username: `admin`
- Password: `password`

You are now logged into the **Bilabonnement dashboard**.

To stop the system:
```bash
docker compose down
```

Thank you for trying our system ❤️
