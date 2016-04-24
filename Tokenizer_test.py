from Tokenizer import Tokenizer

sentences = ["The odd even invariant for graphs.",
             "What's your name?",
             "I AM A STUDENT. NICE TO MEET YOU!"
             ]

tokenizer = Tokenizer()
tokenizer.set_stemming(True)
tokenizer.set_stopping(True)

for sentence in sentences:
    tokens = sentence.split(" ")
    for token in tokens:
        print(tokenizer.tokenize(token))

    print("\n")