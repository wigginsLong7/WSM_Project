from Tokenizer import Tokenizer

sentences = ["&#1054;&#1068;"]

tokenizer = Tokenizer()
tokenizer.set_stemming(True)
tokenizer.set_stopping(True)

for sentence in sentences:
    tokens = sentence.split(" ")
    for token in tokens:
        print(tokenizer.tokenize(token))