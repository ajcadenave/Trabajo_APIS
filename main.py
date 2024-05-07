from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import psycopg2
from datetime import date

app = FastAPI()

db_params = {
    'dbname': 'my_collections',
    'user': 'postgres',
    'password': 1234,
    'host': 'localhost',
    'port': '5432',
}

conn = psycopg2.connect(**db_params)

class Pelicula(BaseModel):
    autor: str
    descripcion: str
    fechaestreno: date


@app.get('/pelicula')
def consultar_pelicula():

    temporal_list = []

    with conn.cursor() as cursor:
        
        try:
            get_data_query = '''
            SELECT* FROM my_movies
            '''
            
            cursor.execute(get_data_query)

            rows = cursor.fetchall()

            for row in rows:
                print(row)
                temporal_list.append(row)
        except:
            print("Error con la consulta GET")

    return {"message": temporal_list}

@app.get("/pelicula/{pelicula_id}")
def consultar_pelicula(pelicula_id: int):

    temporal_list = []

    try:
        # Asumiendo que 'conn' es una conexión activa al inicio de tu app
        with conn.cursor() as cursor:
            get_data_query = '''
            SELECT * FROM my_movies WHERE id = %s;
            '''
            cursor.execute(get_data_query, (pelicula_id,))

            rows = cursor.fetchall()

            for row in rows:
                print(row)
                temporal_list.append(row)

    except Exception as e:
        print("Error con la consulta GET: ", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return {"message": temporal_list}

@app.post('/pelicula')
def crear_pelicula(pelicula:Pelicula):

    with conn.cursor() as cursor:
        
        try:
            insert_data_query = '''
            INSERT INTO my_movies (autor, descripcion, fechaestreno) VALUES (%s, %s, %s) RETURNING id;
            '''
            cursor.execute(insert_data_query, (pelicula.autor, pelicula.descripcion, pelicula.fechaestreno))
            conn.commit()

        except Exception as e:
            print(e)
            print("Error con la consulta POST")

    return {"message": "Creado correctamente"}

@app.put("/pelicula/{pelicula_id}", response_model=Pelicula, status_code=status.HTTP_200_OK)
def actualizar_pelicula(pelicula_id: int, pelicula: Pelicula):
    cursor = conn.cursor()

    update_query = '''
    UPDATE my_movies SET autor=%s, descripcion=%s, fechaestreno=%s WHERE id=%s;
    '''
    cursor.execute(update_query, (pelicula.autor, pelicula.descripcion, pelicula.fechaestreno, pelicula_id))
    conn.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Pelicula no encontrada")

    return pelicula

@app.delete("/pelicula/{pelicula_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_pelicula(pelicula_id: int):
    with conn.cursor() as cursor:
        delete_query = '''
        DELETE FROM my_movies WHERE id = %s;
        '''
        cursor.execute(delete_query, (pelicula_id,))
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Pelicula no encontrada")