from data.__all_models import User, Event
from data.db_session import global_init, create_session
# 1234abcd qwerty123 bulba3445 skam123 checkYourLinux 2020qQ11!?


global_init('db/data.sqlite')
db_sess = create_session()

user = User()
user.name = 'Vladislav'
user.surname = 'Tarakanov'
user.email = 'vtarakanov2017@litsey2.ru'
user.set_password('2020qQ11!?')
db_sess.add(user)
db_sess.commit()
db_sess.close()
