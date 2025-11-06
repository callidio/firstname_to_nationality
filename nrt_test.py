from firstname_to_nationality import FirstnameToNationality

predictor = FirstnameToNationality()

names = open("test_data/test.txt", 'r', encoding='utf8').read().splitlines()

results = predictor(names, top_n=5, use_dict=False)
with open("test_data/test.expected", "w", encoding="utf8") as fout:
    for r in results:
        preds = r[-1]
        preds = ",".join(each[0] for each in preds)
        fout.write(preds + "\n")
