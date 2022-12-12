from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-gem-en")

model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-gem-en")


def hel_translate(sentence):
    tokens = tokenizer.encode(sentence, return_tensors="pt")
    outputs = model.generate(tokens)
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return decoded