from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String


db = SQLAlchemy()
class Movie(db.Model):
    __tablename__ = 'new_movies2'
    電影名      = Column(db.String(255), primary_key=True)
    海報        = Column(String(255))
    鏈接        = Column(String(255))
    類型        = Column(String(255))
    片長        = Column(String(255))
    制片國家    = Column(String(255))
    語言        = Column(String(255))
    上映日期    = Column(String(255))
    導演        = Column(String(255))
    編劇        = Column(String(255))
    別名        = Column(String(255))
    IMDb編號    = Column(String(255))
