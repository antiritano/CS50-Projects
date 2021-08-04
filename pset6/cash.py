from cs50 import get_float

while True:
    try:
        change = get_float("How much change is owed?")
        if change > 0:
            break
    except:
        print("", end="")
            
coins = 0
changeR = change * 100

while changeR >= 25:
    changeR = changeR - 25
    coins = coins + 1
while changeR >= 10:
    changeR = changeR - 10
    coins = coins + 1
while changeR >= 5:
    changeR = changeR - 5
    coins = coins + 1
while changeR >= 1:
    changeR = changeR - 1
    coins = coins + 1
    
print(coins)