% Last modified 30.11.2016.
%
% load_data Function load all necessary for doing NMF for data clustering.
%           Function is constructing integer matrix (m x n) with informations 
%           how often each word occurred in each article, and string array 
%           (size m) of each word from dictionary. 
%           m -> different words from dictionary.
%           n -> number of articles.
%
%
%   For running function it must be: 
%       (1) in directory with X.txt files, 
%           where X are consecutive natural numbers and starts with 1.txt. 
%           Files have all known words (words from dictionary) from articles 
%           that we want to classify with following shape: 
%               'string number1 number2' where 
%               string is word from dictionary, 
%               number1 is integer number of word occurrence in article and
%               number2 is row number (integer) of word in dictionary.
%       (2) in directory with dictionary_ascii.txt.
%           File represent all words from dictionary without coratians letters
%           (ć, č, đ, š, ž) and words without spaces.
%
%
%   <Input>
%       num_of_files : Number (integer) of files (articles).
%
%   <Outputs>
%        matrix : (m x n) matrix loaded from txt files. 
%        dictionary : m array of word loaded from dictionary_ascii.txt.
%        
%   <Usage Examples>
%        load_data(1182);

function [matrix, dictionary] = load_data(num_of_files)

    # Load dictionary
    dictionary = get_dictionary();
    # Get number of differnt words, needed for constructing occurrence matrix.
    words_in_dictionary = size(dictionary, 1);
        
    matrix = zeros(words_in_dictionary, num_of_files);
    
    #size(matrix)
    #num_of_files
    
    # For each article/file.
    for i = 1:num_of_files
    
        appendix = '.txt';
        file = strcat(int2str(i), appendix);
        a = importdata(file, ' ').data;
        %printf('size a = (%d, %d)\n', size(a));
        
        % For each word in file record number of occurrence.
        for j = 1:size(a,1)
            %printf('matrix(%d, %d) = %d\n', a(j,2), j, a(j,1));
            matrix(a(j,2), i) = a(j,1);
        end
    end
    
end



% Function for loading dictionary from 'dictionary_ascii.txt' file.
function dictionary = get_dictionary()

    fileID = fopen('dictionary_ascii.txt');
    dictionary = textscan(fileID ,'%s'){1,1};
    fclose(fileID);
    
end

