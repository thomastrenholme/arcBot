##Thomas Trenholme
##5 3 2021
##Choose one desired time you want at the Aztec Rec Center. This program will either wait the correct amount of time and snatch your spot for you 48 hours before, or it will refresh and check for an open spot if the desired time
##Is full.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import easygui
from datetime import datetime
from datetime import timedelta





##My account
username = "{yourusername}"
password = "{yourpassword}"

days = ["Today","Tomorrow","The Day After Tomorrow"]
hours = ["6:00 AM", "8:00 AM", "10:00 AM", "12:00 PM", "2:00 PM", "4:00 PM", "6:00 PM", "8:00 PM", "10:00 PM"]
hoursIntArr = [6, 8, 10, 12, 14, 16, 18, 20, 22]
##easygui.msgbox(msg="Welcome to the ARC Bot developed by Monkey Business Inc.", title="ArcBot v1.1")

##userInput from easyGUI
##usernameEntered = easygui.enterbox(msg="Please enter your Aztec Recreation login username.",title="ArcBot v1.1")
##passwordEntered = easygui.passwordbox(msg="Please enter your Aztec Recreation login password",title="ArcBot v1.1")
##dayEntered = easygui.buttonbox(msg="Please enter which day you would like to make your aztec recreation reservation",title="ArcBot v1.1",choices=days)
##hoursEntered = easygui.multchoicebox(msg="Please enter which hour(s) you would like to make your aztec recreation reservation for",title="ArcBot v1.1",choices=hours)

timeDictionary = {'06:00 AM': 6, '08:00 AM': 8, '09:30 AM': 9.5, '10:00 AM': 10, '11:30 AM': 11.5, '12:00 PM': 12, '01:30 PM': 13.5, '02:00 PM': 14, '02:30 PM': 14.5, '03:00 PM': 15, '03:30 PM': 15.5, '04:00 PM': 16, '06:00 PM': 18, '08:00 PM': 20, '10:00 PM': 22}
def getIntTimeFromStrTime(timeStr):
    return timeDictionary.get(timeStr)


PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH) 
driver.get("https://hdc-p-ols.spectrumng.net/sdsu/Login.aspx?isKiosk=False&AspxAutoDetectCookieSupport=1")

usernameXPath = "//*[@id='ctl00_pageContentHolder_loginControl_UserName']"
usernameBox = driver.find_element_by_xpath(usernameXPath)
usernameBox.send_keys(username)
passwordXPath = "//*[@id='ctl00_pageContentHolder_loginControl_Password']"
passwordBox = driver.find_element_by_xpath(passwordXPath)
passwordBox.send_keys(password)
loginXPath = "//*[@id='ctl00_pageContentHolder_loginControl_Login']"
login = driver.find_element_by_xpath(loginXPath)
login.click()
print("Login successful")
time.sleep(2)
reservationsXPath = "//*[@id='img_GRX']"
reservations= driver.find_element_by_xpath(reservationsXPath)
reservations.click()
time.sleep(1)

def clickTomorrowButton():
    tomorrowButtonXPath = "/html/body/form/div[3]/table[1]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[3]/td/div/div/div/table[1]/tbody/tr[6]/td[2]/table/tbody/tr/td[3]/table/tbody/tr/td[1]/span/label"
    tomorrowButton = driver.find_element_by_xpath(tomorrowButtonXPath)
    tomorrowButton.click()
    time.sleep(1)
clickTomorrowButton()

def setDate(dateString):
    ##Sets the date by disabling the html disabled attribute and resetting the text box
    driver.execute_script("document.getElementById('ctl00_pageContentHolder_ctrlFromDate_txtDate').removeAttribute('disabled');")
    dateTextBox = driver.find_element_by_xpath("//*[@id='ctl00_pageContentHolder_ctrlFromDate_txtDate']")
    dateTextBox.clear()
    time.sleep(1)
    dateTextBox.send_keys(dateString)
    time.sleep(1)
    ##Now Clicks the search button
    searchButton = driver.find_element_by_xpath("//*[@id='btnSearch']")
    searchButton.click()


##Returns the amount of seconds to wait until it is possible to reserve a spot (48 hours away) Enter the hour given in 24-Hour formatted time (22:00)
def calculateWaitUntilReserveAvailable(hourGiven):
    minuteToPut = 0
    rightNow = datetime.now()
    print(rightNow)
    futureReservationTime = datetime.now() + timedelta(days=2)
    
    if(hourGiven - int(hourGiven) != 0):
        hourGiven = int(hourGiven)
        minuteToPut = 30

    futureReservationTime = futureReservationTime.replace(hour=hourGiven, minute=minuteToPut, second=0,microsecond=0)
    print("\nFuture reservation time is at: " + str(futureReservationTime))

    waitingTime = futureReservationTime - datetime.now() - timedelta(days=2)
    print(waitingTime)

    waitingTimeSeconds = waitingTime.total_seconds()

    print(waitingTimeSeconds)

    print("Waiting " + str(waitingTimeSeconds) + " seconds until able to make reservation")
    return waitingTimeSeconds


