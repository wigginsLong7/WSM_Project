from Tokenizer import Tokenizer

<<<<<<< HEAD
sentences = ["&#1054; &#1068;"]

=======
sentences = ["&#1054;&#1068;"]
>>>>>>> origin/master

tokenizer = Tokenizer()
tokenizer.set_stemming(True)
tokenizer.set_stopping(True)
tokenizer.set_num_del(False)

for sentence in sentences:
    tokens = sentence.split(" ")
    for token in tokens:
<<<<<<< HEAD
       t = tokenizer.tokenize(token)
       if t != "":
           print(t)
    print("\n")
=======
        print(tokenizer.tokenize(token))
>>>>>>> origin/master
