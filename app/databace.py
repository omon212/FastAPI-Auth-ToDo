from sqlalchemy import create_engine, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, Session, relationship
from passlib.context import CryptContext

engine = create_engine(f'sqlite:///data.db')
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(16), unique=True)
    password: Mapped[str] = mapped_column(String(128))

    tasks: Mapped[list["Tasks"]] = relationship("Tasks", back_populates="user")


class Tasks(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(128))
    time: Mapped[str] = mapped_column(String(16))
    description: Mapped[str] = mapped_column(String(256))
    status: Mapped[str] = mapped_column(String(16))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    user: Mapped["User"] = relationship("User", back_populates="tasks")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
