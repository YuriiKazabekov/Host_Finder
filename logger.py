with open('FG - Copy.log') as file:
    array = [row.strip() for row in file]
    
      

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
    if before_keyword2 not in users:
        users.append(before_keyword2)

print(users)




        
        

