from inner_kernel.Tokenizer import Tokenizer

sentences = ["&#1054;A B C"]
tokenizer = Tokenizer()
tokenizer.set_stemming(True)
tokenizer.set_stopping(True)
tokenizer.set_num_del(False)

for sentence in sentences:
    tokens = sentence.split(" ")
    for token in tokens:
       t = tokenizer.tokenize(token)
       if t != "":
           print(t)
    print("\n")
    print(tokenizer.tokenize(token))

