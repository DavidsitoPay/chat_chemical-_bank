El proyecto está hecho en Django (se necesita python 3.x para generar un entorno virtual), esta es una pequeña guía para poder levantar el servidor:

1. Descargar en alguna carpeta
2. Abrir la carpeta con algún terminal (cmd, powershell, gitbash)
3. Comando para crear el entorno virtual: python -m venv env
4. Levantar entorno virtual (depende del terminal que se use):
   a. linux/gitbash: source env/Script/activate
   b. cmd/powershell: env\Scripts\activate
5. Ahora se tienen dos carpetas (/chat_app-main y /env), hay que entrar a /chat_app-main (cd /chat_app-main) e instalar los requerimientos (pip install -r requirement.txt)
6. Ya instalados los requerimientos se realizan las migraciones:
    python manage.py makemigrations
    python manage.py migrate
7. Recomiendo crear superusuario para poder acceder a la parte del admin de la página en Django (ejecutar el siguiente comando y llenar el formulario):
    python manage.py createsuperuser
8. Levantamos el servidor (recomiendo verificar si se tiene algún puerto abierto previamente, sino hay que abrir uno para poder levantar el servidor):
    Comando para levantar en puerto predeterminado (8000): python manage.py runserver
    Comando para levantar en puerto especifico (reemplazar el $puerto por el puerto que se tenga abierto): python manage.py runserver 127.0.0.1:$puerto
9. Abrimos la página y nos logeamos


