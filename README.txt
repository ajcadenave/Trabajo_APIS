Creacion del postgres en docker:
docker run --name database -e POSTGRES_PASSWORD=1234 -p 5432:5432 -d postgres

Se mueve el archivo sql con la tabla a crear en el postgres:
docker cp my_collections.sql database:/my_collections.sql

Se ejecuta el script en postgres:
docker exec -it database psql -U postgres -f /my_collections.sql

Se valida la creacion correcta de la tabla my_movies:
docker exec -it database psql -U postgres -d my_collections -c "SELECT* FROM my_movies"

Se sube el API:
uvicorn main:app --reload