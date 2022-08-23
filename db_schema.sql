
CREATE SCHEMA IF NOT EXISTS content;


-- создаем таблицы
CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    birth_date DATE,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);
CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    description TEXT,
    created_at timestamp with time zone,
    updated_at timestamp with time zone

);
CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    creation_date DATE,
    certificate TEXT,
    file_path TEXT,
    rating NUMERIC(2,1),
    type VARCHAR(30) NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);
CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL REFERENCES content.film_work(id) ON DELETE CASCADE,
    person_id uuid NOT NULL REFERENCES content.person(id) ON DELETE CASCADE,
    role VARCHAR(30) NOT NULL,
    created_at timestamp with time zone
);
CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL REFERENCES content.film_work(id) ON DELETE CASCADE,
    genre_id uuid NOT NULL REFERENCES content.genre(id) ON DELETE CASCADE,
    created_at timestamp with time zone
);

-- создаем индексы
CREATE INDEX film_work_creation_date_idx ON content.film_work(creation_date);
CREATE UNIQUE INDEX film_work_person ON content.person_film_work (film_work_id, person_id);
CREATE UNIQUE INDEX film_work_genre ON content.genre_film_work (film_work_id, genre_id);
