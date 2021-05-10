##Thomas Trenholme
##5 3 2021
##Choose one desired time you want at the Aztec Rec Center. This program will either wait the correct amount of time and snatch your spot for you 48 hours before, or it will refresh and check for an open spot if the desired time
##Is full.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import easygui
from tkinter import Label, Tk
from datetime import datetime
from datetime import timedelta






#variables to be inputted through GUI, used for the reservation methods
username = ""
password = ""
day = ""
location = ""
hour = ""
moreThan48 = None

days = [ (datetime.now().strftime("%m/%d/"+"20"+"%y")), (datetime.now() + timedelta(days=1)).strftime("%m/%d/"+"20"+"%y"), (datetime.now() + timedelta(days=2)).strftime("%m/%d/"+"20"+"%y") ]
allHours = ["06:00 AM", "08:00 AM", "09:00 AM", "09:30 AM", "10:00 AM", "11:30 AM", "12:00 PM", "01:00 PM", "02:00 PM", "03:30 PM", "04:00 PM", "05:30 PM", "06:00 PM", "07:00 PM", "08:00 PM", "09:00 PM", "10:00 PM"]
arcHours = ["06:00 AM", "08:00 AM", "10:00 AM", "12:00 PM", "02:00 PM", "04:00 PM", "06:00 PM", "08:00 PM", "10:00 PM"]
poolHours = ["10:00 AM", "11:30 AM", "01:00 PM", "02:30 PM", "04:00 PM", "05:30 PM"]
locations = ["Aztec Rec Center", "Comp Pool Lap Swim", "Rec Field Otdr Workout", "ARC Express", "Plex Otdr Workout", "Rec Pool Lap Swim"]
hoursIntArr = [6, 8, 10, 12, 14, 16, 18, 20, 22]

def tkMessageBoxDeleteAfterXsec(msgStr, x):
        ##Tk Message pop up
        root = Tk()
        root.title("Arc Bot v1.2")
        prompt = msgStr
        label1 = Label(root, text=prompt, width=len(prompt))
        label1.pack()

        def close_after_Xs():
            root.destroy()

        root.after(x, close_after_Xs)
        root.mainloop()
        ##


def easyGuiSetup():
    easygui.msgbox(msg="Welcome to the ARC Bot developed by Monkey Business Inc.", title="ArcBot v1.2")
    ##userInput from easyGUI
    username = str(easygui.enterbox(msg="Please enter your Aztec Recreation login username.",title="ArcBot v1.2"))
    password = easygui.passwordbox(msg="Please enter your Aztec Recreation login password",title="ArcBot v1.2")
    day = easygui.buttonbox(msg="Please enter which day you would like to make your aztec recreation reservation",title="ArcBot v1.2",choices=days)

    location = easygui.choicebox(msg="Please enter the location you are making your reservation for.",title="ArcBot v1.2",choices=locations)
    if(location=="Comp Pool Lap Swim" or location=="Rec Pool Lap Swim"):
        hour = easygui.choicebox(msg="Please enter which hour you would like to make your aztec recreation reservation for.\nNote: Comp and Rec Pool Reservations are available every 1.5 hours starting 10:00 AM - 5:30 PM",title="ArcBot v1.2",choices=poolHours)
    elif(location=="Aztec Rec Center"):
        hour = easygui.choicebox(msg="Please enter which hour you would like to make your aztec recreation reservation for.\nNote: ARC Reservations are only available every two hours starting 6:00 AM - 10:00 PM.\n6:00 AM and 10:00 PM are not available on friday or weekends.",title="ArcBot v1.2",choices=arcHours)
    else:
        hour = easygui.choicebox(msg="Please enter which hour you would like to make your aztec recreation reservation for",title="ArcBot v1.2",choices=allHours)
    
    
    ##If the day selected is 2 days from now, check if the reservation is more than 48 hours away from now. 

    masQue48 = None
    if(day == days[2]):
        if(hour is not None):
            futureReservationTime = (datetime.now() + timedelta(days=2) ).replace(hour=getIntTimeFromStrTime(hour), minute=0, second=0,microsecond=0)

            difference = futureReservationTime - datetime.now()

            differenceHours = difference.total_seconds() / 3600

            if(differenceHours > 48):
                ##print("\n\nThe selected date is more than 48 HOURS AWAY")
                masQue48 = True
            else:
                masQue48 = False

    return username, password, day, location, hour, masQue48



