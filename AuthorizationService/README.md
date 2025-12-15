# AuthorizationService

## Hvad gør denne microservice?
- Dette er et `/login` endpoint som validerer brugernavn/password mod en MySQL database.
- Returnerer en JWT (feltet `JWT_token`) med `sub` (username) og `role`, så der er forskel på, hvad man har adgang til afhængig af, om man er admin eller almindelig user.

## Filer
- `app.py` - Flask app og `/login` endpoint.
- `db.py` - Database-hjælper (forbindelse til MySQL og `validate_user`).
- `db_init/init.sql` - MySQL init-script som opretter tabel og indsætter default brugere.
- `requirements.txt` - Python dependencies.

## Environment variables
- `JWT_SECRET` - hemmelig nøgle for JWT (brug .env i projektroden).
- `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DB` - databaseforbindelse (disse variabler bliver angivet i `docker-compose.yml` når man kører programmet i compose).

## Kør med Docker Compose
1. Sørg for at `.env` indeholder `JWT_SECRET`. Sæt `JWT_SECRET` til whatever. Fx 123. Det er vigtigt, at der ikke er mellemrum før og efter lighedstegnet. Korrekt eksemepel: JWT_SECRET=123

2. Start service
   ```bash
   docker compose up --build
   ```
3. MySQL initialiseres automatisk fra `AuthorizationService/db_init/init.sql`

## Test login via vores gateway med terminalen
- Via gateway :
  ```bash
  curl -X POST http://localhost:5001/auth/login \
    -H 'Content-Type: application/json' \
    -d '{"username":"admin","password":"password"}' | jq
  ```

## Output
JSON med `JWT_token`, `token_type` og `role`.

