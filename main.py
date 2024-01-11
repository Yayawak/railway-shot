import requests
from datetime import datetime, timezone, timedelta
import calendar
import ezsheets
import time
import schedule

api_endpoint = 'https://openexchangerates.org/api/latest.json?app_id=042976e8e40745ef883cfc9d015e0bdb'

tz = timezone(timedelta(hours=7))

def getnow():
    return datetime.now(tz=tz)


def oneShotRun():
    global sheet
    mainsheet = sheet['Mainsheet']
    # one_thb_to_jpy, one_jpy_to_thb = gettupletwoRates()
    one_thb_to_jpy, one_jpy_to_thb = getDuoRates()
    print(mainsheet)
    mainsheet[3, 2] = one_thb_to_jpy
    mainsheet[3, 3] = one_jpy_to_thb
    # print(mainsheet[2, 3])
    now = getnow()
    s = f"{now.day}-{now.month}-{now.year}"
    mainsheet[1, 2] = s


def getDuoRates():
    apikey = "13b845c9334cb342dd7345645008a0c2"
    # url = "http://api.exchangeratesapi.io/v1/latest?access_key={}&base=THB&symbols=JPY".format(apikey)
    url = "http://api.exchangeratesapi.io/v1/latest?access_key={}&symbols=JPY,THB".format(apikey)

    response = requests.get(url)

    if response.status_code == 200:
        api_data = response.json()
        jpy_per_1_usd = float(api_data['rates']['JPY'])
        thb_per_1_usd = float(api_data['rates']['THB'])

        one_thb_to_jpy = jpy_per_1_usd / thb_per_1_usd
        one_jpy_to_thb = 1 / one_thb_to_jpy
        print("thb to jpy", one_thb_to_jpy)
        print("jpy to thb", one_jpy_to_thb)

        print(api_data)
        return one_thb_to_jpy, one_jpy_to_thb

    else:
        print(f"Error: Unable to fetch data from the API. Status code: {response.status_code}")
        print(response.text)


if __name__ == '__main__':
    # sheet = ezsheets.Spreadsheet('1j9R0dvNIIVQyBBMHjEySVySrEwy7wxsH6LrgDz0Zfe0')
    # print("Title of This Sheet is = ", sheet.title)

    sheet = ezsheets.Spreadsheet('1AZhNQ49Arn2c8qGnkqDAF8iW4eDEBNMQ2LnIZjh6028')
    # AIzaSyA6FoMiyRV5HbwV-RbgZ272xYSxZ5lzkOc
    # print(sheet)
    # current_month = getnow().strftime("%B")
    # currentMonthSheet = sheet[current_month]


    oneShotRun()

    schedule.every(1).minutes.do(oneShotRun)
    # schedule.every(1).seconds.do(oneShotRun)
    while True:
        schedule.run_pending()
        time.sleep(1)
