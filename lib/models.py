from sqlalchemy import Column, Integer, String, DateTime, func, create_engine
from sqlalchemy.orm import validates, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine('sqlite:///authors.db')
session = sessionmaker(bind=engine)()

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer(), primary_key=True)
    name= Column(String(), unique=True, nullable=False)
    phone_number = Column(String())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())


    @validates("phone_number")
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10:
            raise ValueError("phone number too short")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer(), primary_key=True)
    title = Column(String(), nullable=False)
    content = Column(String())
    category = Column(String())
    summary = Column(String())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    @validates("content")
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("content too short")
        return content

    @validates("summary")
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("summary too long")
        return summary


    @validates("category")
    def validate_category(self, key, category):
        if category !="Fiction" and category != "Non-fiction":
            raise ValueError("not valid category")
        return category

    @validates("title")
    def validate_title(self, key, title):
        bait = ["Won't Believe", "Secret", "Top [number]", "Guess"]
        found = False
        for s in bait:
            if s in title:
                found = True
        if not found:
            raise ValueError("not valid title")
        return title

Base.metadata.create_all(engine)
