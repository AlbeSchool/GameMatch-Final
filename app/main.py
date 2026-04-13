from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from sqlalchemy import inspect

from app.database import engine, init_db
from app.routers import users, teams, matches
from schemas import GameRead, MatchRead, TeamRead, UserRead

app = FastAPI(
    title="GameMatch API",
    description="Backend per la gestione di team e partite multiplayer",
    version="1.0.0",
)

app.include_router(users.router)
app.include_router(teams.router)
app.include_router(matches.router)

_COMMON_STYLES = """
    :root {
        color-scheme: dark;
        --bg: #0b1020;
        --panel: #121a33;
        --panel-2: #182344;
        --text: #eef2ff;
        --muted: #aab4d6;
        --accent: #67e8f9;
        --accent-2: #a78bfa;
        --green: #4ade80;
        --red: #f87171;
    }
    * { box-sizing: border-box; }
    body {
        margin: 0;
        font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
        background:
            radial-gradient(circle at top left, rgba(103, 232, 249, 0.18), transparent 35%),
            radial-gradient(circle at top right, rgba(167, 139, 250, 0.18), transparent 30%),
            linear-gradient(180deg, #0b1020 0%, #060912 100%);
        color: var(--text);
        min-height: 100vh;
        padding: 32px;
    }
    .wrap { max-width: 1100px; margin: 0 auto; }
    .card {
        background: rgba(18, 26, 51, 0.88);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 36px;
        box-shadow: 0 24px 80px rgba(0, 0, 0, 0.35);
        backdrop-filter: blur(16px);
    }
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 14px;
        border-radius: 999px;
        background: rgba(103, 232, 249, 0.12);
        color: var(--accent);
        font-size: 0.9rem;
        letter-spacing: 0.02em;
        margin-bottom: 16px;
        border: 1px solid rgba(103, 232, 249, 0.2);
    }
    .badge-green {
        background: rgba(74, 222, 128, 0.12);
        color: var(--green);
        border-color: rgba(74, 222, 128, 0.22);
    }
    .dot {
        width: 8px; height: 8px;
        border-radius: 50%;
        background: currentColor;
        box-shadow: 0 0 0 4px color-mix(in srgb, currentColor 25%, transparent);
    }
    h1 { margin: 0 0 12px; font-size: clamp(2rem, 4vw, 3.5rem); line-height: 1; }
    h2 { margin: 0 0 8px; font-size: 1.1rem; }
    p { margin: 0; color: var(--muted); font-size: 1rem; line-height: 1.65; }
    .grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 16px;
        margin-top: 24px;
    }
    .panel {
        background: linear-gradient(180deg, rgba(24, 35, 68, 0.9), rgba(18, 26, 51, 0.9));
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 18px;
        padding: 20px;
    }
    .links {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-top: 26px;
    }
    a {
        color: var(--text);
        text-decoration: none;
        background: linear-gradient(90deg, rgba(103, 232, 249, 0.15), rgba(167, 139, 250, 0.15));
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 10px 18px;
        border-radius: 14px;
        transition: border-color 0.2s;
        font-size: 0.95rem;
    }
    a:hover { border-color: rgba(103, 232, 249, 0.5); }
    code { color: var(--accent); font-size: 0.95em; }
    @media (max-width: 700px) { .grid { grid-template-columns: 1fr; } }
"""


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/", response_class=HTMLResponse)
def root() -> HTMLResponse:
    html = f"""<!doctype html>
<html lang="it">
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <title>GameMatch API</title>
    <style>{_COMMON_STYLES}</style>
</head>
<body>
<main class="wrap">
    <div class="card">
        <div class="badge">🎮 GameMatch API online</div>
        <h1>GameMatch</h1>
        <p>
            Backend FastAPI per la gestione di utenti, team e partite multiplayer.
            Registra giocatori, crea team e pianifica match competitivi.
        </p>

        <section class="grid" aria-label="Stato progetto">
            <article class="panel">
                <h2>🟢 Stato</h2>
                <p>Server avviato e pronto a ricevere richieste.</p>
            </article>
            <article class="panel">
                <h2>📡 Endpoint utili</h2>
                <p><code>/health</code> · <code>/examples</code> · <code>/docs</code></p>
            </article>
            <article class="panel">
                <h2>🗄️ Database</h2>
                <p>users, games, teams, matches, team_memberships.</p>
            </article>
        </section>

        <nav class="links">
            <a href="/docs">📖 Swagger UI</a>
            <a href="/redoc">📘 ReDoc</a>
            <a href="/health">💚 Stato sistema</a>
            <a href="/examples">🃏 Esempi dati</a>
        </nav>
    </div>
</main>
</body>
</html>"""
    return HTMLResponse(content=html)