##This method will attempt to enroll the user in the desired reservation spot of the desired day, hour, and location. For Ex. ("05/08/2021", "02:00 PM", "50 METER POOL")
def enrollInReservation(day, hour, desiredLocation):
    setDate(day)
    time.sleep(1.5)
    found = False
    isFull = False
    correct1stHour = False
    correctLocation = False
    enrollButtonXPath = None
    rows = len(driver.find_elements_by_xpath("//*[@id='lstSchedules']/table/tbody/tr"))
    cols = len(driver.find_elements_by_xpath("//*[@id='lstSchedules']/table/tbody/tr[2]/td"))

    ##Finds the Xpath of the correct enroll button for 
    for i in range(2, rows+1):
        if(found):
            break
        if(isFull):
            break
        for j in range(1, 5):
            value = driver.find_element_by_xpath("//*[@id='lstSchedules']/table/tbody/tr["+str(i)+"]/td["+str(j)+"]").text
            ##print(value) testing purposes

            if(j == 2):
                if(value == hour):
                    correct1stHour = True
                else:
                    correct1stHour = False
            if(j == 4):
                if(correct1stHour):
                    if(value == desiredLocation):
                        try:
                            enrollButtonXPath = driver.find_element_by_xpath("//*[@id='lstSchedules']/table/tbody/tr["+str(i)+"]/td["+str(1)+"]/input")
                            print("Found correct location of button in table.")
                            found = True
                        except:
                            print("Desired Reservation is currently full.")
                            isFull = True
                        break
    
    time.sleep(1)
    if(found):
        enrollButtonXPath.click()
        #If Class is joinable, join. Otherwise report that it could not be joined
        try:
            time.sleep(2)
            agreeButton = driver.find_element_by_xpath("//*[@id='btnWaiverAgree']")
            time.sleep(1)
            agreeButton.click()
            time.sleep(1)
            registerButton = driver.find_element_by_xpath("//*[@id='ctl00_pageContentHolder_btnContinueCart']")
            time.sleep(1)
            registerButton.click()
            time.sleep(1)
            print("Successfully made a reservation for: " + str(hour) + " at the Aztec Recreation Center on: " + day)
            time.sleep(1.5)
            returnToMainMenuButton = driver.find_element_by_xpath("//*[@id='ctl00_pageContentHolder_btnContinuetoShopping']")
            time.sleep(1)
            returnToMainMenuButton.click()
            time.sleep(1.5)
            reservationsXPath = "//*[@id='img_GRX']"
            reservations= driver.find_element_by_xpath(reservationsXPath)
            reservations.click()
            return True
        except:
            errMsg = driver.find_element_by_xpath("//*[@id='ctl00_pageContentHolder_gvMembers_ctl02_imgErrorMessage']").get_attribute("errmsg")
            print("Could not make the reservation for this reason: " + str(errMsg))
            time.sleep(2)
            backButton = driver.find_element_by_xpath("//*[@id='ctl00_pageContentHolder_btnBack']")
            time.sleep(1)
            backButton.click()
            print("\nNavigated back to the reservations main menu")
            return False
    elif isFull:
        print("Unable to register for the desired reservation because it is currently FULL")
        return False
    else:
        print("Desired Reservation was not found with the current date, time, and location combination")


def snagASpotAlreadyFull(day, hour, desiredLocation, attemptNum):
    gotASpot = enrollInReservation(day, hour, desiredLocation)

    if(not gotASpot):
        print("Attempt #: " + str(attemptNum) + ", Trying again... Refreshing the page in 30 seconds\n")
        time.sleep(30)
        driver.refresh()
        time.sleep(2.5)
        clickTomorrowButton()
        return snagASpotAlreadyFull(day, hour, desiredLocation, attemptNum + 1)
    else:
        print("\n\nAttempt #: " + str(attemptNum) + ", Successfully got a spot for: " + str(day) + ", " + str(hour) + ", at the: " + str(desiredLocation))

def snagASpotMoreThan48HoursAway(day, hour, desiredLocation):
    hourInt = getIntTimeFromStrTime(hour)
    waitingTimeSeconds = calculateWaitUntilReserveAvailable(hourInt) + 30
    print("\nGoing to sleep for: " + str(waitingTimeSeconds) + " seconds.")
    for i in range( int(waitingTimeSeconds / 300) + 1):
        time.sleep(300)
        driver.refresh()
        time.sleep(2.5)
        clickTomorrowButton()

    if(enrollInReservation(day, hour, desiredLocation)):
        print("Successfully got a spot for: " + str(day) + ", " + str(hour) + ", at the: " + str(desiredLocation))
    else:
        print("Failed to get the spot for: " + str(day) + ", " + str(hour) + ", at the: " + str(desiredLocation) + " ... :(")
    
##snagASpotMoreThan48HoursAway("05/09/2021", "02:30 PM", "Plex Otdr Workout")
snagASpotMoreThan48HoursAway("05/09/2021", "04:00 PM", "Aztec Rec Center")

print(" YERRR")                
