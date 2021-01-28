import csv
# from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup
import requests

unemployment = {}
# Download the CSV from the URL
req = requests.get('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')
url_content = req.content
csv_file = open('downloaded.csv', 'wb')
csv_file.write(url_content)
csv_file.close()

# us_state_abbrev = {
#     'Alabama': 'AL',
#     'Alaska': 'AK',
#     'American Samoa': 'AS',
#     'Arizona': 'AZ',
#     'Arkansas': 'AR',
#     'California': 'CA',
#     'Colorado': 'CO',
#     'Connecticut': 'CT',
#     'Delaware': 'DE',
#     'District of Columbia': 'DC',
#     'Florida': 'FL',
#     'Georgia': 'GA',
#     'Guam': 'GU',
#     'Hawaii': 'HI',
#     'Idaho': 'ID',
#     'Illinois': 'IL',
#     'Indiana': 'IN',
#     'Iowa': 'IA',
#     'Kansas': 'KS',
#     'Kentucky': 'KY',
#     'Louisiana': 'LA',
#     'Maine': 'ME',
#     'Maryland': 'MD',
#     'Massachusetts': 'MA',
#     'Michigan': 'MI',
#     'Minnesota': 'MN',
#     'Mississippi': 'MS',
#     'Missouri': 'MO',
#     'Montana': 'MT',
#     'Nebraska': 'NE',
#     'Nevada': 'NV',
#     'New Hampshire': 'NH',
#     'New Jersey': 'NJ',
#     'New Mexico': 'NM',
#     'New York': 'NY',
#     'North Carolina': 'NC',
#     'North Dakota': 'ND',
#     'Northern Mariana Islands':'MP',
#     'Ohio': 'OH',
#     'Oklahoma': 'OK',
#     'Oregon': 'OR',
#     'Pennsylvania': 'PA',
#     'Puerto Rico': 'PR',
#     'Rhode Island': 'RI',
#     'South Carolina': 'SC',
#     'South Dakota': 'SD',
#     'Tennessee': 'TN',
#     'Texas': 'TX',
#     'Utah': 'UT',
#     'Vermont': 'VT',
#     'Virgin Islands': 'VI',
#     'Virginia': 'VA',
#     'Washington': 'WA',
#     'West Virginia': 'WV',
#     'Wisconsin': 'WI',
#     'Wyoming': 'WY'
# }


#Get covid cases data
unemployment = {}
unemployment_relative = {}
# county_name = {}
reader = csv.reader(open('downloaded.csv'), delimiter=",")
max_rate = 0
for row in reader:
    try:
        if row[0] == "2020-10-12":
            full_fips = row[3]
            rate = float( row[4].strip() )
            unemployment[full_fips] = rate
            if row[1] == "New York City":
                unemployment["36085"] = rate
                unemployment["36081"] = rate
                unemployment["36047"] = rate
                unemployment["36005"] = rate
                unemployment["36061"] = rate

             #Fillout County Name - FIPS Dictionary
            # else:
            #     name_with_abbreviation = row[1] + ", " + us_state_abbrev[row[2]]
            #     county_name[name_with_abbreviation] = full_fips

        if row[0] == "2020-10-11":
            full_fips = row[3]
            rate = float( row[4].strip() )
            unemployment_relative[full_fips] = rate
            if row[1] == "New York City":
                unemployment_relative["36085"] = rate
                unemployment_relative["36081"] = rate
                unemployment_relative["36047"] = rate
                unemployment_relative["36005"] = rate
                unemployment_relative["36061"] = rate

        #Need to account for the county exceptions
        # New York City

    except:
        pass


#Get the most recent data by comparing the two dates
for key in unemployment:
    unemployment[key] = unemployment[key] - unemployment_relative[key]
    #Get rid of negative rates, since the numbers should only ever be increasing
    if unemployment[key] < 0:
        unemployment[key] = 0
    if unemployment[key] > max_rate:
        max_rate = unemployment[key]