@app.get("/health", response_class=HTMLResponse)
def health() -> HTMLResponse:
    table_names = inspect(engine).get_table_names()
    table_count = len(table_names)
    last_check = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    chips = "".join(
        f'<span style="display:inline-flex;margin:6px 6px 0 0;padding:6px 12px;'
        f'border-radius:999px;background:rgba(103,232,249,0.12);'
        f'color:var(--accent);border:1px solid rgba(103,232,249,0.2);font-size:.88rem;">'
        f'{name}</span>'
        for name in table_names
    ) or '<span style="color:var(--muted)">Nessuna tabella trovata</span>'

    html = f"""<!doctype html>
<html lang="it">
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <title>GameMatch — Stato del sistema</title>
    <style>
        {_COMMON_STYLES}
        .hero {{
            display: grid;
            grid-template-columns: 1.4fr 0.9fr;
            gap: 20px;
            align-items: stretch;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 14px;
            margin-top: 20px;
        }}
        .stat {{
            background: rgba(24, 35, 68, 0.85);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 16px;
            padding: 16px;
        }}
        .stat .label {{ color: var(--muted); font-size: .85rem; }}
        .stat .value {{ font-size: 1.35rem; margin-top: 8px; font-weight: 600; }}
        .status-ring {{
            width: 200px; height: 200px; border-radius: 50%;
            margin: 0 auto;
            display: grid; place-items: center;
            background:
                radial-gradient(circle at center, rgba(7,17,31,.95) 0 58%, transparent 59%),
                conic-gradient(from 220deg, var(--green), var(--accent), var(--accent-2), var(--green));
        }}
        .status-core {{
            width: 150px; height: 150px; border-radius: 50%;
            display: grid; place-items: center; text-align: center;
            background: linear-gradient(180deg, rgba(20,31,58,.98), rgba(10,18,35,.98));
            border: 1px solid rgba(255,255,255,.08);
        }}
        .status-core strong {{ display:block; font-size:1.1rem; margin-bottom:4px; }}
        .status-core span {{ color:var(--muted); font-size:.85rem; }}
        @media (max-width: 800px) {{ .hero, .stats {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
<main class="wrap">
    <div class="hero" style="margin-bottom:20px;">
        <section class="card">
            <div class="badge badge-green"><span class="dot"></span> Controllo in tempo reale</div>
            <h1>Stato del sistema</h1>
            <p>Dashboard per verificare rapidamente se GameMatch è online e quali tabelle sono attive.</p>

            <div class="stats">
                <div class="stat">
                    <div class="label">Stato</div>
                    <div class="value" style="color:var(--green)">Operativo</div>
                </div>
                <div class="stat">
                    <div class="label">Tabelle DB</div>
                    <div class="value">{table_count}</div>
                </div>
                <div class="stat">
                    <div class="label">Ultima verifica</div>
                    <div class="value" style="font-size:.95rem;line-height:1.4;">{last_check}</div>
                </div>
            </div>

            <div style="margin-top:20px;">
                <p style="margin-bottom:10px;">Tabelle presenti nel database</p>
                <div>{chips}</div>
            </div>
        </section>

        <aside class="card" style="display:grid;place-items:center;text-align:center;">
            <div class="status-ring">
                <div class="status-core">
                    <div>
                        <strong>Online</strong>
                        <span>Servizi operativi</span>
                    </div>
                </div>
            </div>
        </aside>
    </div>

    <section class="grid">
        <article class="panel"><h2>⚡ API</h2><p>Endpoint salute, esempi e docs disponibili.</p></article>
        <article class="panel"><h2>🗄️ Database</h2><p>Modello relazionale con 5 tabelle attive.</p></article>
        <article class="panel"><h2>🔧 Build</h2><p>FastAPI, Pydantic e SQLAlchemy pronti.</p></article>
        <article class="panel"><h2>☁️ Deploy</h2><p>Struttura compatibile con cloud standard.</p></article>
    </section>

    <nav class="links">
        <a href="/">🏠 Home</a>
        <a href="/docs">📖 Swagger UI</a>
        <a href="/examples">🃏 Esempi dati</a>
    </nav>
</main>
</body>
</html>"""
    return HTMLResponse(content=html)


