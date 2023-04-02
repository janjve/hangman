# prompt gpt for phrases:
# "can you give me a list of 20 words with a short 1 sentence description. The words should be 5 or more characters and prefer nouns. The words should not be too obscure since an average person should be able to guess them from knowing some of the letters. It is for a hangman game"

with open("gpt-output-words.csv") as f:
    for row in f:
        if row.strip():
            word, definition = row.strip().split("-", 1)
            word = word.strip()
            definition = definition.strip()
            orow = f'0,"{word}","{definition}"'
            print(orow)

with open("gpt-output-phrases.csv") as f:
    for row in f:
        if row.strip():
            word, definition = row.strip().split("-", 1)
            word = word.strip()
            definition = definition.strip()
            orow = f'1,"{word}","{definition}"'
            print(orow)
