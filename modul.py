# Возможно, функция нигде не вызывается
def answers(counter, sheet, rand):
    print('ON modul.answer')
    print(counter, "- ", sheet.row_values(rand)[0])
    i = 1
    while sheet.row_values(rand)[i] != 'stop':
        print(i, ". ", sheet.row_values(rand)[i])
        i += 1

# Возможно, функция нигде не вызывается
def question(db):
    print('ON modul.question')
    i = 0
    names = db.sheet_names()
    while i != 11:
        print(i + 1, "Тест", names[i])
        i += 1
    case = input()
    sheet = db.sheet_by_index(int(case) - 1)
    return sheet

# Возможно, функция нигде не вызывается
def pointer (count):
    print('ON modul.pointer')
    print(float(count) / 20 * 100)
    if int(float(count) / 20 * 100) > 80:
        print("Ты сдашь, красава!")
    else:
        print("Штош...")

# Возможно, функция нигде не вызывается
def ans_user ():
    print('ON modul.ans_user')
    inpt = input()
    while inpt.isdigit() == False:
        print("Попробуй ещё раз, нужно писать цифры без пробела.")
        inpt = input()
    ls = list(inpt)
    ls = sorted(set(map(int, ls)))
    return ls

# Возможно, функция нигде не вызывается
def true_ans (sheet, rand):
    print('ON modul.true_ans')
    i = 0
    ans = []
    while sheet.row_values(rand)[18 + i] != 'stop':
        ans.append(int(sheet.row_values(rand)[18 + i]))
        i += 1
    sorted(ans)
    return ans

# Возможно, функция нигде не вызывается
def check_answer(ls, sheet, rand, count):
    print('ON modul.check_answer')
    if ls == true_ans(sheet, rand):
        print("Красава", '\n')
        count += 1
    else:
        print("Давай ещё разок! ")
        if ans_user() == true_ans(sheet, rand):
            print("Красава", '\n')
            count += 1
        else:
            print("Плохо, учи!", '\n')
    return count