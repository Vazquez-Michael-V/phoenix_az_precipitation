import csv
from datetime import datetime
import matplotlib.pyplot as plt

#Read the .csv file.
filename = 'data/phoenix_az_7.7.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)

    # Want to know the column headers.
    for index, colum_header in enumerate(header_row):
        print(index, colum_header)  

    #Get columns to lists.
    col_1_name, col_5_DATE, col_6_PRCP, col_7_SNOW = [], [], [], []
    missing_data_snow = []
    for row in reader:
        name = row[1]
        col_1_name.append(name)
        current_date = datetime.strptime(row[5], '%Y-%m-%d')
        col_5_DATE.append(current_date)
        prcp = float(row[6])
        col_6_PRCP.append(prcp)
        #Some snow data is missing. Will replace '' with 0.0.
        try:
            snow = float(row[7])
        except ValueError:                       
            missing_data_snow.append(current_date)
            col_7_SNOW.append(0.0)
        else:
            col_7_SNOW.append(snow)

location = list(set((col_1_name[:]))) #Remove duplicates and put into list.
location = location[0]
print(f"\nData is for {location}.")

highest_snowfall = max(col_7_SNOW)
if highest_snowfall == 0.0:
    print(f"Highest snowfall was 0.0 inches.")
    #Highest snowfall is 0.0 inches, so there's nothing to plot here.

#Obtain a sorted list of the years.
years = []
for y in col_5_DATE[:]:
    y = y.strftime('%Y')
    y = int(y)
    years.append(y)    

#Remove duplicates from the list of years.
for y in years[:]:
    if years.count(y) > 1:
        years.remove(y)

#Min and max years.
min_year = min(years)
max_year = max(years)

#Get min date in form YY-MM.
#Min date here happens to be 2014-01, so the graph will show 2014
    #as the first tick on the axis.
min_year_month = col_5_DATE[0]
min_year_month = min_year_month.strftime('%Y-%m')
#Want to use the list years as the xaxis ticks.
#Shows first date in the dataset.
years.insert(0, min_year_month)

max_year_month = col_5_DATE[len(col_5_DATE)-1]
max_year_month = max_year_month.strftime('%Y-%m')
#Want to use the list years as the xaxis ticks.
#Shows last date in the dataset.
years.append(max_year_month)

print(f"Dataset starts on {min_year_month} and ends on {max_year_month}.")    
print(years)

#Plot the precip by dates.
plt.style.use('dark_background')
fig, ax = plt.subplots()
ax.plot(col_5_DATE, col_6_PRCP, c='blue')
title = (f"Precipitation in Phoenix, AZ\n{min_year_month} to {max_year_month}")
ax.set_title(title, fontsize=20)
ax.set_xlabel('Years', fontsize=16)
ax.set_ylabel('Precipitation (inches)', labelpad=15.0, fontsize=16)
ax.tick_params(axis='both', which='both', labelsize=16)

#Uses the years list as the xaxis ticks.
plt.xticks(ticks=years, labels=years, fontsize=16)

#Setting up gridlines.
plt.grid(b=True, which='major', axis='x', color='white', linestyle='-', linewidth=0.5)
plt.grid(b=True, which='major', axis='y', color='white', linestyle='dotted', linewidth=1)

plt.margins(x=0.0, y=0.05) #Adjusting margins.
fig.autofmt_xdate() #Makes the dates slanted.
plt.tight_layout()

plt.show()