from datetime import datetime
from datetime import timedelta



def enrollInReservationMoreThan48HoursAway(hourGiven):
    rightNow = datetime.now()
    print(rightNow)
    futureReservationTime = datetime.now() + timedelta(days=2)
    
    futureReservationTime = futureReservationTime.replace(hour=hourGiven, minute=0, second=0,microsecond=0)
    print("Future reservation time is at: " + str(futureReservationTime))


    waitingTime = futureReservationTime - datetime.now() - timedelta(days=2)
    print(waitingTime)

    waitingTimeSeconds = waitingTime.total_seconds()

    print(waitingTimeSeconds)

    print("Waiting " + str(waitingTimeSeconds) + " seconds until able to make reservation")


print((3000 + 30)/ 300)

print (3000 % 300)