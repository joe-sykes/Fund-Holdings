# Import Module
    #TYPE IN TO TERMINAL BEFORE STARTING: pip install bs4 requests
from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime
import sys
    #TYPE IN TO TERMINAL BEFORE STARTING: pip install pyfiglet termcolor colorama
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint 
from pyfiglet import figlet_format

cprint(figlet_format('AUTOM8 FUNDS', font='starwars'),
       'white', 'on_green', attrs=['bold'])


#Initialise Lists and Variables
names = []
urls = []
loopCounter = 0
failedData = []



#Collect data from funds.csv
with open('funds.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        names.append(row.get('ï»¿names'))
        urls.append(row.get('urls'))

print(names)

#Cycle through all of the provided URLs
for URL in urls:
    #The computer will take this route if URL is entered correctly
    try:
        #defining browser data for BeautifulSoup to understand
        headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
        page= requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        #Name, 
        fundName = soup.title.text

        #SEDOL
        Sedol = "N/A"

        #Description,
        Description = "Please Input Manually"

        #Fund Manager
        fundManager = "N/A"

        #Yield
        yieldCounter=0
        dividendYield =""

        for link in soup.find_all("tr"):
            dividendYield = (format(link.text))
            yieldCounter=yieldCounter+1
            if yieldCounter== 9:
                break
        dividendYield = dividendYield.replace("\t", "").replace("\r", "").replace("\n", "").replace("%", "%,").replace("  ", "").replace("Dividend yield:", "")

        #Ongoing Charge, 
        chargeCounter=0
        ongoingCharge=""

        for link in soup.find_all("tr"):
            ongoingCharge = (format(link.text))
            chargeCounter = chargeCounter + 1
            if chargeCounter == 8:
                break
        ongoingCharge = ongoingCharge.replace("\t", "").replace("\r", "").replace("\n", "").replace("%", "%,").replace("Ongoing charge:", "")

        #Premium/Discount
        pdCounter=0
        pd=""

        for link in soup.find_all("strong"):
            pd = (format(link.text))
            pdCounter = pdCounter + 1
            if pdCounter == 11:
                break

        #Top 10 Holdings
        exposures=soup.find(id="top-exposures").getText()
        exposures = exposures.replace("\t", "").replace("\r", ",").replace("\n", "").replace("SecurityWeight,","").replace("%,,","%), ").replace(",,"," (").replace("%,","%)")
        exposures = (exposures.strip())
        if "Top 10 " in exposures:
            exposuresSplit=["N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"]

        else:
            exposuresSplit = exposures.split(',')
            
        while len(exposuresSplit) < 10:
            exposuresSplit.extend(["N/A"])

        #CSV creation (if already created the computer will add to the curren CSV)
        documentTitle = ("Generated Reports/"+ str(datetime.today().strftime('%Y-%m-%d'))+".csv")
               

        #Writing to the .CSV
        with open(documentTitle, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            #This will add the header if the cycle is on its first time around
            if loopCounter == 0:
                writer.writerow(["Short Name", "Long Name", "Link", "Sedol", "Description", "Fund Manager", "Yield", "Ongoing Charge", "Discount/Premium", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
                writer.writerow([names[loopCounter], fundName, URL, Sedol, Description, fundManager, dividendYield, ongoingCharge, pd, exposuresSplit[0], exposuresSplit[1], exposuresSplit[2], exposuresSplit[3], exposuresSplit[4], exposuresSplit[5], exposuresSplit[6], exposuresSplit[7], exposuresSplit[8], exposuresSplit[9]])
            #This will just add the data column if it has already cycled through once
            else:
                writer.writerow([names[loopCounter], fundName, URL, Sedol, Description, fundManager, dividendYield, ongoingCharge, pd, exposuresSplit[0], exposuresSplit[1], exposuresSplit[2], exposuresSplit[3], exposuresSplit[4], exposuresSplit[5], exposuresSplit[6], exposuresSplit[7], exposuresSplit[8], exposuresSplit[9]])
        
        print(names[loopCounter])
        print(URL + " Loaded Successfully!\n")
        loopCounter = loopCounter + 1
    #If there is an error, the computer will go to here before looping to the next URL
    except:
        print(names[loopCounter])
        print(URL + " not loaded properly, please ammend!\n")
        failedData.extend([names[loopCounter]])
        loopCounter = loopCounter + 1
        
print('Scrape complete, successfully scraped ' + str(loopCounter-(len(failedData))) +" / "+ str(loopCounter))
print('\nhere were the unsuccessfuly scraped funds:', *failedData, sep='\n- ')

print("\nYour exported file can be found in the 'Generated Report' Folder!")
end_screen = input('Press Enter to Exit.')
if end_screen == "":
    sys.exit()
else:
    sys.exit()