timeDictionary = {'06:00 AM': 6, '08:00 AM': 8, '09:30 AM': 9.5, '10:00 AM': 10, '11:30 AM': 11.5, '12:00 PM': 12, '01:00 PM': 13, '01:30 PM': 13.5, '02:00 PM': 14, '02:30 PM': 14.5, '03:00 PM': 15, '03:30 PM': 15.5, '04:00 PM': 16, '05:00 PM': 17, '05:30 PM': 17.5, '06:00 PM': 18, '08:00 PM': 20, '10:00 PM': 22}
def getIntTimeFromStrTime(timeStr):
    return timeDictionary.get(timeStr)



def clickTomorrowButton(driver):
    tomorrowButtonXPath = "/html/body/form/div[3]/table[1]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[3]/td/div/div/div/table[1]/tbody/tr[6]/td[2]/table/tbody/tr/td[3]/table/tbody/tr/td[1]/span/label"
    tomorrowButton = driver.find_element_by_xpath(tomorrowButtonXPath)
    tomorrowButton.click()
    time.sleep(2)


def setDate(dateString, driver):
    ##Sets the date by disabling the html disabled attribute and resetting the text box
    driver.execute_script("document.getElementById('ctl00_pageContentHolder_ctrlFromDate_txtDate').removeAttribute('disabled');")
    dateTextBox = driver.find_element_by_xpath("//*[@id='ctl00_pageContentHolder_ctrlFromDate_txtDate']")
    dateTextBox.clear()
    time.sleep(2)
    dateTextBox.send_keys(dateString)
    time.sleep(2)
    ##Now Clicks the search button
    searchButton = driver.find_element_by_xpath("//*[@id='btnSearch']")
    searchButton.click()


##Returns the amount of seconds to wait until it is possible to reserve a spot (48 hours away) Enter the hour given in 24-Hour formatted time (22:00)
def calculateWaitUntilReserveAvailable(hourGiven):
    minuteToPut = 0
    rightNow = datetime.now()
    ##print(rightNow)
    futureReservationTime = datetime.now() + timedelta(days=2)
    
    if(hourGiven - int(hourGiven) != 0):
        hourGiven = int(hourGiven)
        minuteToPut = 30

    futureReservationTime = futureReservationTime.replace(hour=hourGiven, minute=minuteToPut, second=0,microsecond=0)
    ##print("\nFuture reservation time is at: " + str(futureReservationTime))

    waitingTime = futureReservationTime - datetime.now() - timedelta(days=2)
    ##print(waitingTime)

    waitingTimeSeconds = waitingTime.total_seconds()

    ##print(waitingTimeSeconds)

    tkMessageBoxDeleteAfterXsec("Waiting " + str(waitingTimeSeconds) + " seconds until able to make reservation.\nThe Program will refresh every 5 minutes until then to not timeout...", 10000)

    return waitingTimeSeconds


##This method will attempt to enroll the user in the desired reservation spot of the desired day, hour, and location. For Ex. ("05/08/2021", "02:00 PM", "50 METER POOL")
def enrollInReservation(day, hour, desiredLocation, driver):
    setDate(day, driver)
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
                            ##print("Found correct location of button in table.")
                            found = True
                        except:
                            ##print("Desired Reservation is currently full.")
                            isFull = True
                        break
    
    time.sleep(2)
    if(found):
        enrollButtonXPath.click()
        time.sleep(2)
        #If Class is joinable, join. Otherwise report that it could not be joined
        try:
            time.sleep(2)
            agreeButton = driver.find_element_by_xpath("//*[@id='btnWaiverAgree']")
            time.sleep(2)
            agreeButton.click()
            time.sleep(2)
            registerButton = driver.find_element_by_xpath("//*[@id='ctl00_pageContentHolder_btnContinueCart']")
            time.sleep(2)
            registerButton.click()
            time.sleep(2)
            ##print("Successfully made a reservation for: " + str(hour) + " at the Aztec Recreation Center on: " + day)
            time.sleep(1.5)

            """maybe for the future
            returnToMainMenuButton = driver.find_element_by_xpath("//*[@id='ctl00_pageContentHolder_btnContinuetoShopping']")
            time.sleep(2)
            returnToMainMenuButton.click()
            time.sleep(1.5)
            reservationsXPath = "//*[@id='img_GRX']"
            reservations= driver.find_element_by_xpath(reservationsXPath)
            reservations.click()
            """
            return True
        except:
            errMsg = driver.find_element_by_xpath("//*[@id='ctl00_pageContentHolder_gvMembers_ctl02_imgErrorMessage']").get_attribute("errmsg")
            ##print("Could not make the reservation for this reason: " + str(errMsg))
            time.sleep(2)
            backButton = driver.find_element_by_xpath("//*[@id='ctl00_pageContentHolder_btnBack']")
            time.sleep(2)
            backButton.click()
            ##print("\nNavigated back to the reservations main menu")
            return False
    elif isFull:
        ##print("Unable to register for the desired reservation because it is currently FULL")
        return False
    else:
        ##print("Desired Reservation was not found with the current date, time, and location combination")
        pass



