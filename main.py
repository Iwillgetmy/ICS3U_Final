# This is a list of all the imports
# This is importing random. Will be used for the spawning of coins and other vehicles
import random
# This is the import needed to use the camera
import cv2
# Media pipe is used for the actual game and the movement
import mediapipe as mp
# this is used to keep time during the game
import time
# Importing pygame
import pygame

# Initializing hand recognition libraries & variables, also pygame libraries & variable initialiation
cap = cv2.VideoCapture(0)
pygame.init()
# This is inditializing the hand
mpHands = mp.solutions.hands
# this is setting ket information, like to only detect one hand
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=1,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils
# This is setting the name of the display and its dimensions
display = pygame.display.set_mode((700, 600))
# This is initilizing the clock in pygame
clock = pygame.time.Clock()


# Different stats for user.
# Different stats for user.
userStats = [1000, 0]
# This is a variable used for the user to decide if they want to play using hand recognition or keyboard
keyboardOrCamera = "Keyboard"
# This is a list that holds all the powerup images
powerupImages = [pygame.transform.scale(pygame.image.load('Images/double_score.png'), (100, 100)), pygame.transform.scale(pygame.image.load('Images/coin2.png'), (100, 100)),
                 pygame.transform.scale(pygame.image.load('Images/doublelife.png'), (100, 100))]
# This is a list that holds all the different car colour images
listy = [pygame.transform.scale(pygame.image.load('Images/blue.png'), (80, 100)),
         pygame.transform.scale(pygame.image.load('Images/red.jpg'), (80, 100)), pygame.transform.scale(pygame.image.load('Images/yellow.png'), (80, 100)), pygame.transform.scale(pygame.image.load('Images/orange.png'), (80, 100)), pygame.transform.scale(pygame.image.load('Images/green.png'), (80, 100)), ]
# This is a list that holds the number of each powerup the user has
items = [0, 0, 0]
# Checking if a powerup is chosen
powerChosen = [-1, -1, -1]
# This stores the current prestige level of the user, and the cost to upgrade to the next level
prestigelevel = [0, 1000]

# This function was made by Darun. Used to reduce the initilization of font sizees/types. Could be improved by alowing different font families


def font(size):
    """
    Method to return a pygame font of a specific size
    Args:
        size: size of the text
    """
    # this is just the standart font that will be used
    return pygame.font.SysFont("freesansbold.tt", size)

# This function was made by Darun, Ronil helped him out though. Good function and helps drastically reduce line efficiancy of code


def hoverAnimate(xVal, yVal, width, height, buttonMessage):
    """
        Variable to make colors change when hovering over a buttons
        Args:
            xVal: X coordinate for top left of the button
            yVal: Y coordinate for the top left of the button
            width: width of the button
            height: height of the button
            buttonMessage: text the button displays
        Returns:
            N/A
    """

    mouse = pygame.mouse.get_pos()  # Getting the mouse position
    # If hovering over mouse, background is (0,0,0) and text is (255,255,255)
    if xVal <= mouse[0] <= xVal+width and yVal <= mouse[1] <= yVal+height:
        # drawing the rectangle
        pygame.draw.rect(display, (0, 0, 0), [xVal, yVal, width, height])
        display.blit(pygame.font.SysFont("freesansbold.tt", 20).render(
            buttonMessage, 1, (255, 255, 255)), (xVal+10, yVal+10, width, height))
    else:  # Opposite if not hovering
        # drawing the rectangle
        pygame.draw.rect(display, (255, 255, 255), [xVal, yVal, width, height])
        display.blit(pygame.font.SysFont("freesansbold.tt", 20).render(
            buttonMessage, 1, (0, 0, 0)), (xVal+10, yVal+10, width, height))

# Function to make a label which covers the entirety of the page. This function was made by Darun


def labelCode(message):
    """
        Simple function to create a label on the screen
        Args:
            message: A string which stores the message to be displayed on the screen
    """
    # This is initilizing the label
    label = font(40).render(message, 1, (255, 255, 255))
    # making a rectangle for the text
    pygame.draw.rect(display, (255, 0, 0), (0, 0, 700, 600))
    # printing out the text
    display.blit(label, (230, 300))

# Code for the actual game which uses hand recognition
# All the functionality was decided by both Ronil and Darun. Darun was the one who wrote the code for this section. Ronil assisted with adding some sections of the code, like the movealbe background, and he helped during the debugging


