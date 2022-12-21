from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import translators as ts
import translators.server as tss

tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-gem-en")
model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-gem-en")

# bad model
#tokenizer = AutoTokenizer.from_pretrained("google/bert2bert_L-24_wmt_de_en", pad_token="<pad>", eos_token="</s>", bos_token="<s>")
#model = AutoModelForSeq2SeqLM.from_pretrained("google/bert2bert_L-24_wmt_de_en")


def hel_translate(sentence):
    #tokens = tokenizer.encode(sentence, return_tensors="pt")
    #outputs = model.generate(tokens)
    #decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return tss.google(sentence, 'de', 'en')#decoded