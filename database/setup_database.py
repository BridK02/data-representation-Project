# setup_database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from YogaDAO import Base, Classes

engine = create_engine('mysql://root:root@localhost/Yogastudio', echo=True)

# Create tables
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Populate the 'classes' table
session.add_all([
    Classes(title='Restorative', instructor='Jane', fee=950),
    # Add more classes as needed
])

# Commit the changes
session.commit()
