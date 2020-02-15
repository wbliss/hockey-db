from app import db


class Player(db.Model):
    __table_args__ = {'schema':'hockey'}
    id = db.Column(db.Integer, primary_key=True, index=True)
    slug = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(120))
    position = db.Column(db.String(2))
    shoots = db.Column(db.String(120))
    height = db.Column(db.String(4))
    weight = db.Column(db.Integer)
    dob = db.Column(db.Date)
    is_hof = db.Column(db.Boolean)
    #nationality = db.Column(db.String(50))

    def __init__(self, slug, name, position, shoots, height, weight, dob, is_hof):
        
        self.slug = slug
        self.name = name
        self.position = position
        self.shoots = shoots
        self.height = height
        self.weight = weight
        self.dob = dob
        self.is_hof = is_hof
        #self.nationality = nationality
