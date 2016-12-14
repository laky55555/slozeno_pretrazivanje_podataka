# uvod_u_slozeno_pretrazivanje_podataka
University class about data mining

1. Project on topic Nonnegative matrix factorization for interactive topic modeling and document clustering
	http://www.cc.gatech.edu/~hpark/papers/nmf_book_chapter.pdf
	In directory there are following scripts:
	spider.py 			-> Web scraper for getting content from jutarnji.hr.
	cleaning_jutarnjihr.sh		-> Bash script for cleaning and editing text acquired with spider.py.
	make_loadable.sh 		-> Script for comparing words from jutarnji.hr and dictionary.
	load_data.m 			-> Matlab code for loading data acquired from previous script.
	process_data.m 			-> Code for processing data so it could be loaded into NMF function.

	http://www.igaly.org/rjecnik-hrvatskih-jezika/pages/preuzimanje.php?lang=EN	-> link for dictionary used in make_loadable.sh.
	http://www.cc.gatech.edu/~hpark/nmfsoftware.php					-> link for NMF function used in topic modeling.

