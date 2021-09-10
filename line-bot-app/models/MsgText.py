from .. import db

# 模型( model )定義
class MsgText(db.Model):
    __tablename__ = 'msg_text'
    pid = db.Column(db.Integer, primary_key=True)

    message = db.Column(
        db.String(255), nullable=False)

    insert_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(
        db.DateTime, onupdate=datetime.now, default=datetime.now)

    def __init__(self, message):
        self.message = message