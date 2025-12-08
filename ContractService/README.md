# ContractService

ContractService håndterer oprettelse og visning af lejekontrakter i Bilabonnement-projektet.  
Servicen kører som en separat microservice med sin egen MySQL-database.

---

## Funktionalitet
- Opret lejekontrakter  
- Hent alle kontrakter  

---

## Kørsel via Docker

Start ContractService og databasen:

```bash
docker compose up --build contract-db contract-service
```

---

## API Endpoints

**GET /contracts**  
Henter alle kontrakter.

**POST /contracts**  
Opretter en ny kontrakt.  
Body eksempel:

```json
{
  "customer_id": 1,
  "car_id": 2,
  "start_date": "2024-01-01",
  "end_date": "2024-01-10"
}
```

Svar:

```json
{
  "message": "Lejeaftale oprettet",
  "contract_id": 1
}
```

---