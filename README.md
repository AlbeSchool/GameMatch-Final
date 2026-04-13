# GameMatch

Studente: Alberto Russo  
Classe: 5WDINF  
Anno scolastico: 2025/2026

## 1. Proposta architetturale

GameMatch è pensato come un'applicazione fullstack moderna, organizzata con una netta separazione tra frontend, backend e database. Questa scelta migliora scalabilità, manutenzione e chiarezza progettuale.

### Stack tecnologico

#### Database

- PostgreSQL come database principale
- SQLite come alternativa leggera per lo sviluppo locale
- Supporto a relazioni complesse 1:N e N:M
- Vincoli di integrità e foreign key per garantire coerenza dei dati

#### Backend

- Python + FastAPI
- SQLAlchemy per la gestione del database
- Pydantic per validazione e serializzazione dei dati
- Documentazione automatica tramite Swagger/OpenAPI

#### Frontend

Per l'MVP sono possibili due strade:

- HTML, CSS e JavaScript vanilla per una soluzione semplice e immediata
- React per un'evoluzione futura con componenti riutilizzabili e migliore gestione dello stato

## 2. Architettura dell'applicazione

L'applicazione segue una Three-Tier Architecture:

Frontend -> Backend -> Database

### Flusso di funzionamento

1. L'utente interagisce con il frontend
2. Il frontend invia richieste HTTP al backend
3. Il backend valida i dati con Pydantic
4. Il backend legge o salva i dati nel database
5. Il backend restituisce una risposta JSON

## 3. Struttura del backend

Il backend è organizzato in modo modulare per semplificare sviluppo e manutenzione.

```text
app/
├── main.py          # Entry point FastAPI
├── database.py      # Connessione al database
├── models.py        # Modelli SQLAlchemy
├── schemas.py       # Modelli Pydantic
├── crud.py          # Operazioni sul database
├── routers/
│   ├── users.py
│   ├── teams.py
│   └── matches.py
└── utils/
    └── security.py  # Password e autenticazione
```

## 4. Proposta di deploy

### Ambiente di sviluppo

- GitHub Codespaces per lavorare online senza installazione locale
- Integrazione diretta con il repository GitHub

### Hosting backend

Soluzione principale:

- Webdock VPS
- Controllo completo dell'ambiente
- Possibilità di installare Python, PostgreSQL e Nginx

Alternative:

- Railway per un deploy semplice e veloce
- Render con supporto diretto a FastAPI

### Architettura di deploy

Browser utente -> Frontend -> Backend FastAPI -> Database PostgreSQL

### Docker opzionale

Per aumentare portabilità e coerenza tra ambienti:

- Container per il backend FastAPI
- Container per PostgreSQL
- Gestione tramite docker-compose

## 5. Sviluppo backend

### Architettura logica

Il backend segue un pattern Layered Architecture:

- Router: gestione degli endpoint API
- Schemas: validazione dati con Pydantic
- CRUD: operazioni sul database
- Models: definizione delle tabelle

### Flusso di un endpoint

Esempio: POST /users

1. Ricezione dati tramite UserCreate
2. Validazione con Pydantic
3. Invio al livello CRUD
4. Salvataggio nel database
5. Restituzione di UserRead

### Best practice adottate

- Separazione tra modelli di input e output
- Nessuna password nelle risposte
- Uso corretto delle foreign key
- Modellazione delle relazioni N:M tramite tabella ponte
- Validazione dei dati con Pydantic

### Sviluppi futuri

- Autenticazione con JWT
- Ranking ELO
- Chat in tempo reale con WebSocket
- Sistema tornei
- Integrazione con API di giochi esterni

## 6. Conclusione

L'architettura scelta per GameMatch fornisce una base solida, modulare e scalabile. FastAPI, PostgreSQL e Pydantic permettono di costruire un backend efficiente, ordinato ed estendibile, mantenendo al tempo stesso semplicità e chiarezza per un MVP.

---

# GameMatch - Dal Design ai Modelli Pydantic

Studente: Alberto Russo  
Corso: 5WDINF  
Docente: Zhongli Filippo Hu  
Anno accademico: 2025/2026

