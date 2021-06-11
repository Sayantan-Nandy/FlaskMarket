from sqlalchemy.sql.elements import Null
from market import db,login_manager
from market import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)           #relationship type element of db. Connecting to another db


    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f"{self.budget}$"

    def password_check(self,password_attempt):
        return bcrypt.check_password_hash(self.password_hash,password_attempt)

    def can_purchase(self,item):
        return self.budget>=item.price

    def can_sell(self,item):
        print("Self id",self.id)
        print("item owner",item.owner)
        return self.id==item.owner



    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, text_password):
        self.password_hash = bcrypt.generate_password_hash(text_password).decode('utf8')

    

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30),nullable = False)
    price = db.Column(db.Integer(),nullable = False)
    barcode = db.Column(db.String(length=30),nullable = False, unique = True)
    desc = db.Column(db.String(length=1000),nullable = False, unique = True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))                   #Foreign Key

    def __repr__(self):
        return f'Item{self.name}'                           #Return Item name instead of Object number



    def buy(self,user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()
    
    def sell(self,user):
        self.owner = None
        user.budget += self.price
        db.session.commit()
    """

        Do the below in different python kernel
        
        Steps to create db
            from market import db
            db.create_all()

        Steps to add to SQLAlchemy database:
            from market import db
            from market.models import Item
            item1 = Item(name="IPhone",price=500,barcode="61271419829",desc="Description for IPhone")
            db.session.add(item1)
            db.session.commit()


        To create Relationship between tables:
            i1 = Item.query.filter_by(name="IPhone").first()
            i1.owner = User.query.filter_by(username="Harish M").first().id
            i1.owner
            i1.owned_user


    """