#Get census data
counties = {}
reader1 = csv.reader(open('census-alldata.csv'), delimiter=",")
max_rate = 0
for row1 in reader1:
    try:
        fips = ""

        if len(row1[0]) == 1:
            fips = fips + "0" + row1[0]
        else:
            fips = fips + row1[0]


        if len(row1[1]) == 1:
            fips = fips + "00" + row1[1]
        elif len(row1[1]) == 2:
            fips = fips + "0" + row1[1]
        else:
            fips = fips + row1[1]

        counties[fips] = float( row1[4].strip() )
    except:
        pass

#Make all 5 counties have the combines population
#So the rate % matches
new_york_pop = counties["36085"] + counties["36081"] + counties["36047"] + counties["36005"] + counties["36061"]
counties["36085"] = new_york_pop
counties["36081"] = new_york_pop
counties["36047"] = new_york_pop
counties["36005"] = new_york_pop
counties["36061"] = new_york_pop

# Load the SVG map
svg = open('counties.svg', 'r').read()

# Load into Beautiful Soup
# soup = BeautifulSoup(svg, selfClosingTags=['defs','sodipodi:namedview'], features="html.parser")
soup = BeautifulSoup(svg, features="html.parser")

# Find counties
paths = soup.findAll('path')
#EXPERIMENTAL
black_list_ids = ["t2032", "t2028", "t1909", "t2027", "t2025"]
# for t in titles:
#     if t['id'] != "t3141":
#         if t['id'] in black_list_ids:
#             result = soup.find(id=t['id'])
#             new_title = "New York City" + "\n" + "Number of Cases: " + unemployment["36085"] + "\n" + "Population: " + counties["36085"]
#             t = result.string.replace_with(new_title)
#         else:
#             result = soup.find(id=t['id'])
#             og_title = str(t.string)
#             new_title = og_title + "\n" + "Number of Cases: " + unemployment[county_name[og_title]] + "\n" + "Population: " + counties[unemployment[county_name[og_title]]]
#             t = result.string.replace_with(new_title)

# Map colors
colors = ["#c6dbef", "#eff3ff", "#fdd0a2", "#fdae6b", "#fd8d3c", "#e6550d"]

path_style = '''font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;
stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;
marker-start:none;stroke-linejoin:bevel;fill:'''

# path_style = "fill:"


#This is experimental for the sake of the color gradient
max_rate = 1


test_array=[]
black_list_ids = ["t2032", "t2028", "t1909", "t2027", "t2025"]

for p in paths:
    try:
        if p['id'] not in ["State_Lines", "separator"]:
            x = p['id'].split("_") # Get the fips
            t = p.findAll('title') # Get inner HTML

            if t[0]['id'] in black_list_ids:
                result = soup.find(id=t[0]['id'])
                new_title = "New York City" + "\n" + "Number of Cases: " + str(unemployment["36085"]) + "\n" + "Population: " + str(counties["36085"])
                t[0] = result.string.replace_with(new_title)
            else:
                result = soup.find(id=t[0]['id'])
                og_title = str(t[0].string)
                new_title = og_title + "\n" + "Number of Cases: " + str(unemployment[x[1]]) + "\n" + "Population: " + str(counties[x[1]])
                t[0] = result.string.replace_with(new_title)

            #Get Rate
            x = p['id'].split("_")
            rate = 1000.0 * float(unemployment[x[1]]) / float(counties[x[1]])
            # print(str(unemployment[x[1]]) + "/" + str(counties[x[1]]) + " - " + str(x[1]))
            # print(rate)
            test_array.append(rate)


            if float(len(colors)) * float(rate) / float(max_rate) > 5:
                color_class = 5
            elif float(len(colors)) * float(rate) / float(max_rate) > 4:
                color_class = 4
            elif float(len(colors)) * float(rate) / float(max_rate) > 3:
                color_class = 3
            elif float(len(colors)) * float(rate) / float(max_rate) > 2:
                color_class = 2
            elif float(len(colors)) * float(rate) / float(max_rate) > 1:
                color_class = 1
            else:
                color_class = 0

            color = colors[color_class]
            p['style'] = path_style + color
    except:
        continue


print(soup.prettify())
