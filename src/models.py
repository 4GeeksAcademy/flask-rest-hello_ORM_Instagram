from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean,Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship
import enum

db = SQLAlchemy()
class MediaType(enum.Enum):
    image = "image"
    video = "video"

class User(db.Model):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    user_name: Mapped[str] = mapped_column(String(50), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))


    # relation 
    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    comments: Mapped[list["Comment"]]= relationship(back_populates="author")
    followers: Mapped[list["Follower"]] = relationship("Follower", foreign_keys="[Follower.user_to_id]",back_populates="followed")
    following: Mapped[list["follower"]] = relationship("Follower", foreign_keys="[Follower.user_from_id]", back_populates="follower")
    # serialize
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class Follower(db.Model):
    __tablename__ = "follower"

    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)

    follower: Mapped["User"] = relationship("User", foreign_keys=[user_from_id], back_populates="following")
    followed: Mapped["User"] = relationship("User", foreign_keys=[user_to_id], back_populates="followers")
   


    class Post(db.Model):
        __tablename__ = "post"
        id: Mapped[int] = mapped_column(primary_key=True)
        user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
        user: Mapped["User"] = relationship(back_populates="posts")
        media: Mapped[list["Media"]] = relationship(back_populates="post")
        comments: Mapped[list["comment"]] = relationship(back_populates="post")

    class Media(db.Model):
        __tablename__ = "media"
        id: Mapped[int] = mapped_column(primary_key=True)
        type: Mapped[MediaType] = mapped_column(Enum(MediaType))
        url: Mapped[str] = mapped_column(String, nullable=False)
        post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    author: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")

from eralchemy2 import render_er

try:
    render_er(db.Model, 'diagram.png')  # db.Model si usas Flask-SQLAlchemy
    print("¡Diagrama generado exitosamente!")
except Exception as e:
    print("Error al generar el diagrama:", e)



