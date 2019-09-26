log_filename = input('Введите название log файла')
with open(log_filename) as file:
    array = [row.strip() for row in file]

#with open('FG - Copy.log') as file:
#    array = [row.strip() for row in file]
    
      

users = []

        
for n in array:
    '''res=n
    text = res[0]
    print(text[text.find('.tscrm.com'):(text.find('.tscrm.com')+10)])'''
        #print(n)
        
    mystring = n
    keyword = 'unauthuser="'
    before_keyword, keyword, after_keyword = mystring.partition(keyword)
    mystring2 = after_keyword
    #print(mystring2)
    keyword2 = '" unauthusersource'
    before_keyword2, keyword2, after_keyword2 = mystring2.partition(keyword2)
    #print(before_keyword2)
    if before_keyword2 not in users and len(before_keyword2) > 2:
        users.append(before_keyword2)

print(users)

f = open('/mnt/c/Users/Y.Kazabekov/projects/Network_utilities/users.txt', 'w')
for item in users:
    f.write("%s\n" % item)  
f.close()

input('Нажмите любую клавишу для завершения программы программы')