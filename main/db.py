from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

engine = create_engine('sqlite:///info.db', echo=True)
Base = declarative_base()


class Settings(Base):
    __tablename__ = 'setting'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    path_img_save = Column(String(255))

    def __repr__(self):
        return "<Settings(name='%s')>" % (self.name)


    def start_db(self) -> bool:
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind = engine)
        session = Session()
        
        add_setting = Settings(name = "path_save_img", path_img_save = f"images")
        self.create_object(new_object = add_setting)

        return True


    def find_object(self, find: str) -> object:
        Session = sessionmaker(bind=engine)  
        session = Session()  

        result = session.query(Settings).filter_by(name = find).first()
        return result               


    def edit_object(self, old: str, new: str) -> object:
        Session = sessionmaker(bind=engine)   
        session = Session() 

        find_old = session.query(Settings).filter_by(name = old).first()
        
        find_old.path_img_save = new 

        session.commit()
        return find_old 


    def create_object(self, new_object: object) -> object:
        Session = sessionmaker(bind=engine)
        session = Session()

        new = session.add(new_object)
        session.commit()
        return new 

db = Settings()

if __name__ == "__main__":
    print("START DB")
    db.start_db()








