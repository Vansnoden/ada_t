from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.document_loaders import TextLoader
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain.embeddings import LlamaCppEmbeddings
### full method to build a retriever from text file
import time, os, datetime, json
import chromadb
from langchain.embeddings import LlamaCppEmbeddings
# from langchain.vectorstores import Chroma
from chromadb import Documents, EmbeddingFunction, Embeddings
from chromadb.errors import InvalidDimensionException
from langchain.callbacks.manager import CallbackManager
from langchain.chains import RetrievalQA
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from llama_cpp.llama import Llama, LlamaGrammar
from tqdm import tqdm
from typing import Iterable, List, Optional
import langchain
from langchain_core.runnables import RunnablePassthrough 
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser 
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain.prompts import HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage

