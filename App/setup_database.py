# setup_database.py

from sqlalchemy import create_engine, and_, func
from sqlalchemy.orm import sessionmaker
from database import Base, Classes

engine = create_engine('mysql://root:root@localhost/Yogastudio', echo=True)

# Create tables
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Populate the 'classes' table

session.add_all([
    Classes(title="Yin", instructor="Emma", fee=1000),
    Classes(title="Restorative", instructor=" Jane", fee=950),
    Classes(title="Aerial FUNdamentals", instructor=" Liz", fee=1100),
    Classes(title="Aerial Intermediate", instructor=" Liz", fee=1100),
    Classes(title="Aerial Advanced", instructor=" Orla", fee=1100),
    Classes(title="Pilates", instructor=" Orla", fee=1200)
])


    
'''# Identify classes with duplicated titles, instructors, and fees
duplicated_classes = session.query(Classes.title, Classes.instructor, Classes.fee, func.count().label('count')).group_by(Classes.title, Classes.instructor, Classes.fee).having(func.count() > 1).all()

# Iterate through duplicated classes and keep only the first occurrence
for title, instructor, fee, count in duplicated_classes:
    # Keep the first occurrence and delete the rest
    classes_to_delete = session.query(Classes).filter(and_(
        Classes.title == title,
        Classes.instructor == instructor,
        Classes.fee == fee
    )).order_by(Classes.id.desc()).offset(1).all()

    for class_to_delete in classes_to_delete:
        session.delete(class_to_delete)'''

# Commit the changes to the database
session.commit()
