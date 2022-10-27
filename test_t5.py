from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("castorini/monot5-base-msmarco-10k")

model = AutoModelForSeq2SeqLM.from_pretrained("castorini/monot5-base-msmarco-10k")


input_ids = tokenizer("What is my name? summarize: studies have shown that owning a dog is good for you", return_tensors="pt").input_ids  # Batch size 1
outputs = model.generate(input_ids)
print(tokenizer.decode(outputs[0], skip_special_tokens=True, max_new_tokens=1))