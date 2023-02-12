from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import translators as ts
import translators.server as tss
from transformers import FSMTForConditionalGeneration, FSMTTokenizer

model_name = "Helsinki-NLP/opus-mt-gem-en"
modeL_name = "mbart-large-50-English_German_Translation"
model_facebook = "wmt19-de-en"



tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


#tokenizer = FSMTTokenizer.from_pretrained(model_facebook)
#model = FSMTForConditionalGeneration.from_pretrained(model_facebook)

# bad model
#tokenizer = AutoTokenizer.from_pretrained("google/bert2bert_L-24_wmt_de_en", pad_token="<pad>", eos_token="</s>", bos_token="<s>")
#model = AutoModelForSeq2SeqLM.from_pretrained("google/bert2bert_L-24_wmt_de_en")


def hel_translate(sentence):
    tokens = tokenizer.encode(sentence, return_tensors="pt")
    outputs = model.generate(tokens)
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return decoded #tss.google(sentence, 'de', 'en')#decoded