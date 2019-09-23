#file1 = "fdb_10.0.1.250.txt"


ACSW_fdb = ['10.0.1.250_fdb.txt', '10.0.1.251_fdb.txt', '10.0.1.252_fdb.txt', '10.0.2.250_fdb.txt', '10.0.2.251_fdb.txt', '10.0.2.252_fdb.txt',  '10.0.3.250_fdb.txt', 
			'10.0.3.251_fdb.txt',   '10.0.3.252_fdb.txt', '10.0.3.253_fdb.txt', '10.0.4.250_fdb.txt', '10.0.4.251_fdb.txt', '10.0.4.252_fdb.txt',
			'10.0.5.250_fdb.txt', '10.0.5.251_fdb.txt', '10.0.5.252_fdb.txt', '10.0.5.253_fdb.txt','10.0.6.250_fdb.txt', '10.0.6.251_fdb.txt', '10.0.6.253_fdb.txt']



for file in ACSW_fdb:
    with open(file) as file:
        array = [row.strip() for row in file]
        new_array = []
      
    for i in array:
        if 'Forward' in i:
            new_array.append(i)
        else:
            pass
            
    final_array = []        
    for i in new_array:
        if 'T1' not in i :
            #i = ' '.join(i.split()) #Оставляет только один пробел
            final_array.append(i)
            f = open('/mnt/c/Users/Y.Kazabekov/projects/Network_utilities/parsed_fdb/{}'.format(file), 'w')
            for item in final_array:
                f.write("%s\n" % item)  
            f.close()
        
#for n in final_array:
#   print(n)
 
#print(final_array)