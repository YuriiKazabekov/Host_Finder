import difflib



d = difflib.Differ()

file1 = "file_1.txt"
file2 = "file_2.txt"
text1_lines = open(file1).readlines()
text2_lines = open(file2).readlines()

diff = d.compare(text1_lines, text2_lines)
'''
for i in diff:
    print(i)
'''   
print('\n'.join(diff))

#print(list(d.compare(text1_lines, text2_lines)))















