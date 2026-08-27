#!/usr/bin/env python3
"""
Envía por correo la fábula de Esopo correspondiente al día.

Cómo elige la fábula del día:
- Usa un contador guardado en el archivo 'estado.json' del propio
  repositorio. Cada vez que se ejecuta, envía la siguiente fábula de
  la lista (en el orden del PDF original) y avanza el contador.
- Cuando llega a la fábula 293, vuelve a empezar por la 1.

Variables de entorno necesarias (se configuran como "Secrets" en GitHub):
- GMAIL_USER: la dirección de Gmail desde la que se envía el correo
- GMAIL_APP_PASSWORD: la contraseña de aplicación de Gmail (no la contraseña normal)
- DEST_EMAIL: la dirección de correo donde quieres recibir la fábula
"""

import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

DATA_FILE = "fabulas_completas.json"
STATE_FILE = "estado.json"


def cargar_fabulas():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def cargar_estado():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"indice": 0}


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
    fabulas = cargar_fabulas()
    estado = cargar_estado()

    indice = estado["indice"] % len(fabulas)
    fabula = fabulas[indice]

    enviar_correo(fabula)

    estado["indice"] = (indice + 1) % len(fabulas)
    guardar_estado(estado)


if __name__ == "__main__":
    main()
