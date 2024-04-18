from langchain.prompts import PromptTemplate
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain.embeddings import LlamaCppEmbeddings
import time, os, datetime, json
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import LlamaCpp
from tqdm import tqdm
from typing import List
from langchain_core.runnables import RunnablePassthrough 
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

from database.schemas import Question
from .pdf_preprocessing import *
# import multiprocessing
from joblib import Parallel, delayed


dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir = Path(dir_path).parent
MODEL_PATH = os.path.join(parent_dir, 'utilities/ai_model/ggml-model-f16.gguf')



class CustomLlamaCppEmbeddings(LlamaCppEmbeddings):
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents using the Llama model.
        Args:
            texts: The list of texts to embed.
        Returns:
            List of embeddings, one for each text.
        """
        # embeddings = [self.client.embed(text) for text in tqdm(texts, position=0, leave=True)]
        print("##### ATTEMPTING EMBEDDING ...")
        embeddings = Parallel(n_jobs=8)(delayed(self.client.embed)(text) for text in tqdm(texts, position=0, leave=True))
        print("##### EMBEDDING COMPLETED ...")
        return [list(map(float, e)) for e in embeddings]


def embed_data(documents, embedding_fn):
    tic = time.process_time()
    vectorstore = Chroma.from_documents(documents=documents, embedding=embedding_fn)
    toc = time.process_time()
    stop = toc - tic
    print(f"Embedding completed in {stop/60} s") 
    return vectorstore, stop


def build_retriever(embedding_fn, file_path, chunk_size=3000, chunk_overlap=30):
    try:
        loader = TextLoader(file_path, encoding = 'UTF-8')
    except Exception as e:
        loader = TextLoader(file_path, encoding = 'latin1')
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, add_start_index=True)
    splits = text_splitter.split_documents(docs)
    # Parallel(n_jobs=4)(delayed(embed_data)([item], embedding_fn, vectorstore) for item in splits)
    vectorstore, ellapsed = embed_data(splits, embedding_fn)
    with open("embedding.log.csv", "a+") as f:
        f.write(f"\n{os.path.getsize(file_path)},{ellapsed}")
    retriever = vectorstore.as_retriever()
    return vectorstore, retriever


def inline_text(file_path):
    res = ""
    _switch = False # switch from writting all on the same line to writting as in file.
    mfile = None
    try:
        mfile = open(file_path,"r", encoding="utf-8")
    except Exception as e:
        mfile = open(file_path,"r", encoding="latin1")
    for line in mfile.readlines():
        # exclude document references section and subsequent sections
        if line.lower().strip().startswith("references") or line.lower().strip().startswith("acknowledgement"):
            break
        nline = line
        # nline = line.replace("-\n", "")
        # nline = nline.replace("\n", " ")
        # nline = nline.replace("| ", "")
        # nline = nline.replace("\'", "")
        # nline = nline.replace("  ", " ")
        # nline = nline.replace("\t", " ")
        if nline.lower().strip().startswith("introduction"):
            nline = "MAIN BODY: \n" + nline
        res += nline
    res = "HEADER: \n" + res 
    return res


def setchain(prompt_template, retriever, llm):
    prompt = PromptTemplate(
        template=prompt_template, 
        input_variables=["question"],
    )
    setup_and_retrieval = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    )
    vchain = setup_and_retrieval | prompt | llm 
    return vchain


def refresh_gramma(grammar_path=None):
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    n_gpu_layers = 10  # Metal set to 1 is enough.
    n_batch = 512  # Should be between 1 and n_ctx, consider the amount of RAM of your Apple Silicon Chip.
    # Make sure the model path is correct for your system!
    # gllm("Describe a Sample study in JSON", grammar=vector_grammar)
    if grammar_path:
        gllm = LlamaCpp(
            model_path=MODEL_PATH,
            n_gpu_layers=n_gpu_layers,
            n_batch=n_batch,
            n_ctx=4096,
            f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
            callback_manager=callback_manager,
            verbose=True,  # Verbose is required to pass to the callback manager
            grammar_path=grammar_path,
            # return_full_text=False, # to not repeat the question, set to False
            # top_k=10, # default=10
            # top_p=0.1, # default=0.9
            # temperature=0.3 # default=0.
        )
        return gllm
    else: 
        gllm = LlamaCpp(
            model_path=MODEL_PATH,
            n_gpu_layers=n_gpu_layers,
            n_batch=n_batch,
            n_ctx=4096,
            f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
            callback_manager=callback_manager,
            verbose=True,  # Verbose is required to pass to the callback manager
            # grammar_path=grammar_path,
            # return_full_text=False, # to not repeat the question, set to False
            # top_k=10, # default=10
            # top_p=0.1, # default=0.9
            # temperature=0 # default=0.
        )
        return gllm
    

def data_auto_extract(pdf_path, embedding_fn, prompt_template, questionnaire:List[Question]):
    Answers = []
    basename = os.path.basename(pdf_path).split(".")[0]
    basename = "_".join(basename.lower().split(" "))
    file_path = os.path.join(Path(pdf_path).parent,f"{basename}_ext/text.txt")
    results_path = os.path.join(Path(Path(pdf_path).parent).parent, "results")
    begin = datetime.datetime.now()
    # 1. clean and embed text
    if not os.path.exists(file_path):
        extract_pdf_text(pdf_path=pdf_path)
    m_text = inline_text(file_path).encode("utf8").decode("utf8")
    try:
        with open(file_path, "w+", encoding='utf-8') as f:
            f.write(m_text)
    except Exception as e:
        with open(file_path, "w+", encoding='latin1') as f:
            f.write(m_text)
    vectorstore, retriever = build_retriever(embedding_fn, file_path, chunk_size=1024, chunk_overlap=10)
    print(f"#### RETRIEVER AND VECTORSTORE INITIALIZED")
    # os.remove(f"{basename}.txt")
    first_stop = datetime.datetime.now()
    max_loop = 3
    # 2. extract informations based on questionnaire
    for question in tqdm(questionnaire, position=0, leave=True):
        res_format_ok = False
        grammar_path=question.anwser_grammar
        gllm = refresh_gramma(grammar_path)
        # llm = refresh_gramma()
        # data_extraction_prompt_template
        chain = setchain(prompt_template, retriever, gllm)
        loop_done = 0
        while not res_format_ok and loop_done < max_loop :
            ans = chain.invoke(question.label)
            ans = ans.replace(",}","}")
            ans = ans.replace("\":\":", "\":\"")
            ans = ans.replace("\".", "\"")
            try:
                ans_check = json.loads(str(ans))
                if not ans_check and loop_done < max_loop:
                    # and questionnaire.index(question) < 9: #10 question
                    res_format_ok=False
                    print(f"###>>> FALSE: ANSWER TO QUESTION SHOULDN'T BE EMPTY.")
                elif loop_done >= max_loop: 
                    res_format_ok=True
                    Answers.append(ans_check)
                    print(f"###>>> TRUE: ANSWER TO QUESTION {questionnaire.index(question) + 1} IS A VALID JSON.")
                elif ans_check:
                    res_format_ok=True
                    Answers.append(ans_check)
                    print(f"###>>> TRUE: ANSWER TO QUESTION {questionnaire.index(question) + 1} IS A VALID JSON.")
            except Exception as e:
                print(f"###>>> FALSE: ANSWER TO QUESTION {questionnaire.index(question) + 1} IS NOT A VALID JSON.")
                res_format_ok=False
            finally:
                loop_done += 1
                continue
    end = datetime.datetime.now()
    vectorstore.delete_collection()
    print(f"####VECTORSTORE CLEANNED")
    with open(os.path.join(results_path, f"{basename}.json"), "w+") as f:
        seconds_in_day = 24 * 60 * 60
        embedding_time = first_stop - begin
        extraction_time = end - first_stop
        minutes_em, seconds_em = divmod(embedding_time.days * seconds_in_day + embedding_time.seconds, 60)
        minutes_ex, seconds_ex = divmod(extraction_time.days * seconds_in_day + extraction_time.seconds, 60)
        Answers.append({"embedding_time": [minutes_em, seconds_em]})
        Answers.append({"extraction_time": [minutes_ex, seconds_ex]})
        Answers.append({"pdf_id": basename})
        json.dump(Answers, f, indent = 4)