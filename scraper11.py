# Please read the comments below the code prior to running script

from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content,
                         "xml")
    records = soup.find_all("record")

    data=[]

    for record in records:
        date = record.find("date").get_text()
        probes = record.find_all("probe")

        for probe in probes:
            name = probe.find("name").get_text()
            value = probe.find("value").get_text()

            if "TMP" in name or "PH" in name:
                item={}
                item["Date"] = date
                item["Name"] = name
                item["Value"] = value

                data.append(item)

    return data

def export_data(data):
    df = pd.DataFrame(data)
    # Remove duplicates while keeping the first occurrence
    df = df.drop_duplicates()
    df.to_excel("OAtanks.xlsx", index=False)
    df.to_csv("OAtanks.csv", index=False)

if __name__ == '__main__':
    data = get_data("http://10.80.55.36/cgi-bin/datalog.xml?sdate=2410100000&days=1")
    export_data(data)
    print("Done.")

# Replace the URL with your desired format for data collection
# For specific rows (A-E) or bins you can designate them by adding on to the Excel and CSV filenames
    # (e.g., "OAtanksRowA.xlsx")
# pH and temperature data logging interval is currently set to 10 minutes
    # This can be configured in Apex dashboard if one desires a higher resolution (e.g., 1 minute) prior to an experiment.