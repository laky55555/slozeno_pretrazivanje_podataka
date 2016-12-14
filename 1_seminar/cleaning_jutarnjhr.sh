#!/bin/bash


# Script expects 2 arguments. First file in which scraped data is saved,
# and second, file in which cleaned data will be saved, and 2 of them needs
# to be different.
#
#
#
# Script for cleaning and converting text from jutarnji.hr into format
# ready for finding each word from articles in dictionary.
# Script extract text from first parameter (json coding), with following form:
# [
# {"title": "Some title", "url": "http*", "tags": ["first", "second"], "content": "Some text"},
# {"title": "Some title", "url": "http*", "tags": ["first", "second"], "content": "Some text"},
# ...
# {"title": "Some title", "url": "http*", "tags": ["first", "second"], "content": "Some text"}
# ]


# Function is cheking if input values meet criteria for running script.
function check_input() {

	if ! [ -f "$1" ]; then

		echo "cannot access '$1': No such file" >&2
		exit 1
	fi

	if [ "$1" == "$2" ]; then
		echo "Input and output files must be different." >&2
		exit 2
	fi


	cp "$1" "$2"
	if [ "$?" != 0 ]; then
		echo 'Something went wrong with making new file.' >&2
		exit 3
	fi

	return
}

# In input text there is code for every croatian letter.
function edit_croatian_chars() {

	sed -i 's/\\u0106/Ć/g' "$1"
	sed -i 's/\\u0107/ć/g' "$1"

	sed -i 's/\\u010c/Č/g' "$1"
	sed -i 's/\\u010d/č/g' "$1"

	sed -i 's/\\u0160/Š/g' "$1"
	sed -i 's/\\u0161/š/g' "$1"

	sed -i 's/\\u017d/Ž/g' "$1"
	sed -i 's/\\u017e/ž/g' "$1"

	sed -i 's/\\u0110/Đ/g' "$1"
	sed -i 's/\\u0111/đ/g' "$1"

	return
}


# Removing text describing imported pictures, and videos from instagram.
# Removing text describing gallery pictures from jutarnji.hr
function edit_multiple_pictures() {

	# Replacing text describing pictures gallery.
	sed -i 's/\\nSlika.*2016.\\n/ /g' $1
	sed -i 's/\\nZatvori\\nFOTO:/ /g' $1


	#sed -i 's/Pogledajte gale.*", "tags":/", "tags:"/g' $1

	# Replacing instagram photos info.
	# This part is working with gready approach so if there is text between
	# multiple pictures it will be erased.
	# TODO: Do non gready approach when searching for instagram pictures.
	sed -i 's/photo posted.*PDT/ /g' $1
	sed -i 's/Fotog.*PDT/ /g' $1

	sed -i 's/ideo.*PDT/ /g' $1
	sed -i 's/@[a-žA-Ž0-9]*/ /g' $1

	return
}

# Deleting remaining codes from text. There are a lot \u"something" codes.
function remove_backslash_code() {
	# Replace every \n and \" characters with space, spaces won't matter in getting words.
	sed -i 's/\\[n"]/ /g' $1

	# Code that has \u something inside.
	# grep -o  '.\\u[^ ]*' jutarnji-1257.json

	# Deleting every remaining code (etc \u2014).
	# We're not replacing it with space because code could be in the middle of the word.
	sed -i 's/\\u[^ ]\{4\}//g' $1

	return
}

# Extracting content from title and main content on which we will make analysis.
function extract_title_and_content() {

	sed -i 's/", "url.*content": "/ /g' $1
	sed -i 's/"title": " / /g' $1

	return
}

# Converting all text to lower case.
function make_lower_case() {

	sed -i 's/.*/\L&/' $1
	return
}

# Removing interpunction and numbers from text.
function remove_interpunction_and_numbers() {

	sed -i "s/[^a-ž ]*//g" $1
	sed -i '/^\s*$/d' $1

	return
}

# Removing all word that have less then three letters.
function remove_two_letters_of_less() {

	# If there are 2 single words together one passing with sed won't recognize
	# both of them. Needed 2 passes.
	sed -i 's/ [a-ž] / /g' $1
	sed -i 's/ [a-ž] / /g' $1
	sed -i 's/ [a-ž][a-ž] / /g' $1
	sed -i 's/ [a-ž][a-ž] / /g' $1

	return
}


if [ $# != 2 ]; then

	echo "$0: missing input of output file name." >&2
	echo "Usage: $0 [input_file] [output_file]" >&2
    exit 255
fi



check_input $1 $2

edit_croatian_chars $2

edit_multiple_pictures $2

remove_backslash_code $2

extract_title_and_content $2

make_lower_case $2

remove_interpunction_and_numbers $2

remove_two_letters_of_less $2

exit 0
