from data.__all_models import User, Event
from data.db_session import global_init, create_session
# 1234abcd qwerty123 bulba3445 skam123 checkYourLinux


global_init('db/data.sqlite')
db_sess = create_session()

user = db_sess.query(User).get(5)
print(user.events)
event1 = db_sess.query(Event).get(1)
event2 = db_sess.query(Event).get(2)
user.events.append(event1)

db_sess.commit()
print(user.events)
db_sess = create_session()
user = db_sess.query(User).get(5)
event1 = db_sess.query(Event).get(1)
user.events.remove(event1)
db_sess.commit()
print(user.events)
db_sess.close()
