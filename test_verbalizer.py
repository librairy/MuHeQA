import test_logger
import application.summary.verbalizer as vb


print("initializing...")
verbalizer = vb.Verbalizer()

query = "What position does Carlos Gomez play?"
keyword = "Carlos Gomez"

print("verbalizing text...")
result = verbalizer.get_text(query,keyword,1,True,True,False)
print("Result: ", result)
