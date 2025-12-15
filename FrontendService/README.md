# FrontendService

FrontendService er en Streamlit-baseret brugergrænseflade til Bilabonnement-projektet.  
Servicen fungerer som klient og kommunikerer udelukkende via API Gateway.

---

## Funktionalitet

- **Dashboard**: Overblik over flåde, kunder, kontrakter og revenue-analytics
- **Car Management**: Administrer bilflåden (tilføj, vis, filtrer, slet)
- **Customer Management**: Håndter kundedata og kundeoplysninger
- **Contract Management**: Opret og administrer lejekontrakter
- **AI Damage Check**: Upload billeder og få AI-assisteret skadevurdering
- **Authentication**: Login med JWT-baseret adgangskontrol
- **Role-based Access**: Admin og employee roller med forskellige rettigheder

---

## Kørsel via Docker

Start FrontendService:
```bash
docker compose up --build frontend-service
```

Tilgå applikationen på: **http://localhost:3000**

**(Beware: If you have any other service running on port 3000, you will get errors)**

---

## Login Credentials

**Admin:**
- Username: `admin`
- Password: `password`

**Employee:**
- Username: `employee`
- Password: `password`

---

## Sider og Features

### 📊 Dashboard
- KPI metrics (total fleet, customers, active contracts)
- Fleet status breakdown
- Monthly revenue trend (kun admin)
- Revenue by car brand (kun admin)

### 🚗 Car Fleet Management
- Vis alle biler med filtre (status, brand, fuel type)
- Tilføj nye biler til flåden
- Slet biler fra flåden

### 👥 Customer Management
- Vis alle kunder med søgning og filtre
- Opret nye kunder
- Slet kunder (inklusiv tilhørende kontrakter)

### 📄 Contract Management
- Vis alle kontrakter
- Opret nye kontrakter (kun tilgængelige biler og kunder)
- Slet kontrakter

### 🧠 AI Damage Check
- Upload billeder af bil
- Få AI-vurdering af skader
- Generer skadesrapport knyttet til kontrakt

---

## Teknisk Stack

- **Framework**: Streamlit
- **Styling**: Custom CSS med Google Fonts (Inter)
- **Data Visualization**: Plotly, Pandas
- **API Communication**: Requests library
- **Authentication**: JWT tokens

---

## Struktur
```
FrontendService/
├── .streamlit/
│   └── config.toml           # Streamlit theme konfiguration
├── api/
│   └── api_client.py         # API kommunikation
├── components/
│   └── ui_components.py      # Genanvendelige UI komponenter
├── pages/
│   ├── dashboard_page.py     # Dashboard side
│   ├── cars_page.py          # Bilflåde side
│   ├── customer_page.py      # Kunde side
│   ├── contracts_page.py     # Kontrakt side
│   ├── ai_damage_page.py     # AI skade side
│   └── login_page.py         # Login side
├── utils/
│   ├── jwt_utils.py          # JWT token håndtering
│   └── style_loader.py       # CSS loader
├── global_styles.css         # Global styling
├── app.py                    # Main application
├── Dockerfile
└── requirements.txt
```

---
