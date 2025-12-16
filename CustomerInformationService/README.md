# CustomerInformationService

CustomerInformationService håndterer kundeinformation i Bilabonnement-projektet.  
Servicen kører som en separat microservice med sin egen MySQL-database.

---

## Funktionalitet

- Hent alle kunder
- Tilføj nye kunder
- Hent kunde efter ID
- Hent kunde efter email
- Slet kunde (inklusiv tilhørende kontrakter)

---

## Kørsel via Docker

Start CustomerInformationService og databasen:
```bash
docker compose up --build customer-information-db customer-information-service
```

---

## API Endpoints

**GET /customers**  
Henter alle kunder.

**POST /customers**  
Opretter en ny kunde.  
Body eksempel, Denne datastrutur er også forventet i vores udfyldningsmulighed i hjemmesiden
```json
{
  "name": "Anders",
  "last_name": "Nielsen",
  "address": "Vestergade 45, 2. tv",
  "postal_code": "1000",
  "city": "København",
  "email": "anders.nielsen@email.dk",
  "cpr_number": "150678-2341",
  "registration_number": 1234,
  "account_number": 1234567,
  "comments": "Preferred customer"
}
```

Svar:
```json
{
  "customer_id": 1,
  "name": "Anders",
  "last_name": "Nielsen",
  "address": "Vestergade 45, 2. tv",
  "postal_code": "1000",
  "city": "København",
  "email": "anders.nielsen@email.dk",
  "cpr_number": "150678-2341",
  "registration_number": 1234,
  "account_number": 1234567,
  "comments": "Preferred customer"
}
```

**GET /customers/{customer_id}**  
Henter en specifik kunde efter ID.

**GET /customers/{email}**  
Henter kunde-ID og basisoplysninger efter email (bruges til kontraktoprettelse).

**DELETE /customers/{customer_id}**  
Sletter en kunde og alle tilhørende kontrakter. Frigør automatisk biler knyttet til slettede kontrakter.

---
