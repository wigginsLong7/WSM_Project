from inner_kernel.Tokenizer import Tokenizer

<<<<<<< HEAD:inner_kernel/Tokenizer_test.py
sentences = ["&#1054; &#1068; A"]
=======
sentences = ["&#1054;A B C"]
>>>>>>> c684cfd5d1eb5286c2d02e84c7c90e89a927ab5b:Tokenizer_test.py


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

