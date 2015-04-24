import pandas as pd
import matplotlib.pyplot as plt

#Imports a data file for a single week and reads it into a pandas dataframe.
dir = "/Users/ilya/metis/week1/group_project_week_1/"
filename = "150321_reorganized.csv"
file = dir + filename
data = pd.read_csv(file)

#Do an outlier analysis on total_entires and remove rows with counts that are 
#way too high:
print data['entry_total'].median() #Answer = 6249
data.boxplot(column = 'entry_total')
plt.show()
print data['exit_total'].median() #Answer = 3563
data.boxplot(column = 'exit_total')
plt.show()

#Take out the highest 2% of entry values and highest 2% of exit values as a 
#shortcut outlier analysis:
data = data.sort(columns = 'entry_total')
two_percent = 2*len(data)/100
data = data[:-two_percent]
data = data.sort(columns = 'exit_total')
data = data[:-two_percent]

