import datetime
from sqlalchemy import (Index, Column, Integer, String, Sequence, DateTime, create_engine)
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker, relationship, backref


Base = declarative_base()

def initialize(dbname):
    engine = create_engine('sqlite:///' + dbname, echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def write_to_db(session, new_entries):
    dict = {entry.link : entry for entry in new_entries}
    for entry in session.query(JobType.link).filter(JobType.link.in_(dict.keys())).all():
        session.merge(dict.pop(entry.link))
    session.add_all(dict.values())
    session.commit()


def read_db(session):
    for instance in session.query(JobType).order_by(JobType.id):
        print(instance)


class JobType(Base):
    __tablename__ = "jobs"

    id = Column(Integer, Sequence("id_seq"), unique=True)
    created_at = Column(DateTime, default=datetime.datetime.now, index=True)
    last_updated_at = Column(DateTime, onupdate=datetime.datetime)
    title = Column(String)
    company = Column(String)
    salary = Column(String)
    description = Column(String)
    link = Column(String, primary_key=True)

    def __repr__(self):
        return f"<Job(title={self.title}, last_updated_at={self.last_updated_at})"
