import logging
import os
import pandas as pd
from haystack import Document
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import RAGenerator, DensePassageRetriever
# Or alternatively use the Pipeline class
from haystack.pipelines import GenerativeQAPipeline
from haystack.utils import print_answers

logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
logging.getLogger("haystack").setLevel(logging.INFO)

# Create dataframe with columns "title" and "text"
doc_dir = "datasets/CovidQA/"
df = pd.read_csv(f"{doc_dir}/splitted_covid_dump.csv", sep="\t", header=None, names=['title','text'])
# Minimal cleaning
df.fillna(value="", inplace=True)

print(df.head())


# Use data to initialize Document objects
titles = list(df['title'].values)[:10]
texts = list(df['text'].values)[:10]
documents = []
for title, text in zip(titles, texts):
    documents.append(Document(content=text, meta={"name": title or ""}))

# Initialize FAISS document store.
# Set `return_embedding` to `True`, so generator doesn't have to perform re-embedding
document_store = None

if os.path.exists('faiss_document_store.db'):
	print("loading index...")
	document_store = FAISSDocumentStore(faiss_index_path="my_faiss", sql_url= "sqlite:///faiss_document_store.db", index="document")
else:
	document_store = FAISSDocumentStore(faiss_index_factory_str="Flat", return_embedding=True, sql_url= "sqlite:///faiss_document_store.db")	


# Initialize DPR Retriever to encode documents, encode question and query documents
retriever = DensePassageRetriever(
    document_store=document_store,
    query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
    passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
    use_gpu=True,
    embed_title=True,
)

# Initialize RAG Generator
generator = RAGenerator(
    model_name_or_path="facebook/rag-token-nq",
    use_gpu=True,
    top_k=1,
    max_length=200,
    min_length=2,
    embed_title=True,
    num_beams=2,
)


# Delete existing documents in documents store
#document_store.delete_documents()

# Write documents to document store
document_store.write_documents(documents)

# Add documents embeddings to index
document_store.update_embeddings(retriever=retriever)
#document_store.update_embeddings(retriever=retriever,update_existing_embeddings=True)

document_store.save('my_faiss')

pipe = GenerativeQAPipeline(generator=generator, retriever=retriever)

counter = 0
out = open("./datasets/CovidQA/test/facebook.responses", "w")
with open('./datasets/CovidQA/test/test.source') as f:
	for q in f.readlines():
		print(counter,":",q)
		res = pipe.run(query=q, params={"Generator": {"top_k": 1}, "Retriever": {"top_k": 5}})
		if (len(res['answers'])>0):
			answer = res['answers'][0].answer
			print("\t", answer)
			out.write(answer)
		out.write("\n")
		counter += 1
		if (counter > 3):
			break
out.close()



