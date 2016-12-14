% Last modified 30.11.2016.
%
% process_data  Function process data for faster and more accurate NMF.
%               Function eject all words that appears less than three times
%               and all articles that has less than five words from 
%               further processing. After that each article is normalized
%               so in later NMF looks like every article has same number of words.
%               Function also export reduced dictionary into file 
%               'dictionary_reduced.txt' for further analysis.
%               
%
%   <Input>
%       matrix : (m x n) double matrix. 
%       dictionary : m array of strings.

%   <Outputs>
%        matrix : (m2 x n) matrix with sum of each column of 1 where m2 <= m. 
%        dictionary : m2 array of strings where m2 <= m.
%        
%   <Usage Examples>
%        load_data(matrix, dictionary);

function [matrix, dictionary] = process_data(matrix, dictionary)
    
    % Remove words that appeared less than 3 times in articles.
    [matrix, dictionary] = remove_rows(matrix, dictionary);
    
    % Export reduced dictionary.
    export_used_words(dictionary);
    
    % Remove articles that has less than 5 words and normalize each article.
    matrix = remove_normalize_columns(matrix);
    
    
    
    
    
end


% Function that find all rows in matrix and remove all of them with sum less 
% then 3, also remove same rows from dictionary.
function [matrix, dictionary] = remove_rows(matrix, dictionary)

    appeared = 0;  
    remove_row = -1;
    
    matrix(1,:) = 0;
    
    % For each row in matrix.
    for i=1:size(matrix, 1)
               
        % If sum of row is less than 3 select row for removing.
        if sum(matrix(i,:)) < 3 
            if appeared == 0
                remove_row = i;
                appeared = 1;
            else
                remove_row (end+1) = i;
            end
        end
    
    end

    % If there is at least on row for removing
    % remove all selected rows.
    if appeared == 1
        matrix(remove_row, :) = [];
        dictionary(remove_row, :) = [];
    end

end


% Function that find all columns in matrix and remove all of them with sum less
% than 5, also normalize each column so that sum of each column is 1.
function [matrix] = remove_normalize_columns(matrix)
    
    appeared = 0;
    remove_col = -1;
    
    % For each column in matrix.
    for i=1:size(matrix, 2)
               
        % Save suma, we will use it for normalization.
        suma = sum(matrix(:,i));
        if suma < 5 
            if appeared == 0
                remove_col = i;
                appeared = 1;
            else
                remove_col(end+1) = i;
            end
        % If we won't remove column we need to normalize it.
        else
            matrix(:,i) = matrix(:,i)/suma;
        end
    
    end

    % If there is at least on column for removing
    % remove all selected columns.
    if appeared == 1
        matrix(:, remove_col) = [];
    end
end


% Function for exporting reduced dictionary.
function export_used_words(dictionary)

    fileID = fopen('dictionary_reduced.txt','w');
    [nrows,ncols] = size(dictionary);
    output_format = '%s\n';
    for row = 1:nrows
        fprintf(fileID, output_format, dictionary{row,:});
    end
    fclose (fileID);

end