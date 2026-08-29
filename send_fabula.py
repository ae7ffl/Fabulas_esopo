#!/usr/bin/env python3
"""
Envía por correo la fábula de Esopo correspondiente al día.

Cómo elige la fábula del día:
- Usa un contador guardado en 'estado.json'. Cada vez que se envía,
  avanza al siguiente número de la lista (en el orden del PDF original)
  y, al llegar a la 293, vuelve a empezar por la 1.

Protección contra duplicados y retrasos:
- GitHub a veces ejecuta el workflow programado más tarde de lo previsto.
  Por eso, en vez de exigir que sea una hora exacta, el script guarda la
  FECHA (no la hora) del último envío en 'estado.json'. Si hoy ya se envió,
  no vuelve a enviar aunque se ejecute otra vez ese mismo día.

Variables de entorno necesarias (Secrets en GitHub):
- GMAIL_USER, GMAIL_APP_PASSWORD, DEST_EMAIL
"""

import json
import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from zoneinfo import ZoneInfo

DATA_FILE = "fabulas_completas.json"
STATE_FILE = "estado.json"
ZONA_MADRID = ZoneInfo("Europe/Madrid")


def cargar_fabulas():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def cargar_estado():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"indice": 0, "ultima_fecha_enviada": None}


def guardar_estado(estado):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(estado, f, ensure_ascii=False, indent=1)


def construir_html(fabula):
    preguntas_html = "".join(f"<li>{p}</li>" for p in fabula["questions"])
    texto_html = fabula["text"].replace("\n\n", "</p><p>").replace("\n", "<br>")

    historical_block = ""
    if fabula.get("historical") and fabula["historical"] != "n/a":
        historical_block = f"""
        <h3 style="color:#7a5230;">📜 Un ejemplo histórico</h3>
        <p>{fabula['historical']}</p>
        """

    html = f"""
    <html>
    <body style="font-family: Georgia, 'Times New Roman', serif; max-width: 650px; margin: auto; padding: 20px; color: #2c2c2c; background-color: #fdfaf3;">
        <h1 style="color:#8b4513; border-bottom: 2px solid #d8c3a5; padding-bottom: 10px;">
            🦉 Fábula del día: {fabula['title']}
        </h1>
        <p style="font-style: italic; color: #666;">Fábula nº {fabula['num']} de 293 — Esopo</p>

        <p>{texto_html}</p>

        <h3 style="color:#7a5230;">🤔 Preguntas para reflexionar</h3>
        <ul>
            {preguntas_html}
        </ul>

        <h3 style="color:#7a5230;">💡 Significado</h3>
        <p>{fabula['moral']}</p>

        {historical_block}

        <hr style="border: none; border-top: 1px solid #d8c3a5; margin-top: 30px;">
        <p style="font-size: 0.85em; color: #999;">Recibes este correo porque configuraste tu propio envío diario de fábulas de Esopo. 🌅</p>
    </body>
    </html>
    """
    return html


def enviar_correo(fabula):
    gmail_user = os.environ["GMAIL_USER"]
    gmail_password = os.environ["GMAIL_APP_PASSWORD"]
    dest_email = os.environ["DEST_EMAIL"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🦉 Fábula del día: {fabula['title']}"
    msg["From"] = gmail_user
    msg["To"] = dest_email

    html_content = construir_html(fabula)
    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, dest_email, msg.as_string())

    print(f"Correo enviado: fábula #{fabula['num']} - {fabula['title']}")


def main():
    hoy_madrid = datetime.now(ZONA_MADRID).date().isoformat()

    estado = cargar_estado()

    if estado.get("ultima_fecha_enviada") == hoy_madrid:
        print(f"Ya se envió la fábula de hoy ({hoy_madrid}). No se hace nada.")
        return

    fabulas = cargar_fabulas()
    indice = estado["indice"] % len(fabulas)
    fabula = fabulas[indice]

    enviar_correo(fabula)

    estado["indice"] = (indice + 1) % len(fabulas)
    estado["ultima_fecha_enviada"] = hoy_madrid
    guardar_estado(estado)


if __name__ == "__main__":
    main()
