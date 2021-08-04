import cs50

while True:
    str = cs50.get_string('Text: ')
    index = 0
    i = 0
    alphabets = 0
    digits = 0
    special = 0
    words = 1
    sentences = 0
    if (str):
        for i in range(len(str)):
            if (str[i].isalpha()):
                alphabets += 1
            elif (str[i].isnumeric()):
                digits += 1
            elif (str[i] == ' ' and str[i + 1]):
                words += 1
            elif (str[i] == '?' or str[i] == '!' or str[i] == '.'):
                sentences += 1
            else:
                special += 1
        
        L = float(alphabets / words * 100)
        S = float(sentences / words * 100)
        index = round((float)(0.0588 * L - 0.296 * S - 15.8))
        if (index >= 16):
            print('Grade 16+')
        elif (index < 1):
            print('Before Grade 1')
        else:
            print('Grade ', index)

        break