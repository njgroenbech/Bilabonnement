# CarFleetService

CarFleetService håndterer bilflådestyring i Bilabonnement-projektet.  
Servicen kører som en separat microservice med sin egen MySQL-database.

---

## Funktionalitet

- Hent alle biler i flåden
- Tilføj nye biler til flåden
- Hent bil efter ID
- Hent biler efter mærke
- Filtrer biler efter pris pr. måned
- Hent tilgængelige biler til kontraktoprettelse
- Opdater bilstatus (available, rented, maintenance)
- Slet bil fra flåden

---

## Kørsel via Docker

Start CarFleetService og databasen:
```bash
docker compose up --build carfleet-db carfleet-service
```

---

## API Endpoints

**GET /cars**  
Henter alle biler i flåden.

**POST /cars**  
Tilføjer en ny bil til flåden.  
Body eksempel:
```json
{
  "brand": "Tesla",
  "model": "Model 3",
  "year": 2023,
  "license_plate": "AB12345",
  "km_driven": 5000,
  "fuel_type": "electric",
  "status": "available",
  "location": "Copenhagen",
  "purchase_price": 450000,
  "sub_type": "subscription",
  "sub_price_per_month": 6500
}
```

**GET /cars/{car_id}**  
Henter en specifik bil efter ID.

**GET /cars/{brand}**  
Henter alle biler af et bestemt mærke.

**GET /cars/price?min_price={min}&max_price={max}**  
Henter biler inden for en prisklasse sorteret efter pris.

**GET /cars/{brand}/{model}/{year}/{fuel_type}**  
Henter tilgængelige biler med præcise specifikationer til kontraktoprettelse.

**PATCH /cars/{car_id}/status**  
Opdaterer en bils status.  
Body eksempel:
```json
{
  "status": "rented"
}
```

Gyldige statusværdier: `available`, `rented`, `maintenance`

**DELETE /cars/{car_id}**  
Sletter en bil fra flåden.

---
