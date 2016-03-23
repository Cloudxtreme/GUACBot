#http://www.guachunter.com/
#freeGuacAndChips method credit to @jayzer1217

import requests,json,gspread,time
from oauth2client.client import SignedJwtAssertionCredentials

def freeGuacAndChips(f,l,m,z):
	print f,l,m,z
	reqUrl='http://api.guachunter.com/guac-it-out/reg'
	postHeaders={
		'Accept-Language':'en-US,en;q=0.8',
		'Origin':'http://www.guachunter.com',
		'Referer':'http://www.guachunter.com/',
		'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.120 Chrome/37.0.2062.120 Safari/537.36'
	}

	payload={"f":f,"l":l,"m":m,"s":"true","z":z}
	session=requests.Session()
	response=session.post(reqUrl,data=json.dumps(payload),headers=postHeaders)
	print response.content

json_key=json.load(open('YourJSONFileName.json')) # Replace with your own json file
scope=['https://spreadsheets.google.com/feeds']
credentials=SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
gc=gspread.authorize(credentials)
worksheet=gc.open('Your Response Sheet Name').sheet1 # Replace with your own sheet name

line=worksheet.col_values(6).count('Done')+2 # Skip header (+1) and get the next row (+1) to start working on, using 'Done' as a completion indicator
delay=1 # Or whatever you want it to be

print 'Starting at line: ' + str(line)

while True:
    if credentials.access_token_expired:
        gc.login() # Refresh the token if it expires
        worksheet=gc.open('Your Response Sheet Name').sheet1
        print 'Token expired, logged in again'
    if (worksheet.cell(line, 1).value != ('')): # These all depend on which columns actually store this data
        first=worksheet.cell(line, 2).value
        last=worksheet.cell(line, 3).value
        mobile=worksheet.cell(line, 4).value
        zipCode=worksheet.cell(line, 5).value

        if (len(zipCode) == 4): # For the fact that Google forms don't keep leading zeroes
            zipCode = '0' + zipCode
        
        print 'Sent form:'
        freeGuacAndChips(first,last,mobile,zipCode)
        worksheet.update_cell(line,6,'Done') # Finished with that line
        line += 1 # Go to the next line and wait for it to be filled
        
    time.sleep(delay) # Adds a delay to the process, you can delete this