Hello, 
You are welcome to SentiLeye sentiment classifier

A sentiment lexicon algorithm to classify pidgin English and English text into positive, negative or neutral


To use this system, you can enter raw text directly or enter your document name (for example, data.csv). Kindly ensure your document is in csv file format.
You need to name the column as 'text'. 
The system creates new column for score and class. 
You should expect the output as shown below. 

            text     score     class
the bank is good      2       positive


## How to use the packages

pip install 

from  sentileye import polarity
## then
polarity.result()

Follow the instructions, enter your csv filename (for example, data.csv) or your raw text directly to classify. 

NB: filename - your csv file must be in your current working directory 