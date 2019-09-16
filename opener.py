ip_list_name = "ACSW_IP.txt"


f=open(ip_list_name,"r+")
ip_list = f.read().split('\n')   
f.close() 
print(ip_list)
