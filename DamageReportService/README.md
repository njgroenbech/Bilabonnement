# DamageReportService

DamageReportService håndterer skaderapportering med AI-assisteret billedvurdering i Bilabonnement-projektet.  
Servicen kører som en separat microservice med sin egen MySQL-database.

---

## Funktionalitet

- Opret skaderapporter baseret på uploadede billeder
- AI-assisteret vurdering af skader i tre kategorier
- Hent alle skaderapporter
- Automatisk kategorisering: ingen skader, mindre skader, mellemstore skader eller store skader

---

## Kørsel via Docker

Start DamageReportService og databasen:
```bash
docker compose up --build damage-report-db damage-report-service
```

---

## API Endpoints

**POST /damagecheck**  
Opretter en skaderapport baseret på uploadede billeder.  
Form-data eksempel:
```
images: [file1.jpg, file2.jpg, ...]
contract_id: 1
car_id: 2
```

Svar:
```json
{
  "report_id": 1,
  "overall_status": "damage_found",
  "color": "red",
  "message": "Skade fundet: MELLEMSTORE SKADER",
  "damage_level": "medium"
}
```

**Mulige svar-typer:**

- `overall_status: "clear"` (grøn) - Ingen skader fundet
- `overall_status: "unclear"` (gul) - Uklare billeder, tag nye
- `overall_status: "damage_found"` (rød) - Skader fundet med kategori:
  - `damage_level: "minor"` - Mindre kosmetiske skader
  - `damage_level: "medium"` - Mellemstore skader
  - `damage_level: "major"` - Store skader

**GET /reports**  
Henter alle skaderapporter sorteret efter oprettelsesdato (nyeste først).

---
