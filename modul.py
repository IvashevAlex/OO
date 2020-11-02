def answers(counter, sheet, rand):
    print(counter, "- ", sheet.row_values(rand)[0])
    i = 1
    while sheet.row_values(rand)[i] != 'stop':
        print(i, ". ", sheet.row_values(rand)[i])
        i += 1

def question(db):
    i = 0
    names = db.sheet_names()
    while i != 11:
        print(i + 1, "Тест", names[i])
        i += 1
    case = input()
    sheet = db.sheet_by_index(int(case) - 1)
    return sheet

def pointer (count):
    print(float(count) / 20 * 100)
    if int(float(count) / 20 * 100) > 80:
        print("Ты сдашь, красава!")
    else:
        print("Штош...")

def ans_user ():
    inpt = input()
    while inpt.isdigit() == False:
        print("Попробуй ещё раз, нужно писать цифры без пробела.")
        inpt = input()
    ls = list(inpt)
    ls = sorted(set(map(int, ls)))
    return ls

def true_ans (sheet, rand):
    i = 0
    ans = []
    while sheet.row_values(rand)[18 + i] != 'stop':
        ans.append(int(sheet.row_values(rand)[18 + i]))
        i += 1
    sorted(ans)
    return ans

def check_answer(ls, sheet, rand, count):
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