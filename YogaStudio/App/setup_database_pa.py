from sqlalchemy import create_engine, and_, func
from sqlalchemy.orm import sessionmaker
from YogaDAO.base import Base
from YogaDAO.models import Classes
from YogaDAO.dbconfigpa import mysql  # Import MySQL configuration for PythonAnywhere
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

try:# Create engine with PythonAnywhere MySQL configuration
    engine = create_engine(
        f"mysql+mysqlconnector://{mysql['user']}:{mysql['password']}@{mysql['host']}/{mysql['database']}",
        echo=True
    )

    
    Classes.__table__.create(engine, checkfirst=True)


    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    # Populate the 'classes' table
    session.add_all([
        Classes(title="Yin", instructor="Emma", fee=10.00, image_filename="Yin.jpg"),
        Classes(title="Restorative", instructor=" Jane", fee=9.50, image_filename="Restorative.jpg"),
        Classes(title="Aerial FUNdamentals", instructor=" Liz", fee=11.00, image_filename="aerialFundamentals.jpg"),
        Classes(title="Aerial Intermediate", instructor=" Liz", fee=11.00, image_filename="aeriallmage.jpg"),
        Classes(title="Aerial Advanced", instructor=" Orla", fee=11.00, image_filename="aeriallmage.jpg"),
        Classes(title="Pilates", instructor=" Orla", fee=12.00, image_filename="pilatesimage.jpg")
    ])

    # Identify classes with duplicated titles, instructors, and fees
    duplicated_classes = session.query(
        Classes.title, Classes.instructor, Classes.fee, func.count().label('count')
    ).group_by(
        Classes.title, Classes.instructor, Classes.fee
    ).having(
        func.count() > 1
    ).all()

    # Iterate through duplicated classes and keep only the correct occurrence
    for title, instructor, fee, count in duplicated_classes:
        # Get all occurrences of the class
        all_occurrences = session.query(Classes).filter(
            and_(
                Classes.title == title,
                Classes.instructor == instructor,
                Classes.fee == fee
            )
        ).order_by(Classes.id.desc()).all()

        # Get the correct occurrence with the correct image link
        correct_occurrence = next(
            (class_occurrence for class_occurrence in all_occurrences if class_occurrence.image_filename != "default_value"),
            None
        )

        # Delete all occurrences except the correct one
        for class_to_delete in all_occurrences:
            if class_to_delete != correct_occurrence:
                session.delete(class_to_delete)

    session.commit()

except Exception as e:
    print(f"Error: {e}")
    raise