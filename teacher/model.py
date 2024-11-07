class Teacher:
    id: int
    name: str
    grade: str
    sphere: str
    description: str
    show: bool
    nickname: str

    def __init__(self, id, name, grade, sphere, description, show, nickname):
        self.id = id
        self.name = name
        self.grade = grade
        self.sphere = sphere
        self.description = description
        self.show = show
        self.nickname = nickname
