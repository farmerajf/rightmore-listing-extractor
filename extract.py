from bs4 import BeautifulSoup
import urllib.request
import ssl
import re

context = ssl._create_unverified_context()
fp = urllib.request.urlopen("https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=POSTCODE%5E1172036&minBedrooms=4&radius=0.25&sortType=6&propertyTypes=detached&secondaryDisplayPropertyType=detachedshouses&includeSSTC=true&mustHave=&dontShow=&furnishTypes=&keywords=", context=context)
mybytes = fp.read()
mystr = mybytes.decode("utf8")
fp.close()

soup = BeautifulSoup(mystr, features="html.parser")
result = soup.find_all(name="div", attrs={ "data-test":re.compile("propertyCard-\d")})

for prop in result:
    addressTag = prop.find("meta", attrs={"itemprop":"streetAddress"})
    address = addressTag["content"]
    address = re.sub(r" - REF.*", "", address)
    address = re.sub(r", ", "-", address)

    priceTag = prop.find("div", attrs={"class":"propertyCard-priceValue"})
    price = priceTag.string
    price = re.sub(r"[£|,]", "", price)
    
    print(address + "," + price)