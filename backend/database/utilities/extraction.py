from tqdm import tqdm
from . import pipeline 
import os
from pathlib import Path


dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir = Path(dir_path).parent
MODEL_PATH = os.path.join(parent_dir, 'utilities/ai_model/ggml-model-f16.gguf')

data_extraction_prompt_template = """
    {context}
    
    [INST] 
    Summarize the provided context in english then answer the question based only your summary.
    Format your answers in valid JSON objects.
    
    Question: {question} [/INST]"""

# set of 15 question th paper is to be evaluated on
questionnaire = [
    "Who are the authors, title, publisher of this article; when and where was it published?",
    "In what country and what study sites was the study describe in this document carried out?",
    "Considering the sites found earlier, was the use of insecticide-based control reported?",
    "During what period was the study carried out?",
    "What Disease was the study focused on?",
    "What mosquitoes or vector species was reported in each study sites?",
    "What sampling methods was employed, and how many individuals were sampled in each study sites?",
    "Was the daily survival rate of identified species in each location reported?",
    "Was the fecundity information and gonotrophic cycle reported for identified species?",
    "Describe the communities of each location, if reported in the study in terms of housing, cooking, common occupation, average bedtime, average wake time",
    "Describe the environment in each location if reported in the study.",
    "What infection details of each species was reported in the study?",
    "What biting information were reported in the study for each specie?",
    "What information about the resting preference of each species was reported?",
    "What larvae information was reported in the study for each species on each site?"
]


embedding_fn = pipeline.CustomLlamaCppEmbeddings(
    model_path=MODEL_PATH, n_ctx=4096, n_gpu_layers=10,
)

def run_exp(pdfPaths):
    global embedding_fn, data_extraction_prompt_template, questionnaire
    for pdf_path in tqdm(pdfPaths,position=0, leave=True):
        try:
            pipeline.data_auto_extract(pdf_path,
                            embedding_fn, 
                            data_extraction_prompt_template, questionnaire)
        except Exception as e:
            print(e)
            continue
    return True