def snagASpotAlreadyFull(day, hour, desiredLocation, attemptNum, driver):
    gotASpot = enrollInReservation(day, hour, desiredLocation, driver)
    if gotASpot is None:
        easygui.msgbox(msg="Desired Reservation was not found with the current date, time, and location combination. Quitting...", title="ArcBot v1.2")
        driver.quit()
    else:
        if(not gotASpot):
            msgForBox = ("\nAttempt #: " + str(attemptNum) + "\nFailed to get a spot for: " + str(day) + ", " + str(hour) + ", at the: " + str(desiredLocation) + " because it is currently full...\nTrying again in 30 seconds")
            tkMessageBoxDeleteAfterXsec(msgForBox, 5000)

            time.sleep(30)
            driver.refresh()
            time.sleep(2.5)
            clickTomorrowButton(driver)
            return snagASpotAlreadyFull(day, hour, desiredLocation, attemptNum + 1, driver)
        else:
            easygui.msgbox(msg="\nAttempt #: " + str(attemptNum) + ", Successfully got a spot for: " + str(day) + ", " + str(hour) + ", at the: " + str(desiredLocation), title="ArcBot v1.2")
            driver.quit()

def snagASpotMoreThan48HoursAway(day, hour, desiredLocation, driver):
    hourInt = getIntTimeFromStrTime(hour)
    waitingTimeSeconds = calculateWaitUntilReserveAvailable(hourInt) + 30
    ##print("\nGoing to sleep for: " + str(waitingTimeSeconds) + " seconds.")
    for i in range( int(waitingTimeSeconds / 300) + 1):
        time.sleep(300)
        driver.refresh()
        time.sleep(2.5)
        clickTomorrowButton(driver)

    if(enrollInReservation(day, hour, desiredLocation, driver)):
        easygui.msgbox(msg="Successfully got a spot for: " + str(day) + ", " + str(hour) + ", at the: " + str(desiredLocation), title="Arc Bot v1.2")
        driver.quit()
    else:
        easygui.msgbox(msg="Failed to get the spot for: " + str(day) + ", " + str(hour) + ", at the: " + str(desiredLocation) + " ... :(", title="Arc Bot v1.2")
        driver.quit()
    

def allInputFilled():
    if(username == "" or username is None or password is None or password == "" or day == "" or hour is None or location is None or moreThan48 is None):
        return False
    return True

username, password, day, location, hour, moreThan48 = easyGuiSetup()

if(allInputFilled()):
    ##Run the program

    time.sleep(2)
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

    time.sleep(2)
    reservationsXPath = "//*[@id='img_GRX']"
    reservations= driver.find_element_by_xpath(reservationsXPath)
    reservations.click()
    time.sleep(2)
    clickTomorrowButton(driver)
    if(moreThan48):
        snagASpotMoreThan48HoursAway(day, hour, location, driver)
    else:
        snagASpotAlreadyFull(day, hour, location, 1, driver)


    tkMessageBoxDeleteAfterXsec("Thank you for using the Arc Bot v1.2 developed by Thomas Trenholme.\nHave a great day!", 5000)     

else:
    tkMessageBoxDeleteAfterXsec("Not all info easy inputted correctly in the GUI, please try again", 5000)