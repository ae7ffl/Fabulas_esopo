# Fábula diaria de Esopo por correo

Este repositorio envía automáticamente, todos los días a las 7:00 (hora de España),
un correo con una fábula de Esopo, preguntas para reflexionar, su significado
y un ejemplo histórico o de actualidad donde se puede aplicar.

Las 293 fábulas van en orden (el mismo del libro original) y, al llegar a la
última, se vuelve a empezar por la primera.

## Cómo ponerlo en marcha (una sola vez)

### 1. Crear una contraseña de aplicación de Gmail

Esto permite que el script envíe correos desde tu cuenta de Gmail sin usar tu
contraseña normal.

1. Ve a https://myaccount.google.com/security
2. Activa la verificación en dos pasos si no la tienes activada (es obligatorio
   para poder crear contraseñas de aplicación).
3. Ve a https://myaccount.google.com/apppasswords
4. Crea una nueva contraseña de aplicación.
5. Copia la contraseña de 16 caracteres que te da Google. La necesitarás en el
   paso 3.

### 2. Subir este repositorio a GitHub

1. Crea una cuenta gratuita en https://github.com si no tienes una.
2. Crea un repositorio nuevo (puede ser privado).
3. Sube todos los archivos de esta carpeta a ese repositorio. Formas de hacerlo:
   - Arrastrando los archivos desde la web de GitHub ("Add file" → "Upload files"), o
   - Con git desde una terminal:
     ```
     git init
     git add .
     git commit -m "Primer commit"
     git branch -M main
     git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
     git push -u origin main
     ```

### 3. Configurar los "Secrets" (datos privados) en GitHub

En tu repositorio en GitHub, ve a:
**Settings → Secrets and variables → Actions → New repository secret**

Crea estos tres secrets:

| Nombre               | Valor                                                        |
|-----------------------|--------------------------------------------------------------|
| `GMAIL_USER`          | Tu dirección de Gmail (ej: tunombre@gmail.com)               |
| `GMAIL_APP_PASSWORD`  | La contraseña de aplicación de 16 caracteres del paso 1      |
| `DEST_EMAIL`          | La dirección donde quieres recibir la fábula (puede ser la misma que GMAIL_USER) |

### 4. Activar el envío automático

El archivo `.github/workflows/fabula-diaria.yml` ya está configurado para
ejecutarse todos los días a las 7:00 (hora de España, ajustando automáticamente
el cambio de horario de verano/invierno). En cuanto subas el repositorio a
GitHub con este archivo, GitHub Actions se activa solo — no hay que hacer nada más.

### 5. (Opcional) Probarlo ahora mismo

Para comprobar que todo funciona sin esperar a mañana:
1. Ve a la pestaña **Actions** de tu repositorio en GitHub.
2. Selecciona el workflow "Enviar fábula diaria".
3. Pulsa **Run workflow** (esto ignora la comprobación de la hora y prueba el envío).

   Nota: si usas "Run workflow" tal cual, como no serán las 7:00 en Madrid, el
   paso de envío se saltará. Si quieres forzar un envío de prueba real,
   dime y te preparo una versión del workflow sin esa comprobación horaria
   para probarlo una vez.

## Archivos de este repositorio

- `fabulas_completas.json`: las 293 fábulas con su texto, preguntas, significado
  y ejemplo histórico. Fuentes: fábulas (Elejandria) y el resto (Claude).
- `send_fabula.py`: el script que arma y envía el correo.
- `estado.json`: guarda qué fábula toca mañana (se actualiza solo cada día).
- `.github/workflows/fabula-diaria.yml`: la configuración de GitHub Actions
  que ejecuta el script automáticamente cada mañana.

## Coste

Este proceso no usa ninguna API de pago ni consume tokens de Claude: todo el
contenido ya está generado y guardado en `fabulas_completas.json`. GitHub
Actions es gratuito para este uso (muy por debajo del límite gratuito mensual
para repositorios privados). El archivo de las Fábulas de Esopo es un pdf descargado 
de elejandria.com
