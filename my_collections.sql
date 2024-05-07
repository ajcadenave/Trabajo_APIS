CREATE DATABASE my_collections;

\c my_collections;

CREATE TABLE my_movies (
    ID SERIAL PRIMARY KEY,
    autor VARCHAR(100),
    descripcion VARCHAR(255),
    fechaestreno DATE
);

INSERT INTO my_movies (autor, descripcion, fechaestreno) VALUES
('Autor 1', 'Pelicula 1', '2023-01-01'),
('Autor 2', 'Pelicula 2', '2023-02-15'),
('Autor 3', 'Pelicula 3', '2023-03-20');