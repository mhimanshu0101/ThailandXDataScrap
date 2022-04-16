import requests
from bs4 import BeautifulSoup
import csv

thailand_ric_list = []

with open('thailand_input_fol.csv', 'r') as f:
    lines = f.readlines()
    print("Reading input file....")
    for line in lines[1:]:
        thailand_ric_list.append(line.strip().split(',')[1].split('.')[0])

print(f"Started finding FOL value for {len(thailand_ric_list)} RIC's")


def get_fol_value(ric):
    page = requests.get(
        f"https://www.set.or.th/set/companyprofile.do?symbol={ric}&ssoPageId=4&language=en&country=US",
        verify=False
    )
    
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        table = soup.find("div", {'class': 'table-reponsive'})
    except:
        return

    if not table:
        return
    rows = table.findChildren('div', {'class': 'row'})
    for row in rows:
        try:
            if row.find('strong'):
                if row.find('strong').text.strip() == 'Foreign Limit':
                    # parse FOL value from rows.
                    ric_fol_value = row.contents[3].text.strip().split("(")[0]
                    return ric_fol_value
        except:
            pass
    return


# # Make a request to https://codedamn-classrooms.github.io/webscraper-python-codedamn-classroom-website/
ric_fol_data = []
for ric in thailand_ric_list:
    fol_value = get_fol_value(ric)
    ric_fol_data.append({'ric': ric, 'fol': fol_value if fol_value else ''})

with open('ric_mapped_fol.csv', 'w', newline='\n', encoding='utf-8') as ric_fol_file:
    headers = ('ric', 'fol')
    dict_writer = csv.DictWriter(ric_fol_file, headers, delimiter=';')
    dict_writer.writeheader()
    dict_writer.writerows(ric_fol_data)

