
class Teacher:
    id: int
    type: str
    name: str
    surname: str
    grade: str
    sphere: str
    description: str
    sort: int
    show: bool
    def __init__(self, id, type, name, surname, grade, sphere, description, sort, show):
        self.id = id
        self.type = type
        self.name = name
        self.surname = surname
        self.grade = grade
        self.sphere = sphere
        self.description = description
        self.sort = sort
        self.show = show