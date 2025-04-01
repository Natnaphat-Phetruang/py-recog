def findsum (numbers,want):
    seenum =  set()
    
    for number in numbers:
         required = want - number
    if required in seenum:
            return True
    seenum.add(number)
    
    return False


comeinput = input("กรอกชุดตัวเลข: ")
numbers = list(map(int, input.split()))
want=int(input("ต้องการ: "))
result = findsum(numbers,want)
print (result)