def game(keyboardOrCamera, listy, powerChosen):
    """
        The actual game. Here, users will control a car with their hand through hand tracking and must collect coins while avoiding oncoming wasif's.
    Args:
        keyboardOrCamera: A string which stores the current device being used for the game
        listy: A list of pygame images to choose the color of the car
        powerChosen: A list of ints which stores what powers are currently chosen. Each array index represents a different power
    Returns:
    """

    # Initialization of all of the variables
    # This is the coin image
    coin = pygame.transform.scale(
        pygame.image.load('Images/coin.png'), (50, 50))
    # This is the background track image
    bg = pygame.transform.scale(
        pygame.image.load('Images/track2.png'), (700, 600))
    # This is the heart image
    heart = pygame.transform.scale(
        pygame.image.load('Images/heart.jpg'), (50, 50))
    # Setting this variable to true. start off assuming the hand can be seen
    handDetected = True
    xVals = [485, 400, 310, 220, 130]
    averageX = 300
    averageY = 400
    # This is the total number of coins collected
    coinsCollected = 0
    # This is the final sum of all the points
    sum = 0
    # This is a variable used to track the number of iterations of the code
    iterations = 0
    arrObjects = []
    coinVar = [False, 0, 0]
    lastPos = [-100, -100]
    # Setting the Y value for the first image
    bgY = 0
    bgY2 = bg.get_height()
    lives = max(powerChosen[2]+1, 1)
    cpuVeichles = [pygame.transform.scale(
        pygame.image.load('Images/cpu1.png'), (50, 80)), pygame.transform.scale(
        pygame.image.load('Images/cpu2.png'), (50, 80)), pygame.transform.scale(
        pygame.image.load('Images/cpu3.png'), (50, 80)), pygame.transform.scale(
        pygame.image.load('Images/cpu4.png'), (70, 80)), pygame.transform.scale(
        pygame.image.load('Images/cpu5.png'), (70, 80)), pygame.transform.scale(
        pygame.image.load('Images/cpu6.png'), (70, 80)), ]
    # Looping until user dies/wins
    while True:

        # Different movement if camera or keyboard device
        if keyboardOrCamera == "Camera":
            # Getting each point of finger, then getting the average location of the users hand
            success, img = cap.read()
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)
            if results.multi_hand_landmarks:  # Checking if hand is recognized
                averageX = 0
                averageY = 0
                sum = 0

                # Getting each hand landmark (each joint of finger is a different landmark)
                for handLms in results.multi_hand_landmarks:
                    displayWarning = False
                    for id, lm in enumerate(handLms.landmark):
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y*h)
                        averageX += cx
                        averageY += cy
                        sum += 1

                # Getting average x and y values for the hand
                averageX /= sum
                averageY /= sum
                averageX = 600-averageX+30

                # Making sure user doesn't teleport after hand not detected
                if not handDetected:
                    # This checks if the users hand was in the same position as it was in before it left the screen
                    if lastPos[0]-150 <= averageX <= lastPos[0]+150 and lastPos[1]-150 <= averageY <= lastPos[1]+150 or lastPos[0] == -100:
                        handDetected = True
                    # If the hand position isnt the same as last iteration. Then the user has teleported
                    else:
                        # An error messages pops up
                        labelCode("Dont Try Teleporting")
                        pygame.draw.rect(display, (255, 255, 255),
                                         (lastPos[0], lastPos[1], 150, 50))
                        pygame.display.update()
                        continue

            else:  # If hand isn't recognized, then set boolean to displaywarning to true
                handDetected = False
        else:
            # This is for the users who use keyboard to play
            keys = pygame.key.get_pressed()
            # This is to turn left
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and averageX > 0:
                averageX -= (15+(iterations//200))
            # this is to turn right
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and averageX < 600:
                averageX += (15+(iterations//200))
            # This is to go up
            if (keys[pygame.K_UP] or keys[pygame.K_w]) and averageY > 0:
                averageY -= (15+(iterations//200))
            # This is to go down
            if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and averageY < 500:
                averageY += (15+(iterations//200))
        # This is checking if the hand is detected
        if handDetected:
            # Cpu spawning. Probability for a cpu to spawn rises overtime, cap also rises with prestige level
            if iterations < 1200+(prestigelevel[0]*30):
                # Depending on the number of iterations there is a higher change that an incoming car will spawn
                if random.randint(1+int(iterations/40-(prestigelevel[0]*2)), 50) == 50:

                    # Creating the array object, and storing the cpu's x coordinate, y xoordinate, its image (what cpu image) and if it is a hittable object
                    arrObjects.append(
                        [random.choice(xVals), 0, random.choice(cpuVeichles), True])

            else:
                if random.randint(1+int(1200/40-(prestigelevel[0]*2)), 50) == 50:
                    arrObjects.append(
                        [random.choice(xVals), 0, random.choice(cpuVeichles), True])

            # Code to make a moving background
            display.blit(bg, (0, -bgY))
            display.blit(bg, (0, -bgY2))
            # As more iterations go by, the screen moves faster
            bgY = bgY - (5+(iterations//200))
            bgY2 = bgY2 - (5+(iterations//200))

            # If the y value of the first background image is out of the screen, It resets it.
            if bgY < bg.get_height() * -1:
                bgY = bg.get_height()

            # If the y value of the first background image is out of the screen, It resets it.
            if bgY2 < bg.get_height() * -1:
                bgY2 = bg.get_height()

            # Random chance for a coin to spawn (collect the coin)
            if not coinVar[0] and random.randint(1, 50) == 50:
                coinVar[0] = True
                coinVar[1] = random.randint(130, 510)
                coinVar[2] = random.randint(50, 550)

            # Displaying number of hearts
            for i in range(lives):
                display.blit(heart, (635-i*50, 50))

            # Checking if a coin is spawned, then checking for collision
            if coinVar[0]:
                display.blit(coin, (coinVar[1], coinVar[2]))
                # If collision, then up the coins collected and set the first element in array to false, stating no coin on track
                if listy[0].get_rect(topleft=(averageX, averageY)).colliderect(coin.get_rect(topleft=(coinVar[1], coinVar[2]))):
                    coinsCollected += 1
                    coinVar[0] = False
            # Looping through all current cpu objects
            for i in range(len(arrObjects)):
                # Displaying object
                display.blit(arrObjects[i][2],
                             arrObjects[i][2].get_rect(center=(arrObjects[i][0]+40, arrObjects[i][1])))
                # All death conditions (going outside of screen, colliding with car). The last and statement checks is False if it was the car that removed user's double life powerup
                if listy[0].get_rect(topleft=(averageX, averageY)).colliderect(arrObjects[i][2].get_rect(topleft=(arrObjects[i][0], arrObjects[i][1]))) and arrObjects[i][3] != False:

                    # If the powerup chosen is double life, remove the power, deduct 1 life, and set the object that hit the car to be unable to collide with the user's car
                    if powerChosen[2] == 1:
                        powerChosen[2] = -1
                        lives -= 1
                        arrObjects[i][3] = False

                    # If the double life powerup isn't chosen, go here
                    else:

                        # If the doublescore power is chosen, double their score at the end. It is put before double points because iterations counts towards final points accumulated. Set powerup to false once dead
                        if powerChosen[0] == 1:
                            iterations *= 2

                        # If powerupchosen is double coins, multiply the amount of coins collected by 2
                        if powerChosen[1] == 1:
                            userStats[0] += coinsCollected * \
                                (iterations//100+1)*2
                        else:
                            userStats[0] += coinsCollected*(iterations//100+1)

                        # Tell the user that they died, and keep the label there for 1 second. Also check for a new highscore then return to homepage
                        labelCode("       YOU DIED")
                        pygame.display.update()
                        time.sleep(1)
                        userStats[1] = max(userStats[1], iterations)
                        for i in range(3):
                            powerChosen[i] = -1
                        return

                # Make cpu car move down screen
                arrObjects[i][1] += (10+(iterations//200))

            if len(arrObjects) > 0:  # If there are and cpu objects, go into if statement
                # If the cpu's y coordinate is greater than or equal to 600, delete it
                if arrObjects[0][1] >= 600:
                    arrObjects.pop(0)

            # Displaying imge of car, which is updated with the x and y values of users hand
            display.blit(listy[0], (averageX, averageY))

            # Updating variables
            lastPos = [averageX, averageY]
            iterations += 1

            # Checks to see if the user went to the grass area. If they did, make them die (you aren't allowed to touch grass in this game)
            if averageX < 130 or averageX > 510:

                # Checking if they activated double score, and doing the needed actions
                if powerChosen[0] == 1:
                    iterations *= 2
                # Checking if they activated double coins, and doing the needed actions
                if powerChosen[1] == 1:
                    userStats[0] += coinsCollected*(iterations//100+1)*2
                else:
                    userStats[0] += coinsCollected*(iterations//100+1)

                # Informing the user they died, resetting needed variables and returning to homescreen
                labelCode("       YOU DIED")
                pygame.display.update()
                time.sleep(1)
                userStats[1] = max(userStats[1], iterations)
                for i in range(3):
                    powerChosen[i] = -1
                return

        # If hand isn't detected, inform the user
        else:
            labelCode("Hand Not Deteced")

        for event in pygame.event.get():  # If the user quits screen, exit code
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Setting fps cap to 20
        clock.tick(20)

        # Displaying the user's score, and doubling it if the user activated double score. Important note, we didn't simply write iterations+=2 isntead of iteration+=1 because that would make the game significantly harder (spawning rate of cpu cars)
        if powerChosen[0] == 1:
            pygame.draw.rect(display, (0, 0, 0), [
                             0, 0, 160+(len(str(iterations*2)))*10, 50])
            display.blit(font(40).render(
                "SCORE:"+str(iterations*2), 1, (255, 255, 255)), (20, 10))

        else:
            pygame.draw.rect(display, (0, 0, 0), [
                             0, 0, 160+(len(str(iterations)))*10, 50])
            display.blit(font(40).render(
                "SCORE:"+str(iterations), 1, (255, 255, 255)), (20, 10))

        pygame.display.update()  # Updating pygame screen


# The functionality was made by Ronil and Darun. Darun made the main code for this section and Ronil assisted and did a lot of the re-formatting and debugging

def homepage(userStats, keyboardOrCamera, prestigelevel):
    """
    Home page of the game, and main navigation center. Here users will be able to play the game, read instructions, go to the upgrade section, and more
    Args:
        # points, highscore, etc...
        userStats: A list ints of of the user's stats. This includes
        keyboardOrCamera: A string which stores Current device chosen for game
        prestigeleve: a list of ints which says what the user's  current prestige level is, and how much it'll cost for the next prestige level
    Returns:
        "u": A string which will lead to the upgrade Page
        "r": A string which will lead to the prestige/restart Page
        "i": A string which will lead to the instructions Page
        "h": A string whih will lead to the handCheck Page
        "c": A string which will lead to the customization page
    """

    # Essential variables
    questionDimension = 50
    keystrokes = []
    # #These are global variables that are needed
    # global userStats
    # global keyboardOrCamera
    # global prestigelevel
    while True:
        # Creating initial displays, such as title screen, #coins collected, etc...
        # This inidializes question image
        questionImg = pygame.transform.scale(pygame.image.load(
            'Images/questionmark.png'), (questionDimension, questionDimension))
        # Making the display colour yellowish
        display.fill((255, 255, 155))
        # initializing all the text
        header_text = font(120).render("Virtual Racer", True, (0, 0, 0))
        info3_text = font(40).render(
            "Points: "+str(userStats[0]), True, (0, 0, 0))
        info4_text = font(40).render(
            "High Score: "+str(userStats[1]), True, (0, 0, 0))
        info5_text = font(40).render("Current Device: " +
                                     keyboardOrCamera, True, (0, 0, 0))

        # Blitting items to the screen
        # Displaying the different texts on the screen
        display.blit(header_text, (25, 25))
        display.blit(info3_text, (25, 125))
        display.blit(info4_text, (25, 175))
        display.blit(info5_text, (25, 225))
        display.blit(font(40).render("Prestige cost: " +
                     str(prestigelevel[1]) + " points", True, (0, 0, 0)), (25, 275))
        display.blit(font(40).render("Prestige Level: " +
                     str(prestigelevel[0]), True, (0, 0, 0)), (25, 325))
        # Variables for display width and length
        X = 600
        Y = 700

        mouse = pygame.mouse.get_pos()  # Getting the x and y values of mouse

        # Animating when hover over questionmark
        if 600 <= mouse[0] <= 650 and 40 <= mouse[1] <= 105:
            # Increases the size of questionmark
            questionDimension = 75
        else:
            questionDimension = 50
        # displays the questionmark
        display.blit(questionImg, questionImg.get_rect(center=(625, 75)))

        # Event listener
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the user quits, quit the code
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # If a mouse was clicked...
                # If the user clicked the game button, visit the game
                if 500 <= mouse[0] <= 640 and 425 <= mouse[1] <= 465:
                    return "u", keyboardOrCamera
                # If the user clicked the quit button, exit the code
                elif 50 <= mouse[0] <= 190 and 425 <= mouse[1] <= 465:
                    pygame.quit()
                    quit()
                elif 200 <= mouse[0] <= 340 and 425 <= mouse[1] <= 465:
                    # Switching option if user clicked the switch device button
                    cap  # Defined outside as it neeeeeds to update
                    if keyboardOrCamera == "Camera":
                        keyboardOrCamera = "Keyboard"
                    else:
                        # If the user doesn't have a camera, don't let them use hand recognition gameplay
                        if cap != None and cap.isOpened():
                            keyboardOrCamera = "Camera"
                # depending on the button that is clicked, they will be sent to a different page
                elif 350 <= mouse[0] <= 490 and 500 <= mouse[1] <= 540:
                    return "r", keyboardOrCamera
                elif 600 <= mouse[0] <= 650 and 40 <= mouse[1] <= 105:
                    return "i", keyboardOrCamera
                elif 200 <= mouse[0] <= 340 and 500 <= mouse[1] <= 540:
                    cap  # Defined outside as it neeeeeds to update
                    if cap != None and cap.isOpened():
                        return "h", keyboardOrCamera
                elif 350 <= mouse[0] <= 490 and 425 <= mouse[1] <= 465:
                    return "c", keyboardOrCamera

        # Checking if money was typed, and setting points to 100000
        keys = pygame.key.get_pressed()
        count = 0
        for i in keys:
            if i:
                if count in [16, 18, 17, 8, 28] and len(keystrokes) != 5:
                    if len(keystrokes) > 0:
                        if keystrokes[len(keystrokes)-1] != count:
                            keystrokes.append(count)
                    else:
                        keystrokes.append(count)
                    break
                else:
                    keystrokes.clear()
            count += 1
        print(keystrokes)
        if [16, 18, 17, 8, 28] == keystrokes:
            print("hi")
            userStats[0] = 100000

        # Displaying the buttons with the hover annimation
        hoverAnimate(500, 425, 140, 40, 'Go to game')
        hoverAnimate(50, 425, 140, 40, 'Quit Game')
        hoverAnimate(350, 500, 140, 40, 'Prestige')
        hoverAnimate(200, 500, 140, 40, "Camera Test")
        hoverAnimate(200, 425, 140, 40, 'Change Device')
        hoverAnimate(350, 425, 140, 40, 'Customization')

        # Updating display
        pygame.display.update()

# This function was designed by both Ronil and Darun. Darun made the first version, which was improved and re-made by Ronil for the current version.


def restart(userStats, prestigelevel, items, powerChosen):
    """
        Function that allows the user to prestige their level and increase thier progress in the game. They lose all thier money and powerups when thiy prestige
        Args:
            # points, highscore, etc...
            userStats: A list of ints of the user's stats. This includes
            prestigeleve: A list of ints of what their current prestige level is, and how much it'll cost for the next prestige level.
            items: A list of ints which store how much of each powerup type the user currently contains. In this method, each index will be reset to 0
        Returns:
            None: Returns nothing, leading to the Homepage
            "w": A string which leads to the win page
    """
    # Making a while true loop
    restart = True
    # global userStats
    # global prestigelevel
    # global items
    while restart:

        # Adding a colour to the background of the screen
        display.fill((255, 215, 0))
        header_text = font(120).render("Prestige", True, (0, 64, 255))
        info3_text = font(25).render(
            "Please confirm that you want to prestige. (You will lose ALL coins & powerups)", True, (0, 0, 0))
        info4_text = font(25).render(
            "If you prestige, you will be on the next level", True, (0, 0, 0))
        info5_text = font(25).render(
            "Current Prestige Level: Level " + str(prestigelevel[0]), True, (0, 0, 0))
        info6_text = font(25).render("Prestige cost: " +
                                     str(prestigelevel[1]) + " points", True, (0, 0, 0))

        # Blitting items to the screen
        # Displaying the different texts on the screen
        display.blit(header_text, (200, 25))
        display.blit(info3_text, (25, 225))
        display.blit(info4_text, (175, 275))
        display.blit(info5_text, (225, 325))
        display.blit(info6_text, (250, 375))

        text = font(35).render('Prestige Level', True, (255, 255, 255))
        text2 = font(35).render('Cancel', True, (255, 255, 255))

        # going into the pygame loop
        for event in pygame.event.get():
            # If the user exits the page
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # If the user is moving thier mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Checking if the mouse clicked the prestige button
                if 150 <= mouse[0] <= 290 and 450 <= mouse[1] <= 490:
                    # This chekcs if they can afford prestiging
                    if userStats[0] >= prestigelevel[1]:
                        # They lose all thier money
                        userStats[0] = 0
                        # increase in level
                        prestigelevel[0] += 1
                        # The cost of the next prestige level is reset
                        prestigelevel[1] = int(prestigelevel[1] * 1.2)
                        # reseting all of thier powerups
                        for i in range(3):
                            items[i] = 0
                            powerChosen[i] = -1
                        # If they haven't completed the game yet
                        if prestigelevel[0] != 5:
                            labelCode("Level Prestiged!")
                            pygame.display.update()
                            time.sleep(1)
                        # When they complete the game it will redirect them to the win page
                        else:
                            return "w"
                    else:
                        # This is what happens when they do not have enough points to afford prestiging
                        labelCode("Not Enough Points")
                        pygame.display.update()
                        time.sleep(1)
                    return
                # checking if the mouse clicked the cancel button
                if 410 <= mouse[0] <= 550 and 450 <= mouse[1] <= 490:
                    # not chaning userstats
                    return

        # getting the exact position of the mouse
        mouse = pygame.mouse.get_pos()

        # Displaying buttons
        hoverAnimate(150, 450, 140, 40, 'Prestige')
        hoverAnimate(410, 450, 140, 40, 'Cancel')

        # updating the screen
        pygame.display.update()

# The information that would go in this section was made by both Darun and Ronil. Ronil was the one who made and designed the page


def Instructions():
    """
        Simple Instructions page for the user, telling them what the game is about, how to play, any problems
        Args:
            N/A
        Returns:
            None: None will lead the user back to the homepage
    """
    # this is the dimensions for the homeImg at the start
    questionDimension = 50
    # This is the different colours
    while True:
        # This is to create the initial displays
        # Here i am making the background green
        display.fill((3, 252, 248))

        # X image to return to Homepage. Initialized in while loop as needs to update size
        homeImg = pygame.transform.scale(pygame.image.load(
            'Images/homeImg.png'), (questionDimension, questionDimension))

        # Here we are initializing all of the text going onto the page
        # Header Text
        title_text = font(60).render(
            "Instructions", True, (0, 0, 0))
        # Body Text with all of the rules
        info1_text = font(20).render(
            "- Using you hand, move the car across the road to dodge the incomming traffic", True, (0, 0, 0))
        info2_text = font(20).render(
            "- The farther you go, the faster the incomming cars will be", True, (0, 0, 0))
        info3_text = font(20).render(
            "- Try and collect coins to increase your score", True, (0, 0, 0))
        info4_text = font(20).render(
            "- Once you die, your money will be added to your wallet as currency", True, (0, 0, 0))
        info5_text = font(20).render(
            "- Spend money to buy powerups and prestige levels", True, ((0, 0, 0)))
        info7_text = font(20).render(
            "- If device doesn't switch to camera, it isn't being recognized", True, (0, 0, 0))
        info8_text = font(20).render(
            "- Coins matter towards your score, but longer survival means more points", True, (0, 0, 0))
        info10_text = font(20).render(
            "- If a white rectangle appears & a text saying to not teleport, bring your hand to where the rectangle is", True, (0, 0, 0))
        info6_text = font(50).render(
            "How long can you last?", True, (0, 0, 0))
        info9_text = font(50).render(
            "PLAY NOW", True, (0, 0, 0))
        # This is where all of the text is being displayed onto the screen
        display.blit(title_text, (225, 30))
        display.blit(info1_text, (25, 100))
        display.blit(info2_text, (25, 150))
        display.blit(info3_text, (25, 200))
        display.blit(info4_text, (25, 250))
        display.blit(info5_text, (25, 300))
        display.blit(info7_text, (25, 350))
        display.blit(info8_text, (25, 400))
        display.blit(info10_text, (25, 450))
        display.blit(info6_text, (150, 475))
        display.blit(info9_text, (250, 525))

        # Getting Mouse
        mouse = pygame.mouse.get_pos()  # Mouse object

        # Animating when hover over questionmark
        if 600 <= mouse[0] <= 650 and 25 <= mouse[1] <= 75:
            # when the mmouse hovers over it, the size of the image increases
            questionDimension = 75
        else:
            # When the mouse isn't hovering over it, it stays the same
            questionDimension = 50

        # Blitting image to screen
        display.blit(homeImg, homeImg.get_rect(center=(625, 50)))

        # Checking for pygame events
        for event in pygame.event.get():
            # Checks if the user exited the tab
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # Checks if the user clicked the button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 600 <= mouse[0] <= 650 and 25 <= mouse[1] <= 75:
                    return None

        # Updating display
        pygame.display.update()

# Page to show hand tracking (ball moving across the screen)

# This function was planned by Ronil and executed by Darun who wrote the code


def handCheck(listy):
    """
        Function to Show general hand tracking for the user (Dots would represent their hand)
        Args:
            listy: A list of pygame images which stores the car images. Will be used to display the correct car image (color)
        Returns:
            None: Nonetype is associated with the homepage function
    """

    # Looping until user returns to homepage
    otherDevice = "Car"
    while True:

        # Filling the screen (255,255,255)
        display.fill((255, 255, 255))

        # Variables needed for hand recognition
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        landmarks = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [
            0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        averages = [0, 0]
        # Printing the hand points
        if results.multi_hand_landmarks:  # Checking if hand is recognized

            # Variables needed to create picture of hand
            i = 0

            # Getting each hand landmark (each joint of finger is a different landmark)
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    # Getting x and y coordinates
                    cx, cy = int(lm.x * w), int(lm.y*h)
                    # Drawing the circle for the joint
                    i += 1  # Increasing iteration count
                    if otherDevice == "Car":
                        pygame.draw.circle(
                            display, ((245, 0, 0)), (600-cx+30, cy), 5)
                        # Storing the coordinates of joint
                        landmarks[i-1] = [630-cx, cy]
                        if i != 1 and i != 6 and i != 10 and i != 14 and i != 18:  # Drawing the line IF it is needed
                            pygame.draw.line(
                                display, ((245, 0, 0)), (landmarks[i-2][0], landmarks[i-2][1]), (600-cx+30, cy), 5)
                    else:
                        averages[0] += cx
                        averages[1] += cy
        if otherDevice == "Car":
            # Drawing 5 of the lines manually. This is so that it is clear to the user about how the hand exactly looks
            pygame.draw.line(display, ((
                245, 0, 0)), (landmarks[2][0], landmarks[2][1]), (landmarks[5][0], landmarks[5][1]), 5)
            pygame.draw.line(display, ((
                245, 0, 0)), (landmarks[5][0], landmarks[5][1]), (landmarks[9][0], landmarks[9][1]), 5)
            pygame.draw.line(display, ((
                245, 0, 0)), (landmarks[9][0], landmarks[9][1]), (landmarks[13][0], landmarks[13][1]), 5)
            pygame.draw.line(display, ((
                245, 0, 0)), (landmarks[13][0], landmarks[13][1]), (landmarks[17][0], landmarks[17][1]), 5)
            pygame.draw.line(display, ((
                245, 0, 0)), (landmarks[17][0], landmarks[17][1]), (landmarks[0][0], landmarks[0][1]), 5)
        else:
            averages[0] /= 21
            averages[1] /= 21
            display.blit(listy[0], (630-averages[0], averages[1]))
        # Pygame events
        for event in pygame.event.get():
            # IF user quits
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # If user clicks the button
            if event.type == pygame.MOUSEBUTTONDOWN:  # Checks if mouse was clicked
                mouse = pygame.mouse.get_pos()
                # If user clicked return to homepage button, return home
                if 10 <= mouse[0] <= 150 and 550 <= mouse[1] <= 590:
                    return
                elif 500 <= mouse[0] <= 640 and 550 <= mouse[1] <= 590:
                    if otherDevice == "Car":
                        otherDevice = "Hand"
                    else:
                        otherDevice = "Car"

        # Items to display other than hand joints
        hoverAnimate(10, 550, 140, 40, "Return to Homepage")
        hoverAnimate(500, 550, 140, 40, otherDevice + " View")
        display.blit(font(20).render(
            "Each dot represents a keypoint on your hand", True, (0, 0, 0)), (10, 10, 140, 40))

        # Update screen
        pygame.display.update()

# This section was planned by both, but Ronil was the one who made the code for this section.


def customization(listy):
    """
        Function for the customizations page, where the user gets to customize their vehicle colour
        Args:
            listy: A list of pygame images, used to customize the color of the car (index 0 is the car that will be used)
        Returns:
            None: Nonetype is associated with the homepage function
    """
    i = 0
    while True:
        # This is initializing all of the font, background and text
        font = pygame.font.Font('freesansbold.ttf', 40)
        # Setting background colour
        display.fill((98, 200, 255))
        title_text = font.render("Car Garage", True, (155, 155, 155))
        info1_text = font.render("Change Car Colour", True, (0, 0, 0))
        # Displaying the text
        display.blit(title_text, (225, 30))
        display.blit(info1_text, (150, 150))
        # initilaizing text for the buttons

        for event in pygame.event.get():
            # If the user quits the game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # If the user clicks the button
            if event.type == pygame.MOUSEBUTTONDOWN:
                # This is to ensure that the car colour options will loop.
                # This is the right button for the car carousel
                if 425 <= mouse[0] <= 475 and 275 <= mouse[1] <= 325:
                    i = (i+1) % len(listy)
                # This is the left button for the car carousel
                elif 225 <= mouse[0] <= 275 and 275 <= mouse[1] <= 325:
                    i = (i-1) % len(listy)
                # This is return back to the main menu
                elif 50 <= mouse[0] <= 190 and 550 <= mouse[1] <= 590:
                    listy.insert(0, listy.pop(i))
                    return None

        mouse = pygame.mouse.get_pos()
        # This draws the triangular carousel buttons
        # this draws the left triangle
        pygame.draw.polygon(display, (255, 255, 255), points=[
            (275, 275), (275, 325), (225, 300)])
        # This draws the right triangle
        pygame.draw.polygon(display, (255, 255, 255), points=[
                            (425, 275), (425, 325), (475, 300)])
        # This displayes the car images
        display.blit(listy[i], (310, 260))
        # This changes the colour of the buttons if the mouse hovers over them
        if 425 <= mouse[0] <= 475 and 275 <= mouse[1] <= 325:
            pygame.draw.polygon(display, (255, 165, 0), points=[
                                (425, 275), (425, 325), (475, 300)])
        elif 225 <= mouse[0] <= 275 and 275 <= mouse[1] <= 325:
            pygame.draw.polygon(display, (255, 165, 0), points=[
                                (275, 275), (275, 325), (225, 300)])
        # This animates the home button
        hoverAnimate(50, 550, 140, 40, "Home")
        # Updates the display
        pygame.display.update()

# This section both worked on/designed, but Ronil was the one who made the code for this section


def upgrades(items, powerupImages, userStats, powerChosen):
    """
        Function for the upgrades page, where the user gets to buy different powerups
        Args:
            items: A list of integers which stores the quantity of each power a user contains. Each index stores a different powerups
            powerupImages: A list of pygame images to store the images of each power
            userStats: A list integers containing the user's points and highscore
            powerChosen: A list of integers containing which power the user chose. -1 represents not chosen, 1 represents chosen
        Returns:
            None: Nonetype is associated with the homepage function
            "g": A string which brings the user to the game function
    """
    # Variables
    powerup_costs = [200, 300, 400]
    questionDimension = 50

    # Blank variable
    i = 0
    while True:
        questionImg = pygame.transform.scale(pygame.image.load(
            'Images/info.png'), (questionDimension, questionDimension))
        # this makes the background blue
        display.fill((76, 230, 70))
        # This is the header font
        title_text = font(60).render("Upgrades", True, (0, 0, 0))
        # This is the sub heading font
        info1_text = font(50).render("Buy Powerups", True, (0, 0, 0))
        # This is the main text font
        info3_text = font(35).render(
            "Cost: " + str(powerup_costs[0]) + " points", True, (0, 0, 0))
        info13_text = font(15).render(
            "*Click on a powerup to select it", True, (0, 0, 0))
        info4_text = font(35).render(
            "Cost: " + str(powerup_costs[1]) + " points", True, (0, 0, 0))
        info5_text = font(35).render(
            "Cost: " + str(powerup_costs[2]) + " points", True, (0, 0, 0))
        info7_text = font(35).render("Double Score", True, (0, 0, 0))
        info8_text = font(35).render("Double Coins", True, (0, 0, 0))
        info9_text = font(35).render("Double Lives", True, (0, 0, 0))
        # This text is the number of powerups the player currently has
        info10_text = font(35).render(str(items[0]), True, (0, 0, 0))
        info11_text = font(35).render(str(items[1]), True, (0, 0, 0))
        info12_text = font(35).render(str(items[2]), True, (0, 0, 0))

        # Displaying all of the font that was initialized above
        display.blit(title_text, (250, 30))
        display.blit(info1_text, (225, 100))
        display.blit(info3_text, (50, 175))
        display.blit(info4_text, (265, 175))
        display.blit(info5_text, (480, 175))
        display.blit(info7_text, (80, 225))
        display.blit(info8_text, (280, 225))
        display.blit(info9_text, (480, 225))
        display.blit(info13_text, (500, 100))

        # Getting mouse location
        mouse = pygame.mouse.get_pos()

        # Checking for pygame events
        for event in pygame.event.get():
            # This is if the user wants to leave the game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # This is if the user clicks on of the buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                # This is if they click the button to buy the third power up
                if 520 <= mouse[0] <= 570 and 415 <= mouse[1] <= 455:
                    # Checks if they have enough to buy the powerup
                    if userStats[0] >= powerup_costs[2]:
                        # if they have enough it procedes to buy it
                        userStats[0] -= powerup_costs[2]
                        items[2] += 1
                    else:
                        # If they don't have enough it gives the error message
                        labelCode("Not Enough Points")
                        pygame.display.update()
                        time.sleep(1)
                # This is if they click the button to buy the second power up
                elif 320 <= mouse[0] <= 370 and 415 <= mouse[1] <= 455:
                    # Checks if they have enough to buy the powerup
                    if userStats[0] >= powerup_costs[1]:
                        # if they have enough it procedes to buy it
                        userStats[0] -= powerup_costs[1]
                        items[1] += 1
                    else:
                        # If they don't have enough it gives the error message
                        labelCode("Not Enough Points")
                        pygame.display.update()
                        time.sleep(1)
                # This is if they click the button to buy the first power up
                elif 120 <= mouse[0] <= 170 and 415 <= mouse[1] <= 455:
                    # Checks if they have enough to buy the powerup
                    if userStats[0] >= powerup_costs[0]:
                        # if they have enough it procedes to buy it
                        userStats[0] -= powerup_costs[0]
                        items[0] += 1
                    else:
                        # If they don't have enough it gives the error message
                        labelCode("Not Enough Points")
                        pygame.display.update()
                        time.sleep(1)
                # This is if they click the button to go back home
                elif 100 <= mouse[0] <= 200 and 550 <= mouse[1] <= 590:
                    return None
                # This is if they click the button to continue to game
                elif 500 <= mouse[0] <= 600 and 550 <= mouse[1] <= 590:
                    return "g"
                # This is if the user clicks the button to use the double score powerup
                elif 80 <= mouse[0] <= 180 and 300 <= mouse[1] <= 400:
                    # Checks if they clicked on the powerup to activate it
                    if items[0] > 0 or powerChosen[0] == 1:
                        # This makes a white background behind the powerup
                        powerChosen[0] *= -1
                        items[0] -= powerChosen[0]
                # This is if the user clicks the button to use the double coins powerup
                elif 280 <= mouse[0] <= 380 and 300 <= mouse[1] <= 400:
                    # Checks if they clicked on the powerup to activate it
                    if items[1] > 0 or powerChosen[1] == 1:
                        # This makes a white background behind the powerup
                        powerChosen[1] *= -1
                        items[1] -= powerChosen[1]
                # This is if the user clicks the button to use the double life powerup
                elif 480 <= mouse[0] <= 580 and 300 <= mouse[1] <= 400:
                    # Checks if they clicked on the powerup to activate it
                    if items[2] > 0 or powerChosen[2] == 1:
                        # This makes a white background behind the powerup
                        powerChosen[2] *= -1
                        items[2] -= powerChosen[2]
                # This checks if the user want to go to the powerups information page
                elif 25 <= mouse[0] <= 75 and 25 <= mouse[1] <= 75:
                    return "p"

        # this makes the information image become bigger if its hovered over
        if 25 <= mouse[0] <= 75 and 25 <= mouse[1] <= 75:
            questionDimension = 75
        else:
            questionDimension = 50
        # If the user wants to use the powerup, it highlights the powerup
        # This is for the double points powerup
        if powerChosen[0] == 1:
            pygame.draw.rect(display, (255, 255, 255), [109, 274, 102, 102])
        # This is for the double coints powerup
        if powerChosen[1] == 1:
            pygame.draw.rect(display, (255, 255, 255), [309, 274, 102, 102])
        # This is for the double life powerup
        if powerChosen[2] == 1:
            pygame.draw.rect(display, (255, 255, 255), [509, 274, 102, 102])
        # This prints the different powerup images
        display.blit(powerupImages[0], (110, 275))
        display.blit(powerupImages[1], (310, 275))
        display.blit(powerupImages[2], (510, 275))
        display.blit(questionImg, questionImg.get_rect(center=(50, 50)))
        # This animates the buy button whenever the mouse hovers over them
        hoverAnimate(120, 425, 50, 40, "Buy")
        hoverAnimate(320, 425, 50, 40, "Buy")
        hoverAnimate(520, 425, 50, 40, "Buy")
        # This prints the rectangle for the number of powerups the user has
        pygame.draw.rect(display, (255, 255, 255), [
                         207, 416, 15+(len(str(items[0])))*10, 20])
        pygame.draw.rect(display, (255, 255, 255), [
                         407, 416, 15+(len(str(items[1])))*10, 20])
        pygame.draw.rect(display, (255, 255, 255), [
                         607, 416, 15+(len(str(items[2])))*10, 20])
        # This prints out all of the text
        display.blit(info10_text, (210, 415))
        display.blit(info11_text, (410, 415))
        display.blit(info12_text, (610, 415))

        display.blit(info7_text, (80, 225))
        display.blit(info8_text, (280, 225))
        display.blit(info9_text, (480, 225))

        # this displays thier points
        display.blit(font(40).render(
            "Points:"+str(userStats[0]), True, (255, 255, 255)), (500, 50))
        # Animates the enter game and main menu buttons
        hoverAnimate(500, 550, 100, 40, "Enter Game")
        hoverAnimate(100, 550, 100, 40, "Main Menu")
        # updates the screen
        pygame.display.update()

# this page was designed and made by Ronil, Darun made some tweaks/functionalities


def powerups():
    """
        Simple Powerups information page for the user, telling them what each powerup is
        Args:
            N/A
        Returns:
            "u": A string which will direct the user to the upgrades page
    """
    questionDimension = 50
    # This is the different colours
    while True:
        # This is to create the initial displays
        # Here i am making the background green
        display.fill((0, 255, 0))

        # X image to return to Homepage. Initialized in while loop as needs to update size
        homeImg = pygame.transform.scale(pygame.image.load(
            'Images/back.png'), (questionDimension, questionDimension))
        # Here we are initializing all of the text going onto the page
        # Header Text
        title_text = font(60).render(
            "Powerup Information", True, (0, 0, 0))
        # Body Text with all the descriptions
        info1_text = font(30).render(
            "Double Score", True, (0, 0, 0))
        info2_text = font(22).render(
            "During the round, your score doubles(spawn rate still stays the same)", True, (0, 0, 0))
        info3_text = font(22).render(
            "Exp. If you would usually get 400 points for last 20 seconds, you would get 800 points", True, (0, 0, 0))
        info4_text = font(30).render(
            "Double Coins", True, (0, 0, 0))
        info5_text = font(22).render(
            "During the round, the number of coins collected will double", True, (0, 0, 0))
        info6_text = font(22).render(
            "Exp. If you collect 4 coins before you die, it will become 8 coins", True, (0, 0, 0))
        info7_text = font(30).render(
            "Double Lives", True, (0, 0, 0))
        info8_text = font(22).render(
            "This gives you two lives, so you need to get hit by two incoming cars before you die", True, (0, 0, 0))
        info9_text = font(22).render(
            "If you go off the road you still die", True, ((0, 0, 0)))
        # This is where the images of the powerups are being displayed onto the screen
        display.blit(powerupImages[0], (175, 100))
        display.blit(powerupImages[1], (175, 245))
        display.blit(powerupImages[2], (175, 400))

        # This is where all of the text is being displayed onto the screen
        display.blit(title_text, (160, 30))
        display.blit(info1_text, (25, 150))
        display.blit(info2_text, (25, 200))
        display.blit(info3_text, (25, 225))
        display.blit(info4_text, (25, 300))
        display.blit(info5_text, (25, 350))
        display.blit(info6_text, (25, 375))
        display.blit(info7_text, (25, 450))
        display.blit(info8_text, (25, 500))
        display.blit(info9_text, (25, 525))

        # Getting Mouse
        mouse = pygame.mouse.get_pos()  # Mouse object

        # Animating when hover over questionmark
        if 25 <= mouse[0] <= 75 and 25 <= mouse[1] <= 75:
            questionDimension = 75
        else:
            questionDimension = 50

        # Blitting image to screen
        display.blit(homeImg, homeImg.get_rect(center=(50, 50)))

        # Checking for pygame events
        for event in pygame.event.get():
            # Checks if the user exited the tab
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # Checks if the user clicked the button
            if event.type == pygame.MOUSEBUTTONDOWN:
                # This is if they wnat to return back to the upgrades page
                if 12.5 <= mouse[0] <= 87.5 and 12.5 <= mouse[1] <= 87.5:
                    return "u"

        # Updating display
        pygame.display.update()

# This function was designed and written by Darun


def gameWon():
    """
        Function to be called when the user has won the game
        Args:
            N/A
        Returns:
            None: Nontype which will direct the user to the Homepage
            "q": A string which will lead to a selection which will break the while loop, causing the code to end
    """
    while True:
        # this is making the background
        display.fill((255, 155, 0))
        # This is initializing all the text
        display.blit(font(40).render(
            "Congrats, you won the game!", True, (0, 0, 0)), (30, 30))
        display.blit(font(30).render(
            "If you wish to exit the game, click the button on the bottom left", True, (0, 0, 0)), (30, 80))
        display.blit(font(30).render(
            "If not, you can continue on, but you will be able to quit anytime", True, (0, 0, 0)), (30, 130))

        mouse = pygame.mouse.get_pos()

        # Checking for pygame events
        for event in pygame.event.get():
            # This is if the user wants to leave the game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # This is if they click the quit button
                if 30 <= mouse[0] <= 130 and 550 <= mouse[1] <= 590:
                    return "q"
                # this is if they click the continue button
                elif 550 <= mouse[0] <= 690 and 550 <= mouse[1] <= 590:
                    return
        # This annimates the quit and continue buttons
        hoverAnimate(30, 550, 100, 40, "Quit Game")
        hoverAnimate(550, 550, 140, 40, "Continue Onwards")
        # This updates the screen
        pygame.display.update()


# Main code, simply calling the main function (homepage), iterating through a while loop until you quit code then quitting the code if you ever exit it
choice = None
while True:
    # This sends them to the handbeck page
    if choice == "h":
        choice = handCheck(listy)
    # This sends them to the restart page
    elif choice == "r":
        choice = restart(userStats, prestigelevel, items, powerChosen)
    # This sends them to the instructions page
    elif choice == "i":
        choice = Instructions()
    # This sends them to the game page
    elif choice == "g":
        choice = game(keyboardOrCamera, listy, powerChosen)
    # This sends them to the home page
    elif choice == None:
        choice, keyboardOrCamera = homepage(
            userStats, keyboardOrCamera, prestigelevel)
    # This sends them to the custimization page
    elif choice == "c":
        choice = customization(listy)
    # This sends them to the upgrades page
    elif choice == "u":
        choice = upgrades(items, powerupImages, userStats, powerChosen)
    # This sends them to the gameWon page
    elif choice == "w":
        choice = gameWon()
    # This sends them to the powerups information page
    elif choice == "p":
        choice = powerups()
    # This quits the pygames
    elif choice == "q":
        break

# Ronil and Darun worked together on most of the code when debugging, but initially when writing the different sections the work was split up between the two.
# In class, a lot of the work was done together throguh constant discussions between the two as they helped eachother develop the code
