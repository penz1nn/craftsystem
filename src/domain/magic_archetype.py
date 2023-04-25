class Archetype:
    name: str

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, o):
        return self.name == o.name

    def __hash__(self):
        return hash(self.name)
