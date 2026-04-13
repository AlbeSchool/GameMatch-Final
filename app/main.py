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
def examples() -> HTMLResponse:
    html = """
    <!doctype html>
    <html lang="it">
        <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <title>GameMatch – Esempi</title>
            <style>
                :root {
                    color-scheme: dark;
                    --bg: #0b1020;
                    --panel: rgba(18, 26, 51, 0.92);
                    --panel-2: rgba(24, 35, 68, 0.95);
                    --text: #eef2ff;
                    --muted: #9fb0d0;
                    --cyan: #67e8f9;
                    --violet: #a78bfa;
                    --green: #4ade80;
                    --yellow: #fbbf24;
                    --red: #f87171;
                    --border: rgba(255,255,255,0.08);
                }
                * { box-sizing: border-box; }
                body {
                    margin: 0;
                    font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
                    background:
                        radial-gradient(circle at 10% 10%, rgba(103,232,249,0.18), transparent 35%),
                        radial-gradient(circle at 90% 5%, rgba(167,139,250,0.18), transparent 30%),
                        linear-gradient(180deg, #0b1020 0%, #060912 100%);
                    color: var(--text);
                    min-height: 100vh;
                    padding: 40px 24px;
                }
                .wrap { max-width: 980px; margin: 0 auto; }
                /* ── header ── */
                .header { margin-bottom: 36px; }
                .badge {
                    display: inline-flex;
                    align-items: center;
                    gap: 8px;
                    padding: 8px 14px;
                    border-radius: 999px;
                    background: rgba(103,232,249,0.12);
                    color: var(--cyan);
                    border: 1px solid rgba(103,232,249,0.22);
                    font-size: 0.88rem;
                    margin-bottom: 14px;
                }
                h1 {
                    margin: 0 0 8px;
                    font-size: clamp(2rem, 4vw, 3rem);
                    line-height: 1.1;
                }
                .subtitle { margin: 0; color: var(--muted); font-size: 1rem; line-height: 1.65; }
                /* ── grid layout ── */
                .grid-top {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 20px;
                    margin-bottom: 20px;
                }
                /* ── cards ── */
                .card {
                    background: var(--panel);
                    border: 1px solid var(--border);
                    border-radius: 22px;
                    padding: 26px;
                    box-shadow: 0 18px 60px rgba(0,0,0,0.32);
                    backdrop-filter: blur(16px);
                }
                .card-header {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    margin-bottom: 20px;
                    padding-bottom: 14px;
                    border-bottom: 1px solid var(--border);
                }
                .icon {
                    width: 44px; height: 44px;
                    border-radius: 14px;
                    display: grid;
                    place-items: center;
                    font-size: 1.4rem;
                    flex-shrink: 0;
                }
                .icon-user  { background: rgba(103,232,249,0.14); }
                .icon-team  { background: rgba(167,139,250,0.14); }
                .icon-match { background: rgba(251,191,36,0.14);  }
                .icon-game  { background: rgba(74,222,128,0.14);  }
                .card-title { margin: 0; font-size: 1.15rem; font-weight: 600; }
                .card-id    { margin: 2px 0 0; font-size: 0.82rem; color: var(--muted); }
                /* ── fields ── */
                .field { display: flex; flex-direction: column; gap: 4px; margin-bottom: 14px; }
                .field:last-child { margin-bottom: 0; }
                .field-label {
                    font-size: 0.78rem;
                    text-transform: uppercase;
                    letter-spacing: 0.06em;
                    color: var(--muted);
                }
                .field-value {
                    font-size: 1rem;
                    color: var(--text);
                    word-break: break-all;
                }
                .pill {
                    display: inline-flex;
                    padding: 4px 12px;
                    border-radius: 999px;
                    font-size: 0.88rem;
                    font-weight: 500;
                }
                .pill-cyan   { background: rgba(103,232,249,0.14); color: var(--cyan);   border: 1px solid rgba(103,232,249,0.22); }
                .pill-violet { background: rgba(167,139,250,0.14); color: var(--violet); border: 1px solid rgba(167,139,250,0.22); }
                .pill-green  { background: rgba(74,222,128,0.14);  color: var(--green);  border: 1px solid rgba(74,222,128,0.22);  }
                .pill-yellow { background: rgba(251,191,36,0.14);  color: var(--yellow); border: 1px solid rgba(251,191,36,0.22);  }
                /* ── match card ── */
                .match-card { width: 100%; }
                .match-body {
                    display: grid;
                    grid-template-columns: 1fr auto 1fr;
                    gap: 20px;
                    align-items: center;
                    margin-bottom: 22px;
                }
                .team-side { text-align: center; }
                .team-avatar {
                    width: 64px; height: 64px;
                    border-radius: 50%;
                    display: grid;
                    place-items: center;
                    font-size: 1.6rem;
                    margin: 0 auto 10px;
                }
                .team-avatar-1 { background: rgba(103,232,249,0.16); border: 2px solid rgba(103,232,249,0.3); }
                .team-avatar-2 { background: rgba(167,139,250,0.16); border: 2px solid rgba(167,139,250,0.3); }
                .team-name { font-size: 1.05rem; font-weight: 600; margin-bottom: 4px; }
                .team-meta { font-size: 0.82rem; color: var(--muted); }
                .vs {
                    font-size: 1.6rem;
                    font-weight: 700;
                    color: var(--yellow);
                    text-shadow: 0 0 18px rgba(251,191,36,0.45);
                }
                .match-meta {
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 14px;
                    padding-top: 18px;
                    border-top: 1px solid var(--border);
                }
                .meta-item { display: flex; flex-direction: column; gap: 4px; }
                .meta-label { font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted); }
                .meta-value { font-size: 0.95rem; }
                /* ── links ── */
                .links { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 32px; }
                a {
                    color: var(--text);
                    text-decoration: none;
                    background: linear-gradient(90deg, rgba(103,232,249,0.14), rgba(167,139,250,0.14));
                    border: 1px solid rgba(255,255,255,0.1);
                    padding: 12px 18px;
                    border-radius: 14px;
                    font-size: 0.95rem;
                    transition: border-color 0.2s;
                }
                a:hover { border-color: rgba(103,232,249,0.5); }
                @media (max-width: 640px) {
                    .grid-top { grid-template-columns: 1fr; }
                    .match-body { grid-template-columns: 1fr; }
                    .vs { text-align: center; }
                    .match-meta { grid-template-columns: 1fr 1fr; }
                }
            </style>
        </head>
        <body>
            <main class="wrap">
                <header class="header">
                    <div class="badge">&#127918; Esempi schemi Pydantic</div>
                    <h1>Dati di esempio</h1>
                    <p class="subtitle">Visualizzazione grafica degli oggetti restituiti dall'API: utente, team e match.</p>
                </header>

                <!-- top row: user + team -->
                <div class="grid-top">

                    <!-- User card -->
                    <div class="card">
                        <div class="card-header">
                            <div class="icon icon-user">&#128100;</div>
                            <div>
                                <p class="card-title">Utente</p>
                                <p class="card-id">UserRead</p>
                            </div>
                        </div>
                        <div class="field">
                            <span class="field-label">Username</span>
                            <span class="field-value"><strong>proGamer</strong></span>
                        </div>
                        <div class="field">
                            <span class="field-label">Email</span>
                            <span class="field-value">pro@email.com</span>
                        </div>
                        <div class="field">
                            <span class="field-label">ID</span>
                            <span class="field-value"><span class="pill pill-cyan">#1</span></span>
                        </div>
                    </div>

                    <!-- Team card -->
                    <div class="card">
                        <div class="card-header">
                            <div class="icon icon-team">&#128101;</div>
                            <div>
                                <p class="card-title">Team</p>
                                <p class="card-id">TeamRead</p>
                            </div>
                        </div>
                        <div class="field">
                            <span class="field-label">Nome</span>
                            <span class="field-value"><strong>NightRaiders</strong></span>
                        </div>
                        <div class="field">
                            <span class="field-label">Creator ID</span>
                            <span class="field-value"><span class="pill pill-violet">#1</span></span>
                        </div>
                        <div class="field">
                            <span class="field-label">Membri</span>
                            <span class="field-value"><span class="pill pill-cyan">0 membri</span></span>
                        </div>
                        <div class="field">
                            <span class="field-label">ID Team</span>
                            <span class="field-value"><span class="pill pill-violet">#10</span></span>
                        </div>
                    </div>
                </div>

                <!-- Match card (full width) -->
                <div class="card match-card">
                    <div class="card-header">
                        <div class="icon icon-match">&#9876;&#65039;</div>
                        <div>
                            <p class="card-title">Match</p>
                            <p class="card-id">MatchRead &nbsp;·&nbsp; ID #100</p>
                        </div>
                        <span class="pill pill-green" style="margin-left:auto;">&#127918; Valorant &nbsp;&bull;&nbsp; FPS</span>
                    </div>

                    <div class="match-body">
                        <div class="team-side">
                            <div class="team-avatar team-avatar-1">&#128101;</div>
                            <div class="team-name">NightRaiders</div>
                            <div class="team-meta">Team #10 &nbsp;&bull;&nbsp; Creator #1</div>
                        </div>
                        <div class="vs">VS</div>
                        <div class="team-side">
                            <div class="team-avatar team-avatar-2">&#128101;</div>
                            <div class="team-name">SkyHunters</div>
                            <div class="team-meta">Team #11 &nbsp;&bull;&nbsp; Creator #3</div>
                        </div>
                    </div>

                    <div class="match-meta">
                        <div class="meta-item">
                            <span class="meta-label">&#128197; Data</span>
                            <span class="meta-value">01 giugno 2026</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">&#128336; Orario</span>
                            <span class="meta-value">18:00</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">&#127918; Gioco</span>
                            <span class="meta-value"><span class="pill pill-green">Valorant</span></span>
                        </div>
                    </div>
                </div>

                <nav class="links">
                    <a href="/">&#8592; Home</a>
                    <a href="/docs">Swagger UI</a>
                    <a href="/health">Stato del sito</a>
                </nav>
            </main>
        </body>
    </html>
    """
    return HTMLResponse(content=html)