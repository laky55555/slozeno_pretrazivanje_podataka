#!/bin/bash

# Script expects 3 arguments. First file in which cleaned data is saved,
# second, dictionary, and third name of folder in which out will be saved.
#
# Script for converting cleaned text separated into lines into files ready for
# reading into matrix. Script for each line make new file with 3 columns
# separated with black space. Form of file is:
# 'word number_of_occurence line_number_in_dictionary'
#
# Dictionary must have at least 2 columns separated with tabulator '\t'.
# In first column there are all forms of all words that can occurre, and in
# second root form for word from first column.


# Function is cheking if input values meet criteria for running script.
function check_input() {

	if ! [ -f "$1" ]; then

		echo "check_input: cannot access '$1': No such file" >&2
		exit 4
	fi

	if ! [ -f "$2" ]; then

		echo "check_input: cannot access '$2': No such file" >&2
		exit 5
	fi

	if [ -d "$3" ] || [ -f "$3" ]; then

		echo "check_input: directory '$3' already exist." >&2
		exit 5
	fi

	return
}

# Preparing dictionary and text for process_text() function.
# Removing additional columns from dictionary so searching would be faster.
# Splittin input text into separate files for easier text manipulation and
# reading into matlab.
function split_text_vocabular() {

	# That should be extra because we already checked that in check_input.
	rm -rf $3
	mkdir $3
	cp $1 "$3/$1"

	# Editing dictionaries.
	awk -F"\t" '{print $1, $2}' $2 | tr '[:upper:]' '[:lower:]' > "$3/dictionary_2rows"
	awk -F"\t" '{print $2}' $2 | sort -u | tr '[:upper:]' '[:lower:]' > "$3/dictionary_1row"

	# Every article separate file.
	split -l 1 "$3/$1" "$3/article-"

	return

}

# Searching for each word in each article same word in dictionary.
# If word exist count how many occurrence are in artice and save them.
function process_text() {

	cd $1

	# Renaming articles to numbers for easier reading into matlab.
	iterator=1
	ls article* | while read x
	do
		# We will make more versions of same file because some modification
		# can't be done in same file.
		# This part is longest for execution so we output which file we are editing.
		echo start $x
		# Every word goes into new line.
		cat $x | tr -s '[:space:]' '[\n*]' > $x.txt

		# Deleting file because we will append text into one file, must be
		# empty at beginning.
		rm $x

		# For each word in article find root word in dictionary (if exist),
		# and save root word into file.
		cat $x.txt | while read y; do grep -P -m 1 "^$y " dictionary_2rows | awk -F" " '{print $2}' >> $x; done
		# Delete empty lines (there could be at start).
		sed -i '/^\s*$/d' $x

		# Deleting file because we will append text into one file, must be
		# empty at beginning.
		rm $x.txt

		# Find duplicates and save just one of them with number of duplicates.
		cat $x | while read y; do echo -n "$y " >> $x.txt; grep "^$y$" $x | wc -w >> $x.txt; done
		sort -u $x.txt > $x

		# Save modified text into file with form number.txt
		rm $x.txt
		mv $x $iterator.txt

		iterator=$(($iterator+1))
	done

	cd ..
	return
}


# For every word in each article find from which row in dictionaryar is it coming from.
function find_row_from_dictionary() {

	cd $1

	# For each article.
	ls *txt | while read x
	do
		echo start $x

		# For each word in article.
		cat $x | while read y
		do
			# Appending word and number of occurrence in new file with -n so
			# we can append line number of word in dictionary.
			echo -n "$y " >> $x.txt;
			# Saving search pattern for awk command.
			a=`echo $y | grep -o "^[a-ž]*"`;
			# Finding line in dictionary for given word.
			awk -v pat="^$a" -F ":" '$0~pat{print NR; exit }' dictionary_1row >> $x.txt;
		done

		mv $x.txt $x
	done

	cd ..
	return
}


if [ $# != 3 ]; then

	echo "$0: missing parameter." >&2
	echo "Usage: $0 [input_file] [dictionary_directory] [output_directory]" >&2
    exit 255
fi

check_input $1 $2 $3

split_text_vocabular $1 $2 $3

process_text $3

find_row_from_dictionary $3

exit 0
