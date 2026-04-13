from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from sqlalchemy import inspect

from app.database import engine, init_db
from app.schemas import GameRead, MatchRead, TeamRead, UserRead


app = FastAPI(title="GameMatch", version="1.0.0")


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/")
def root() -> HTMLResponse:
        html = """
        <!doctype html>
        <html lang="it">
            <head>
                <meta charset="utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <title>GameMatch API</title>
                <style>
                    :root {
                        color-scheme: dark;
                        --bg: #0b1020;
                        --panel: #121a33;
                        --panel-2: #182344;
                        --text: #eef2ff;
                        --muted: #aab4d6;
                        --accent: #67e8f9;
                        --accent-2: #a78bfa;
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
                        display: grid;
                        place-items: center;
                        padding: 32px;
                    }
                    .card {
                        width: min(920px, 100%);
                        background: rgba(18, 26, 51, 0.88);
                        border: 1px solid rgba(255, 255, 255, 0.08);
                        border-radius: 24px;
                        padding: 36px;
                        box-shadow: 0 24px 80px rgba(0, 0, 0, 0.35);
                        backdrop-filter: blur(16px);
                    }
                    .badge {
                        display: inline-flex;
                        padding: 8px 12px;
                        border-radius: 999px;
                        background: rgba(103, 232, 249, 0.12);
                        color: var(--accent);
                        font-size: 0.9rem;
                        letter-spacing: 0.02em;
                        margin-bottom: 16px;
                    }
                    h1 {
                        margin: 0 0 12px;
                        font-size: clamp(2.2rem, 4vw, 4rem);
                        line-height: 1;
                    }
                    p {
                        margin: 0;
                        color: var(--muted);
                        font-size: 1.05rem;
                        line-height: 1.65;
                    }
                    .grid {
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                        gap: 16px;
                        margin-top: 28px;
                    }
                    .panel {
                        background: linear-gradient(180deg, rgba(24, 35, 68, 0.9), rgba(18, 26, 51, 0.9));
                        border: 1px solid rgba(255, 255, 255, 0.06);
                        border-radius: 18px;
                        padding: 18px;
                    }
                    .panel h2 {
                        margin: 0 0 10px;
                        font-size: 1rem;
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
                        background: linear-gradient(90deg, rgba(103, 232, 249, 0.18), rgba(167, 139, 250, 0.18));
                        border: 1px solid rgba(255, 255, 255, 0.1);
                        padding: 12px 16px;
                        border-radius: 14px;
                    }
                    a:hover {
                        border-color: rgba(103, 232, 249, 0.45);
                    }
                    code {
                        color: var(--accent);
                    }
                </style>
            </head>
            <body>
                <main class="card">
                    <div class="badge">GameMatch API online</div>
                    <h1>GameMatch</h1>
                    <p>
                        Backend FastAPI per la gestione di utenti, team e match.
                        Il progetto espone una root informativa, endpoint di salute e
                        una pagina esempi per verificare rapidamente gli schemi Pydantic.
                    </p>

                    <section class="grid" aria-label="Stato progetto">
                        <article class="panel">
                            <h2>Stato</h2>
                            <p>Server avviato e pronto a ricevere richieste.</p>
                        </article>
                        <article class="panel">
                            <h2>Endpoint utili</h2>
                            <p><code>/health</code>, <code>/examples</code>, <code>/docs</code></p>
                        </article>
                        <article class="panel">
                            <h2>Database</h2>
                            <p>users, games, teams, matches, team_memberships.</p>
                        </article>
                    </section>

                    <div class="links">
                        <a href="/docs">Apri Swagger UI</a>
                        <a href="/redoc">Apri ReDoc</a>
                        <a href="/status">Verifica stato</a>
                        <a href="/tables">Vedi tabelle DB</a>
                        <a href="/examples">Vedi esempi JSON</a>
                    </div>
                </main>
            </body>
        </html>
        """
        return HTMLResponse(content=html)


