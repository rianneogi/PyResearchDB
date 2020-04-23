from Index import *

notify2.init("PyPapersDB")
# index_file('1.pdf')
# index_file('2.pdf')
# index_file('3.pdf')
# index_file('4.pdf')
load_json()

# for i in range(1000000000):
# 	if i%100000==0:
# 		print(i)

# index_dir('/home/rian/Documents/Research Papers/Algorithms/')
reparse_files()
# remove_dupes()

save_json()

print(gPapers)