## Parte 1 - Presentazione del progetto

### 1. Concept del progetto

#### Nome dell'applicazione

GameMatch

#### Problem statement

Nel gaming multiplayer competitivo, i giocatori incontrano spesso difficoltà nel trovare compagni di squadra con livello simile, organizzare team in modo strutturato e pianificare match in modo ordinato. Le piattaforme comuni come Discord, Telegram o i forum non sono progettate per una gestione dati strutturata di team e partite.

GameMatch nasce per offrire una piattaforma backend pensata per la gestione organizzata di utenti, team e match.

### 2. Target audience

- Giocatori multiplayer online
- Community eSport amatoriali
- Studenti e giovani gamer tra 16 e 30 anni

### 3. Definizione dell'MVP

L'MVP include le funzionalità essenziali per gestire team e match.

#### Funzionalità incluse nella versione 1.0

- Registrazione utenti
- Creazione di team
- Creazione e pianificazione di match tra team

#### Funzionalità future

- Sistema ranking ELO
- Sistema tornei
- Chat interna ai team
- Integrazione con API esterne dei giochi

### 4. Modello dei dati UML

#### Entità principali

- User
- Game
- Team
- Match
- TeamMembership come tabella ponte per la relazione N:M

#### Descrizione delle entità

- User: id, username, email, password solo in input
- Game: id, name, genre
- Team: id, name, creator_id come FK verso User
- Match: id, scheduled_at, game_id, team1_id, team2_id
- TeamMembership: id, user_id, team_id

#### Relazioni

Relazione 1:N:

- User 1 -> Team N
- Un utente può creare più team

Relazione N:M:

- User N <-> Team M
- Un utente può appartenere a più team
- Un team può avere più utenti
- La relazione è modellata tramite TeamMembership

### 5. API progettate per l'MVP

#### POST /users

Crea un nuovo utente.

Esempio response:

```json
{
	"id": 1,
	"username": "proGamer",
	"email": "pro@email.com"
}
```

#### POST /teams

Crea un nuovo team.

Esempio response:

```json
{
	"id": 10,
	"name": "NightRaiders",
	"creator_id": 1
}
```

#### POST /matches

Crea una nuova partita.

Esempio response:

```json
{
	"id": 100,
	"scheduled_at": "2026-06-01T18:00:00",
	"game_id": 2,
	"team1_id": 10,
	"team2_id": 11
}
```

### 6. Scelte progettuali e criticità

#### Scelte progettuali

- Separazione chiara tra modelli Base, Create e Read
- Password esclusa dai modelli di output
- Relazione N:M gestita con tabella ponte
- Doppia FK in Match per distinguere i due team
- MVP mantenuto minimale per rispettare i requisiti

#### Criticità incontrate

- Modellazione coerente della relazione N:M con Pydantic
- Gestione di due foreign key verso la stessa entità nel modello Match
- Scelta tra nested models e lista di ID per le relazioni

## Parte 2 - Modelli Pydantic

### File consegnati

- schemas.py con i modelli Pydantic
- examples.json con esempi JSON validi

### Regole rispettate

- Il campo id compare solo nei modelli Read
- Le password non compaiono nei modelli di output
- Le relazioni 1:N sono rappresentate tramite FK
- Le relazioni N:M sono modellate in modo coerente con l'UML
- I campi opzionali sono dichiarati con Optional
- Sono state previste validazioni con Field ed EmailStr

### Struttura richiesta per ogni entità

Per ogni entità principale sono definiti:

- XBase: attributi comuni
- XCreate: modello di input per POST
- XRead: modello di output per response

### Esempio di output atteso

Gli esempi contenuti in examples.json includono almeno:

- User
- Team
- Match

## Conclusione

GameMatch traduce correttamente l'analisi concettuale in una specifica tecnica concreta tramite modelli Pydantic coerenti con l'UML progettato. La struttura dei modelli rispetta i principi di separazione tra input e output, gestione corretta delle relazioni e buona progettazione backend in ottica FastAPI.