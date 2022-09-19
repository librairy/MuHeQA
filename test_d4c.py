import test_logger
import application.summary.db.d4c as db_d4c

d4c = db_d4c.D4C()


query = "What position does Carlos Gomez play?"
keyword = "Carlos Gomez"

resources = d4c.find_texts(keyword,5)