@app.get("/health")
def health() -> HTMLResponse:
        table_names = inspect(engine).get_table_names()
        table_count = len(table_names)
        active_status = "Operativo"
        last_check = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        html = f"""
        <!doctype html>
        <html lang="it">
            <head>
                <meta charset="utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <title>GameMatch - Stato del sito</title>
                <style>
                    :root {{
                        color-scheme: dark;
                        --bg: #07111f;
                        --card: rgba(12, 21, 40, 0.92);
                        --card-2: rgba(20, 31, 58, 0.95);
                        --text: #edf2ff;
                        --muted: #9fb0d0;
                        --green: #4ade80;
                        --cyan: #67e8f9;
                        --violet: #a78bfa;
                    }}
                    * {{ box-sizing: border-box; }}
                    body {{
                        margin: 0;
                        min-height: 100vh;
                        font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
                        color: var(--text);
                        background:
                            radial-gradient(circle at 20% 20%, rgba(103, 232, 249, 0.18), transparent 25%),
                            radial-gradient(circle at 80% 0%, rgba(167, 139, 250, 0.18), transparent 30%),
                            linear-gradient(180deg, #07111f 0%, #050810 100%);
                        padding: 32px;
                    }}
                    .wrap {{ max-width: 1100px; margin: 0 auto; }}
                    .hero {{
                        display: grid;
                        grid-template-columns: 1.4fr 0.9fr;
                        gap: 20px;
                        align-items: stretch;
                    }}
                    .panel {{
                        background: var(--card);
                        border: 1px solid rgba(255,255,255,0.08);
                        border-radius: 28px;
                        padding: 28px;
                        box-shadow: 0 24px 80px rgba(0,0,0,0.35);
                        backdrop-filter: blur(18px);
                    }}
                    .title {{ margin: 0 0 12px; font-size: clamp(2.2rem, 4vw, 4.2rem); line-height: 1; }}
                    .subtitle {{ margin: 0; color: var(--muted); font-size: 1.05rem; line-height: 1.7; }}
                    .badge {{
                        display: inline-flex;
                        align-items: center;
                        gap: 10px;
                        padding: 10px 14px;
                        border-radius: 999px;
                        background: rgba(74, 222, 128, 0.12);
                        color: var(--green);
                        margin-bottom: 18px;
                        border: 1px solid rgba(74, 222, 128, 0.22);
                        font-size: 0.95rem;
                    }}
                    .dot {{
                        width: 10px;
                        height: 10px;
                        border-radius: 50%;
                        background: var(--green);
                        box-shadow: 0 0 0 6px rgba(74, 222, 128, 0.18);
                    }}
                    .status-ring {{
                        width: 220px;
                        height: 220px;
                        border-radius: 50%;
                        margin: 0 auto;
                        display: grid;
                        place-items: center;
                        background:
                            radial-gradient(circle at center, rgba(7, 17, 31, 0.95) 0 58%, transparent 59%),
                            conic-gradient(from 220deg, var(--green), var(--cyan), var(--violet), var(--green));
                        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.06);
                    }}
                    .status-core {{
                        width: 165px;
                        height: 165px;
                        border-radius: 50%;
                        display: grid;
                        place-items: center;
                        text-align: center;
                        background: linear-gradient(180deg, rgba(20,31,58,0.98), rgba(10,18,35,0.98));
                        border: 1px solid rgba(255,255,255,0.08);
                    }}
                    .status-core strong {{ display: block; font-size: 1.25rem; margin-bottom: 4px; }}
                    .status-core span {{ color: var(--muted); font-size: 0.92rem; }}
                    .stats {{
                        display: grid;
                        grid-template-columns: repeat(3, minmax(0, 1fr));
                        gap: 16px;
                        margin-top: 20px;
                    }}
                    .stat {{
                        background: var(--card-2);
                        border: 1px solid rgba(255,255,255,0.06);
                        border-radius: 18px;
                        padding: 18px;
                    }}
                    .stat .label {{ color: var(--muted); font-size: 0.88rem; }}
                    .stat .value {{ font-size: 1.4rem; margin-top: 10px; }}
                    .section {{ margin-top: 22px; }}
                    .grid {{
                        display: grid;
                        grid-template-columns: repeat(4, minmax(0, 1fr));
                        gap: 16px;
                        margin-top: 20px;
                    }}
                    .mini {{
                        background: var(--card-2);
                        border: 1px solid rgba(255,255,255,0.06);
                        border-radius: 18px;
                        padding: 18px;
                    }}
                    .mini h2 {{ margin: 0 0 8px; font-size: 1rem; }}
                    .mini p {{ margin: 0; color: var(--muted); line-height: 1.55; }}
                    .table-chip {{
                        display: inline-flex;
                        margin: 8px 8px 0 0;
                        padding: 8px 12px;
                        border-radius: 999px;
                        background: rgba(103, 232, 249, 0.12);
                        color: var(--cyan);
                        border: 1px solid rgba(103, 232, 249, 0.18);
                    }}
                    .links {{ display: flex; flex-wrap: wrap; gap: 12px; margin-top: 22px; }}
                    a {{
                        color: var(--text);
                        text-decoration: none;
                        background: linear-gradient(90deg, rgba(103, 232, 249, 0.18), rgba(167, 139, 250, 0.18));
                        border: 1px solid rgba(255,255,255,0.1);
                        padding: 12px 16px;
                        border-radius: 14px;
                    }}
                    a:hover {{ border-color: rgba(103, 232, 249, 0.45); }}
                    .muted {{ color: var(--muted); }}
                    @media (max-width: 900px) {{
                        .hero, .grid, .stats {{ grid-template-columns: 1fr; }}
                    }}
                </style>
            </head>
            <body>
                <main class="wrap">
                    <div class="hero">
                        <section class="panel">
                            <div class="badge"><span class="dot"></span> Controllo in tempo reale</div>
                            <h1 class="title">Stato del sito</h1>
                            <p class="subtitle">
                                Dashboard visiva per verificare rapidamente se GameMatch è online,
                                quali tabelle sono state create e quando è stato eseguito l'ultimo controllo.
                            </p>

                            <div class="stats">
                                <div class="stat">
                                    <div class="label">Stato</div>
                                    <div class="value">{active_status}</div>
                                </div>
                                <div class="stat">
                                    <div class="label">Tabelle DB</div>
                                    <div class="value">{table_count}</div>
                                </div>
                                <div class="stat">
                                    <div class="label">Ultima verifica</div>
                                    <div class="value" style="font-size: 1rem; line-height: 1.45;">{last_check}</div>
                                </div>
                            </div>

                            <div class="section">
                                <div class="muted">Tabelle presenti nel database</div>
                                <div>
                                    {''.join(f'<span class="table-chip">{name}</span>' for name in table_names) if table_names else '<span class="muted">Nessuna tabella trovata</span>'}
                                </div>
                            </div>
                        </section>

                        <aside class="panel" style="display:grid; place-items:center; text-align:center;">
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

                    <section class="grid" style="margin-top: 20px;">
                        <article class="mini">
                            <h2>API</h2>
                            <p>Endpoint di salute, esempi e documentazione già disponibili.</p>
                        </article>
                        <article class="mini">
                            <h2>Database</h2>
                            <p>Modello relazionale con users, games, teams, matches e team_memberships.</p>
                        </article>
                        <article class="mini">
                            <h2>Build</h2>
                            <p>FastAPI, Pydantic e SQLAlchemy pronti per lo sviluppo.</p>
                        </article>
                        <article class="mini">
                            <h2>Deploy</h2>
                            <p>Struttura compatibile con VPS e ambienti cloud standard.</p>
                        </article>
                    </section>

                    <div class="links">
                        <a href="/health/json">Controllo tecnico</a>
                        <a href="/tables">Vedi tabelle complete</a>
                        <a href="/docs">Apri Swagger UI</a>
                        <a href="/">Torna alla home</a>
                    </div>
                </main>
            </body>
        </html>
        """
        return HTMLResponse(content=html)


