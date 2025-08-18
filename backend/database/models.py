from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Text, DateTime, Enum
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
import enum

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    username = Column(String(30), unique=True, nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    is_verified = Column(Boolean, default=False)

    posts = relationship("Post", back_populates="owner")



class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, index=True)
    file_url = Column(String(255), nullable=False)

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)

    post = relationship("Post", back_populates="media_items")



class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)

    content = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    owner = relationship("User", back_populates="posts")

    reply_to_post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
    replies = relationship(
        "Post",
        backref=backref("parent", remote_side=[id]),
        foreign_keys=[reply_to_post_id]
        )

    is_repost = Column(Boolean, default=False)

    repost_of_post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
    repost = relationship(
        "Post",
        remote_side=[id],
        foreign_keys=[repost_of_post_id],
        post_update=True
    )

    media_items = relationship("Media", back_populates="post", cascade="all, delete")

class MessageStatus(str, enum.Enum):
    sent = "sent"
    delivered = "delivered"
    read = "read"
    failed = "failed"

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=True)  # Text message body

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    status = Column(Enum(MessageStatus), default=MessageStatus.sent, nullable=False)

    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    sender = relationship("User", foreign_keys=[sender_id], backref="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], backref="received_messages")

    # Optional: allow attaching media to a message
    media_id = Column(Integer, ForeignKey("media.id", ondelete="SET NULL"), nullable=True)
    media = relationship("Media", backref="messages")

