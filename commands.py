from Index import *

notify2.init("PyPapersDB")

load_json(gJSONfilename)
# gPapers = []

# for i in range(len(gPapers)):
	# gPapers[i]['tags'] = []

# index_dir('/home/rian/Documents/Research Papers/TCS/')
# remove_nonexistent_files()
# index_with_semantic_scholar('/home/rian/Documents/Research Papers/Algorithms/')
# reparse_files()
remove_dupes()
# query_semantic_scholar('budgeted maximum coverage problem')
# query_google_scholar('budgeted maximum coverage problem')
# remove_unindexed_files()

save_json(gJSONfilename)

# print(gPapers)