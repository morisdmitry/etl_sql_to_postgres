from dataclasses import dataclass



@dataclass(frozen=True)
class FilmWork:
    __slots__= (
        'id',
        'title',
        'description',
        'creation_date',
        'certificate',
        'file_path',
        'rating',
        'type',
        'created_at',
        'updated_at'
    )
    id: int
    title: str
    description: str
    creation_date: str
    certificate: str
    file_path: str
    rating: float
    type: str
    created_at: str
    updated_at: str

    def __post_init__(self):
        conditions = [
            isinstance(self.id, str),
            isinstance(self.title, str),
            isinstance(self.description, str),
            isinstance(self.creation_date, str),
            isinstance(self.certificate, str),
            isinstance(self.file_path, str),
            isinstance(self.rating, float),
            isinstance(self.type, str),
            isinstance(self.created_at, str),
            isinstance(self.updated_at, str),
        ]

        if not all(conditions):
            raise ValueError


@dataclass(frozen=True)
class Person:
    __slots__= (
        'id',
        'full_name',
        'birth_date',
        'created_at',
        'updated_at',
    )
    id: str
    full_name: str
    birth_date: str
    created_at: str
    updated_at: str

    def __post_init__(self):
        conditions = [
            isinstance(self.id, str),
            isinstance(self.full_name, str),
            isinstance(self.birth_date, str),
            isinstance(self.created_at, str),
            isinstance(self.updated_at, str),
        ]

        if not all(conditions):
            raise ValueError

@dataclass(frozen=True)
class Genre:
    __slots__= (
        'id',
        'name',
        'description',
        'created_at',
        'updated_at',
    )
    id: str
    name: str
    description: str
    created_at: str
    updated_at: str

    def __post_init__(self):
        conditions = [
            isinstance(self.id, str),
            isinstance(self.name, str),
            isinstance(self.description, str),
            isinstance(self.created_at, str),
            isinstance(self.updated_at, str),
        ]
        if not all(conditions):
            raise ValueError

@dataclass(frozen=True)
class PersonFilmWork:
    __slots__= (
        'id',
        'film_work_id',
        'person_id',
        'role',
        'created_at',
    )
    id: str
    film_work_id: str
    person_id: str
    role: str
    created_at: str


    def __post_init__(self):
        conditions = [
            isinstance(self.id, str),
            isinstance(self.film_work_id, str),
            isinstance(self.person_id, str),
            isinstance(self.role, str),
            isinstance(self.created_at, str)
        ]

        if not all(conditions):
            raise ValueError
@dataclass(frozen=True)
class GenreFilmWork:
    __slots__= (
        'id',
        'film_work_id',
        'genre_id',
        'created_at',
    )
    id: str
    film_work_id: str
    genre_id: str
    created_at: str

    def __post_init__(self):
        conditions = [
            isinstance(self.id, str),
            isinstance(self.film_work_id, str),
            isinstance(self.genre_id, str),
            isinstance(self.created_at, str)
        ]
        if not all(conditions):
            raise ValueError