@app.get("/examples", response_class=HTMLResponse)
def examples() -> HTMLResponse:
    user = UserRead(id=1, username="proGamer", email="pro@email.com")
    team = TeamRead(
        id=10,
        name="NightRaiders",
        creator_id=1,
        members=[
            UserRead(id=1, username="proGamer", email="pro@email.com"),
            UserRead(id=2, username="shadowHunter", email="shadow@email.com"),
        ],
    )
    match = MatchRead(
        id=100,
        scheduled_at=datetime.fromisoformat("2026-06-01T18:00:00"),
        game_id=2,
        team1_id=10,
        team2_id=11,
        game=GameRead(id=2, name="Valorant", genre="FPS"),
        team1=TeamRead(id=10, name="NightRaiders", creator_id=1, members=[]),
        team2=TeamRead(id=11, name="SkyHunters", creator_id=3, members=[]),
    )

    members_html = "".join(
        f"""<div style="display:flex;align-items:center;gap:10px;padding:8px 0;
            border-bottom:1px solid rgba(255,255,255,0.05);">
            <div style="width:32px;height:32px;border-radius:50%;
                background:linear-gradient(135deg,var(--accent),var(--accent-2));
                display:grid;place-items:center;font-weight:700;font-size:.85rem;">
                {m.username[0].upper()}
            </div>
            <div>
                <div style="font-size:.95rem;font-weight:500;">{m.username}</div>
                <div style="font-size:.8rem;color:var(--muted);">{m.email}</div>
            </div>
        </div>"""
        for m in team.members
    )

    html = f"""<!doctype html>
<html lang="it">
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <title>GameMatch — Esempi dati</title>
    <style>
        {_COMMON_STYLES}
        .section-title {{
            font-size: .78rem;
            text-transform: uppercase;
            letter-spacing: .1em;
            color: var(--muted);
            margin: 0 0 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .section-title::after {{
            content: '';
            flex: 1;
            height: 1px;
            background: rgba(255,255,255,0.07);
        }}
        .field {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            font-size: .9rem;
        }}
        .field:last-child {{ border-bottom: none; }}
        .field-key {{ color: var(--muted); }}
        .field-val {{ font-weight: 500; color: var(--text); }}
        .pill {{
            display: inline-flex;
            padding: 4px 10px;
            border-radius: 999px;
            font-size: .8rem;
            font-weight: 600;
        }}
        .pill-blue {{
            background: rgba(103,232,249,0.15);
            color: var(--accent);
            border: 1px solid rgba(103,232,249,0.25);
        }}
        .pill-violet {{
            background: rgba(167,139,250,0.15);
            color: var(--accent-2);
            border: 1px solid rgba(167,139,250,0.25);
        }}
        .pill-green {{
            background: rgba(74,222,128,0.15);
            color: var(--green);
            border: 1px solid rgba(74,222,128,0.25);
        }}
        .vs {{
            font-size: 1.6rem;
            font-weight: 800;
            color: var(--accent-2);
            text-align: center;
            padding: 12px 0;
            letter-spacing: .05em;
        }}
        .team-badge {{
            padding: 14px 16px;
            border-radius: 14px;
            border: 1px solid rgba(255,255,255,0.07);
            text-align: center;
        }}
        .team-badge.t1 {{ background: rgba(103,232,249,0.08); }}
        .team-badge.t2 {{ background: rgba(167,139,250,0.08); }}
        .team-badge .name {{ font-size: 1.05rem; font-weight: 700; margin-bottom:4px; }}
        .team-badge .meta {{ font-size: .8rem; color: var(--muted); }}
    </style>
</head>
<body>
<main class="wrap">
    <div style="margin-bottom:28px;">
        <div class="badge">🃏 Esempi dati GameMatch</div>
        <h1>Anteprima schemi</h1>
        <p>Rappresentazione visiva degli oggetti restituiti dall'API: utente, team e partita.</p>
    </div>

    <!-- Grid principale -->
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px;margin-bottom:20px;">

        <!-- USER CARD -->
        <article class="card">
            <div class="section-title">👤 Utente</div>
            <div style="display:flex;align-items:center;gap:16px;margin-bottom:20px;">
                <div style="width:56px;height:56px;border-radius:50%;flex-shrink:0;
                    background:linear-gradient(135deg,var(--accent),var(--accent-2));
                    display:grid;place-items:center;font-size:1.5rem;font-weight:800;">
                    {user.username[0].upper()}
                </div>
                <div>
                    <div style="font-size:1.2rem;font-weight:700;">{user.username}</div>
                    <div style="color:var(--muted);font-size:.9rem;">{user.email}</div>
                </div>
            </div>
            <div class="field"><span class="field-key">ID</span><span class="field-val pill pill-blue">#{user.id}</span></div>
            <div class="field"><span class="field-key">Username</span><span class="field-val">{user.username}</span></div>
            <div class="field"><span class="field-key">Email</span><span class="field-val">{user.email}</span></div>
        </article>

        <!-- TEAM CARD -->
        <article class="card">
            <div class="section-title">🛡️ Team</div>
            <div style="display:flex;align-items:center;gap:16px;margin-bottom:20px;">
                <div style="width:56px;height:56px;border-radius:14px;flex-shrink:0;
                    background:linear-gradient(135deg,#7c3aed,var(--accent-2));
                    display:grid;place-items:center;font-size:1.6rem;">🏰</div>
                <div>
                    <div style="font-size:1.2rem;font-weight:700;">{team.name}</div>
                    <div style="color:var(--muted);font-size:.9rem;">Creato da utente #{team.creator_id}</div>
                </div>
            </div>
            <div class="field"><span class="field-key">ID</span><span class="field-val pill pill-violet">#{team.id}</span></div>
            <div class="field"><span class="field-key">Membri</span><span class="field-val pill pill-green">{len(team.members)} giocatori</span></div>
            <div style="margin-top:14px;">
                <div style="color:var(--muted);font-size:.8rem;margin-bottom:8px;">ROSTER</div>
                {members_html}
            </div>
        </article>

    </div>

    <!-- MATCH CARD (full width) -->
    <article class="card">
        <div class="section-title">⚔️ Partita</div>

        <!-- Teams VS row -->
        <div style="display:grid;grid-template-columns:1fr auto 1fr;gap:16px;align-items:center;margin-bottom:24px;">
            <div class="team-badge t1">
                <div class="name">{match.team1.name if match.team1 else "Team 1"}</div>
                <div class="meta">ID #{match.team1_id}</div>
            </div>
            <div class="vs">VS</div>
            <div class="team-badge t2">
                <div class="name">{match.team2.name if match.team2 else "Team 2"}</div>
                <div class="meta">ID #{match.team2_id}</div>
            </div>
        </div>

        <!-- Match details grid -->
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;">
            <div class="panel">
                <div style="color:var(--muted);font-size:.8rem;margin-bottom:6px;">🎮 GIOCO</div>
                <div style="font-size:1rem;font-weight:600;">{match.game.name if match.game else "—"}</div>
                <div style="margin-top:4px;"><span class="pill pill-blue">{match.game.genre if match.game else "—"}</span></div>
            </div>
            <div class="panel">
                <div style="color:var(--muted);font-size:.8rem;margin-bottom:6px;">📅 DATA PARTITA</div>
                <div style="font-size:1rem;font-weight:600;">{match.scheduled_at.strftime("%d %b %Y")}</div>
                <div style="color:var(--muted);font-size:.9rem;">{match.scheduled_at.strftime("%H:%M")}</div>
            </div>
            <div class="panel">
                <div style="color:var(--muted);font-size:.8rem;margin-bottom:6px;">🆔 MATCH ID</div>
                <div style="font-size:1.3rem;font-weight:700;color:var(--accent);">#{match.id}</div>
            </div>
        </div>
    </article>

    <nav class="links" style="margin-top:24px;">
        <a href="/">🏠 Home</a>
        <a href="/health">💚 Stato sistema</a>
        <a href="/docs">📖 Swagger UI</a>
    </nav>
</main>
</body>
</html>"""
    return HTMLResponse(content=html)
