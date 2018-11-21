
This package is used to generate academic datasets for gender difference analysis in academia.

To use this package, steps should be followed:
1. Install scholarly package;
2. Build general academic information dataframe: 
	run data_frame.py to get basic academic data from all domains;
	run get_portrait.py to modify the portrait url in dataframe, where downloading portraits is not necessary;
	run get_gender_by_portrait.py to detect gender for researchers;
	run more_scholarly.py to replace scholar.py;
	run hindex.py to retrieve h-index for dataframe;
	run co_author_by_Scholarly.py to get co-author list(get_coauthor_by maka.py is another method for the same function);
	scholar_dataframe_1.csv is an example of the generated dataframe.
3. Install maka package;
4. Build single researcher's publication information dataframe:
	run single_author_dataframe.py to retrieve data from Microsoft Academic;
	run hindex_variation.py to calculate and visualize annual h-index;
	run academic_influence_by_gender.py to visualize gender differences of academic influence.
	
	
	