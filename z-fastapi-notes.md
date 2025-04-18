# fastapi-py-practice

# Python 3.10

- Formas de ejecución - por consola
  uvicorn NOMBRE_FICHERO:app --reload

  app es el nombre de la instancia de FastAPI
  --reload reinicia el servidor si detecta cambios (solo para desarrollo)

- agregando un en el punto de entrada con if **name** == "**main**"
  uvicorn.run("project_01:app", host="127.0.0.1", port=8000, reload=True)

- Librerias iniciales
  pip install fastapi uvicorn pip-chill