@app.get("/health/json")
def health_json() -> dict[str, str]:
        return {"status": "ok"}


@app.get("/status", response_class=HTMLResponse)
def status() -> HTMLResponse:
        table_names = inspect(engine).get_table_names()
        table_count = len(table_names)
        active_status = "Operativo"
        last_check = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        html = f"""
        <!doctype html>
        <html lang="it">
            <head>
                <meta charset="utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <title>GameMatch - Stato del sito</title>
                <style>
                    :root {{
                        color-scheme: dark;
                        --bg: #07111f;
                        --card: rgba(12, 21, 40, 0.92);
                        --card-2: rgba(20, 31, 58, 0.95);
                        --text: #edf2ff;
                        --muted: #9fb0d0;
                        --green: #4ade80;
                        --cyan: #67e8f9;
                        --violet: #a78bfa;
                        --amber: #fbbf24;
                    }}
                    * {{ box-sizing: border-box; }}
                    body {{
                        margin: 0;
                        min-height: 100vh;
                        font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
                        color: var(--text);
                        background:
                            radial-gradient(circle at 20% 20%, rgba(103, 232, 249, 0.18), transparent 25%),
                            radial-gradient(circle at 80% 0%, rgba(167, 139, 250, 0.18), transparent 30%),
                            linear-gradient(180deg, #07111f 0%, #050810 100%);
                        padding: 32px;
                    }}
                    .wrap {{ max-width: 1100px; margin: 0 auto; }}
                    .hero {{
                        display: grid;
                        grid-template-columns: 1.4fr 0.9fr;
                        gap: 20px;
                        align-items: stretch;
                    }}
                    .panel {{
                        background: var(--card);
                        border: 1px solid rgba(255,255,255,0.08);
                        border-radius: 28px;
                        padding: 28px;
                        box-shadow: 0 24px 80px rgba(0,0,0,0.35);
                        backdrop-filter: blur(18px);
                    }}
                    .title {{ margin: 0 0 12px; font-size: clamp(2.2rem, 4vw, 4.2rem); line-height: 1; }}
                    .subtitle {{ margin: 0; color: var(--muted); font-size: 1.05rem; line-height: 1.7; }}
                    .badge {{
                        display: inline-flex;
                        align-items: center;
                        gap: 10px;
                        padding: 10px 14px;
                        border-radius: 999px;
                        background: rgba(74, 222, 128, 0.12);
                        color: var(--green);
                        margin-bottom: 18px;
                        border: 1px solid rgba(74, 222, 128, 0.22);
                        font-size: 0.95rem;
                    }}
                    .dot {{
                        width: 10px;
                        height: 10px;
                        border-radius: 50%;
                        background: var(--green);
                        box-shadow: 0 0 0 6px rgba(74, 222, 128, 0.18);
                    }}
                    .status-ring {{
                        width: 220px;
                        height: 220px;
                        border-radius: 50%;
                        margin: 0 auto;
                        display: grid;
                        place-items: center;
                        background:
                            radial-gradient(circle at center, rgba(7, 17, 31, 0.95) 0 58%, transparent 59%),
                            conic-gradient(from 220deg, var(--green), var(--cyan), var(--violet), var(--green));
                        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.06);
                    }}
                    .status-core {{
                        width: 165px;
                        height: 165px;
                        border-radius: 50%;
                        display: grid;
                        place-items: center;
                        text-align: center;
                        background: linear-gradient(180deg, rgba(20,31,58,0.98), rgba(10,18,35,0.98));
                        border: 1px solid rgba(255,255,255,0.08);
                    }}
                    .status-core strong {{ display: block; font-size: 1.25rem; margin-bottom: 4px; }}
                    .status-core span {{ color: var(--muted); font-size: 0.92rem; }}
                    .stats {{
                        display: grid;
                        grid-template-columns: repeat(3, minmax(0, 1fr));
                        gap: 16px;
                        margin-top: 20px;
                    }}
                    .stat {{
                        background: var(--card-2);
                        border: 1px solid rgba(255,255,255,0.06);
                        border-radius: 18px;
                        padding: 18px;
                    }}
                    .stat .label {{ color: var(--muted); font-size: 0.88rem; }}
                    .stat .value {{ font-size: 1.4rem; margin-top: 10px; }}
                    .section {{ margin-top: 22px; }}
                    .grid {{
                        display: grid;
                        grid-template-columns: repeat(4, minmax(0, 1fr));
                        gap: 16px;
                        margin-top: 20px;
                    }}
                    .mini {{
                        background: var(--card-2);
                        border: 1px solid rgba(255,255,255,0.06);
                        border-radius: 18px;
                        padding: 18px;
                    }}
                    .mini h2 {{ margin: 0 0 8px; font-size: 1rem; }}
                    .mini p {{ margin: 0; color: var(--muted); line-height: 1.55; }}
                    .table-chip {{
                        display: inline-flex;
                        margin: 8px 8px 0 0;
                        padding: 8px 12px;
                        border-radius: 999px;
                        background: rgba(103, 232, 249, 0.12);
                        color: var(--cyan);
                        border: 1px solid rgba(103, 232, 249, 0.18);
                    }}
                    .links {{ display: flex; flex-wrap: wrap; gap: 12px; margin-top: 22px; }}
                    a {{
                        color: var(--text);
                        text-decoration: none;
                        background: linear-gradient(90deg, rgba(103, 232, 249, 0.18), rgba(167, 139, 250, 0.18));
                        border: 1px solid rgba(255,255,255,0.1);
                        padding: 12px 16px;
                        border-radius: 14px;
                    }}
                    a:hover {{ border-color: rgba(103, 232, 249, 0.45); }}
                    .muted {{ color: var(--muted); }}
                    @media (max-width: 900px) {{
                        .hero, .grid, .stats {{ grid-template-columns: 1fr; }}
                    }}
                </style>
            </head>
            <body>
                <main class="wrap">
                    <div class="hero">
                        <section class="panel">
                            <div class="badge"><span class="dot"></span> Controllo in tempo reale</div>
                            <h1 class="title">Stato del sito</h1>
                            <p class="subtitle">
                                Dashboard visiva per verificare rapidamente se GameMatch è online,
                                quali tabelle sono state create e quando è stato eseguito l'ultimo controllo.
                            </p>

                            <div class="stats">
                                <div class="stat">
                                    <div class="label">Stato</div>
                                    <div class="value">{active_status}</div>
                                </div>
                                <div class="stat">
                                    <div class="label">Tabelle DB</div>
                                    <div class="value">{table_count}</div>
                                </div>
                                <div class="stat">
                                    <div class="label">Ultima verifica</div>
                                    <div class="value" style="font-size: 1rem; line-height: 1.45;">{last_check}</div>
                                </div>
                            </div>

                            <div class="section">
                                <div class="muted">Tabelle presenti nel database</div>
                                <div>
                                    {''.join(f'<span class="table-chip">{name}</span>' for name in table_names) if table_names else '<span class="muted">Nessuna tabella trovata</span>'}
                                </div>
                            </div>
                        </section>

                        <aside class="panel" style="display:grid; place-items:center; text-align:center;">
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

                    <section class="grid" style="margin-top: 20px;">
                        <article class="mini">
                            <h2>API</h2>
                            <p>Endpoint di salute, esempi e documentazione già disponibili.</p>
                        </article>
                        <article class="mini">
                            <h2>Database</h2>
                            <p>Modello relazionale con users, games, teams, matches e team_memberships.</p>
                        </article>
                        <article class="mini">
                            <h2>Build</h2>
                            <p>FastAPI, Pydantic e SQLAlchemy pronti per lo sviluppo.</p>
                        </article>
                        <article class="mini">
                            <h2>Deploy</h2>
                            <p>Struttura compatibile con VPS e ambienti cloud standard.</p>
                        </article>
                    </section>

                    <div class="links">
                        <a href="/health">Controllo tecnico</a>
                        <a href="/tables">Vedi tabelle complete</a>
                        <a href="/docs">Apri Swagger UI</a>
                        <a href="/">Torna alla home</a>
                    </div>
                </main>
            </body>
        </html>
        """
        return HTMLResponse(content=html)


@app.get("/tables")
def tables() -> dict[str, list[dict[str, object]]]:
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    tables_info: list[dict[str, object]] = []

    for table_name in table_names:
        columns = [
            {
                "name": column["name"],
                "type": str(column["type"]),
                "nullable": column["nullable"],
                "primary_key": column["primary_key"],
            }
            for column in inspector.get_columns(table_name)
        ]
        tables_info.append({"table": table_name, "columns": columns})

    return {"database": table_names, "tables": tables_info}


@app.get("/examples")
def examples() -> dict[str, object]:
    return {
        "user": UserRead(id=1, username="proGamer", email="pro@email.com"),
        "team": TeamRead(id=10, name="NightRaiders", creator_id=1, members=[]),
        "match": MatchRead(
            id=100,
            scheduled_at=datetime.fromisoformat("2026-06-01T18:00:00"),
            game_id=2,
            team1_id=10,
            team2_id=11,
            game=GameRead(id=2, name="Valorant", genre="FPS"),
            team1=TeamRead(id=10, name="NightRaiders", creator_id=1, members=[]),
            team2=TeamRead(id=11, name="SkyHunters", creator_id=3, members=[]),
        ),
    }