# Magic algorithm

# Dependencies
Python3 or higher

xlsxwriter

numpy

pandas

networkx

matplotlib

xlrd


# Excell template

Do not change the layout of the template. 

Fill it with your own stocks accordingly.

Columns or rows marked with '*' is autofilled, i.e do not write anything in these.

To get the previous close with the help of excell follow this guide : https://support.microsoft.com/en-us/office/get-a-stock-quote-e5af3212-e024-4d4c-bea0-623cf07fbc54

To extend the graphs click on the graph and click on the third logo from the top, shaped like a cone. Then select "mark data"

Use the "Python" sheet for the program. Simply mark what you want to move from the "Overview" sheet and paste it AS LINK, not just "ctrl + v".

In order to get the stock name correctly working in the program these are not pasted as links but as values, not just "ctrl + v". When pasted as values you need to double click on each cell to make the litte monument icon disappear

By right clicking on where you want to paste it in the python sheet you'll get options of how to paste it, named as "paste options" in the menu.

If your program is not working it is possible that the format of the paste is wrong.

If you are not using Excel make sure to export it from your program as an ".xslx"-file.

# Magic_algorithm
Start the program by double click the "magic_algorithm.py" file.

Choose files accordingly.

Magic number is a number that determines the spread of the stocks you want to buy. High Magic Number => Low spread. Low Magic Number => High spread.

This number is highly connected to the cost of the stocks and the amount of money you have. Test with a few numbers to find the best for your situation.

The result is saved in the "Magic_stock_save_file" if choosen as save file. DO NOT CHOOSE THE SAME READ AND SAVE FILE.

The file that the result is saved to can not be open at the same time as the program runs.

Due to the nature of combinations and permutations the algorithm computational time is n! 

If you can't choose the files change the file layout from "(.xlsx)" to "(*all files)"


# Magic algorithm version 2
This is an improved version using pandas. Extremely quicker

# Dependencies
Python3 or higher

numpy

pandas

yfinance

CurrencyConverter

openpyxl

# Excell template

Do not change the layout of the template. 

Fill it with your own stocks accordingly.

Columns or rows marked with '*' is autofilled, i.e do not write anything in these.

To get the previous close with the help of excell follow this guide : https://support.microsoft.com/en-us/office/get-a-stock-quote-e5af3212-e024-4d4c-bea0-623cf07fbc54

To extend the graphs click on the graph and click on the third logo from the top, shaped like a cone. Then select "mark data"

Use the "Python" sheet for the program. Simply mark what you want to move from the "Overview" sheet and paste it with "ctrl + v".

In order to get the stock name correctly working in the program these are not pasted as links but as values. Simply paste them with "ctrl +v" and then change the data type to Strings in excell

In order to get the stock devidend correctly working in the program these are not pasted as links but as values. Simply paste them with "ctrl +v" and then change the data type to Integers in excell. To fill in the blanks with zeros, follow this guide https://www.avantixlearning.ca/microsoft-excel/how-to-fill-blank-cells-with-zeros-dashes-or-other-values-in-excel/

If your program is not working it is possible that the format of the paste is wrong.

If you are not using Excel make sure to export it from your program as an ".xslx"-file.
# Stocks
# Stocks
