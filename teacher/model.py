class Teacher:
    id: int
    name: str
    grade: str
    sphere: str
    description: str
    show: bool

    def __init__(self, id, name, grade, sphere, description, show):
        self.id = id
        self.name = name
        self.grade = grade
        self.sphere = sphere
        self.description = description
        self.show = show
