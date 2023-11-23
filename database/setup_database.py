# setup_database.py

from sqlalchemy import create_engine, and_, func
from sqlalchemy.orm import sessionmaker
from YogaDAO import Base, Classes

engine = create_engine('mysql://root:root@localhost/Yogastudio', echo=True)

# Create tables
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Populate the 'classes' table
'''
session.add_all([
    Classes(title="Aerial FUNdamentals", instructor=" Liz", fee=1100),
    Classes(title="Aerial Intermediate", instructor=" Liz", fee=1100),
    Classes(title="Aerial Advanced", instructor=" Orla", fee=1100),
    Classes(title="Pilates", instructor=" Orla", fee=12000)
])'''


# Retrieve the Pilates class from the database
pilates_class = session.query(Classes).filter_by(title="Pilates").first()

# Check if the Pilates class exists before updating
if pilates_class:
    # Update the fee for Pilates
    pilates_class.fee = 1200  # Corrected fee 

    
# Identify classes with duplicated titles, instructors, and fees
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
        session.delete(class_to_delete)

# Commit the changes to the database
    session.commit()
