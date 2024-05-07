from sqlite3 import connect


class MessagesTable:
    def __init__(self):
        self.connection = connect("database/offline.db")
        self.cur = self.connection.cursor()

    def get_all(self, **kwargs):
        filters = ""
        if kwargs:
            filters = " WHERE " + " ".join([f'{op} = {kwargs[op]}' for op in kwargs])
        line = "SELECT * FROM messages" + filters + ";"

        self.cur.execute(line)

        messages = []
        for msg in self.cur.fetchall():
            messages.append({
                "id": msg[0],
                "sent_by": msg[1],
                "sent_to": msg[2],
                "content": msg[3],
                "sent": msg[4],
                "delivered": msg[5],
                "read": msg[6],
            })

        return messages

    def add_messages(self, messages):
        self.cur.execute("SELECT id FROM messages;")
        in_db = [m[0] for m in self.cur.fetchall()]
        for msg in messages:
            if msg.id in in_db:
                args = [str(msg.sent_by), str(msg.sent_to),
                        msg.content, msg.sent, msg.delivered, msg.read, msg.id]
                self.cur.execute("""UPDATE messages SET 
                                sent_by = ?, sent_to = ?, content = ?, sent = ?, delivered = ?, read = ?
                                WHERE id = ?;""", args)
            else:
                args = [str(msg.id), str(msg.sent_by), str(msg.sent_to),
                        msg.content, msg.sent, msg.delivered, msg.read]
                self.cur.execute("""INSERT INTO messages(id, sent_by, sent_to, content, sent, delivered, read)
                                VALUES (?, ?, ?, ?, ?, ?, ?);""", args)
        self.connection.commit()

    def replace(self, old_id, msg):
        args = [msg["id"], msg["sent_by"], msg["sent_to"],
                msg["content"], msg["sent"], msg["delivered"], msg["read"], old_id]
        self.cur.execute("""UPDATE messages SET 
                        id= ?, sent_by = ?, sent_to = ?, content = ?, sent = ?, delivered = ?, read = ?
                        WHERE id = ?;""", args)


db_messages = MessagesTable()
