from .BARTTokenClassification.run_segbot_bart import run_segbot_bart
from .BERTTokenClassification.run_bert import run_segbot_bert_cased, run_segbot_bert_uncased
import warnings

def run_segbot(sent, granularity_level="default", model="bart", conjunctions=["and", "but", "however"], device='cuda'):
    warnings.filterwarnings('ignore')
    print(f"----------- EDU Segmentation with Segbot with {model} model at granularity level: {granularity_level}----------")

    segbot_model = run_segbot_bart
    if model == "bert_uncased":
        segbot_model = run_segbot_bert_uncased
    elif model == "bert_cased":
        segbot_model = run_segbot_bert_cased

    output = segbot_model(sent, device)
    results = []
    if granularity_level == "conjunction_words":
        for segment in output:
            index_str = segment[0].split(",")
            index_begin = index_str[0]            
            index_end = index_str[1]            
            word_str = segment[1]
            word_str = word_str.strip()
            if word_str.startswith(tuple(conjunctions)):
                splitted = word_str.split()
                first_word = splitted[0]
                remaining_words = " ".join(splitted[1:])
                results.append([f'{index_begin}, {int(index_begin)+1}', first_word])
                results.append([f'{int(index_begin)+2}, {index_end}', remaining_words])
            elif word_str.endswith(tuple(conjunctions)):
                splitted = word_str.split()
                remaining_words = " ".join(splitted[:-1])
                last_word = splitted[-1]
                results.append([f'{index_begin}, {int(index_begin)+1}', remaining_words])
                results.append([f'{int(index_begin)+2}, {index_end}', last_word])
            else:
                results.append(segment)
        return results
    else:
        return output