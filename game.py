import numpy as np
import pygame
from tensorflow import keras

# Initializing Pygame and setting the dimensions of the main window
pygame.init()
win = pygame.display.set_mode((800, 500))
pygame.display.set_caption('Blood Type Prediction Game')

# Various variables we need to run the game such as the Pygame clock. images, text, etc.
clock = pygame.time.Clock()
RBC_right = pygame.image.load('images/RBC_right.png').convert()
chat = pygame.image.load('images/chat.png').convert()
text_font = pygame.font.SysFont('Trebuchet MS', 20)
caption_font = pygame.font.SysFont('Trebuchet MS', 14)
type_font = pygame.font.SysFont('Trebuchet MS', 80)
text1 = text_font.render('Please enter the first blood type!', True, (0, 0, 0))
text2 = text_font.render('Please enter the second blood type!', True, (0, 0, 0))
result_text = text_font.render('These are your inputted blood types!', True, (0, 0, 0))
legend = caption_font.render('A for type A, B for type B, O for type O', True, (0, 0, 0))
blood_type_count = 0
first_type = ''
second_type = ''
RBC_xPos = 80
RBC_yPos = 80
RBC_vel = 10
isBloodInputted = False
isMovementDone = False
isRightEnd = False
model_predicted = False
isRestart = False

blood_types = {'A+': [1, 0, 0, 0, 0, 0, 0, 0],
               'A-': [0, 1, 0, 0, 0, 0, 0, 0],
               'B+': [0, 0, 1, 0, 0, 0, 0, 0],
               'B-': [0, 0, 0, 1, 0, 0, 0, 0],
               'AB+': [0, 0, 0, 0, 1, 0, 0, 0],
               'AB-': [0, 0, 0, 0, 0, 1, 0, 0],
               'O+': [0, 0, 0, 0, 0, 0, 1, 0],
               'O-': [0, 0, 0, 0, 0, 0, 0, 1]}
model = keras.models.load_model('C:/VIA Tech/Blood Type Prediction')
prediction_dict = {}


# Method to return either the blood type A, B, or O from keyboard input
def assign_blood_type(e):
    blood_type = ''
    if e.key == pygame.K_a:
        blood_type = pygame.key.name(pygame.K_a).capitalize()
    elif e.key == pygame.K_b:
        blood_type = pygame.key.name(pygame.K_b).capitalize()
    elif e.key == pygame.K_o:
        blood_type = pygame.key.name(pygame.K_o).capitalize()
    return blood_type


# Method to turn the ANN output probability matrix into a probability dictionary, with each
# blood type as a key and its respective probability as the key's value
def prob_array_to_dict(arr):
    prob_dict = {}
    index = 0
    for key in blood_types.keys():
        prob_dict[key] = arr[index]
        index += 1
    return prob_dict


# draw some text into an area of a surface automatically wraps words returns any text that didn't
# get blitted
def drawWrappedText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text


# Running the Pygame application
while True:
    clock.tick(60)

    win.fill((255, 255, 255))
    win.blit(RBC_right, (RBC_xPos, RBC_yPos))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN and blood_type_count < 2:
            if blood_type_count == 0:
                first_type = assign_blood_type(event)
            elif blood_type_count == 1:
                second_type = assign_blood_type(event)
            blood_type_count += 1
        # allows user to restart prediction once restart button is pressed
        if event.type == pygame.MOUSEBUTTONDOWN and restartButton is not None:
            pos = pygame.mouse.get_pos()
            if not isRestart and restartButton.collidepoint(pos):
                isRestart = True

    if not isBloodInputted:
        # Display corresponding text for inputting first blood type
        if blood_type_count == 0:
            win.blit(chat, (250, 5))
            win.blit(text1, (380, 35))
            win.blit(legend, (400, 70))

        # Display corresponding text for inputting second blood type
        elif blood_type_count == 1:
            win.blit(chat, (250, 5))
            win.blit(text2, (360, 35))
            win.blit(legend, (400, 70))
            first_type_surface = type_font.render(first_type + " + ", True, (255, 0, 0))
            win.blit(first_type_surface, (410, 250))

        else:
            win.blit(chat, (250, 5))
            win.blit(result_text, (360, 50))
            second_type_surface = type_font.render(second_type, True, (255, 0, 0))
            win.blit(first_type_surface, (410, 250))
            win.blit(second_type_surface, (540, 250))

    # Once the two blood types have been inputted, display an animation of sorts
    # to indicate that the AI is working its magic
    else:
        if RBC_xPos < 600 and not isRightEnd:
            RBC_xPos += RBC_vel
            if RBC_xPos == 600:
                isRightEnd = True
                pygame.time.delay(800)
        elif RBC_xPos > 70:
            RBC_xPos -= RBC_vel
        elif RBC_yPos < 150:
            RBC_yPos += RBC_vel
            if RBC_yPos == 150:
                isMovementDone = True

    # Use the inputted blood types to run through the ANN and display its predictions
    if first_type != '' and second_type != '' and isMovementDone:
        if not model_predicted:
            type_one_plus = first_type + "+"
            type_two_plus = second_type + "+"
            type_one_minus = first_type + "-"
            type_two_minus = second_type + "-"
            prediction_plus = model.predict([blood_types[type_one_plus]
                                             + blood_types[type_two_plus]])[0]
            prediction_minus = model.predict([blood_types[type_one_minus]
                                              + blood_types[type_two_minus]])[0]
            prediction = []
            for i, val in np.ndenumerate(prediction_plus):
                prediction.append((val + prediction_minus[i]) / 2)
            temp = prob_array_to_dict(prediction)
            sorted_keys = sorted(temp, key=temp.get, reverse=True)
            for k in sorted_keys:
                prediction_dict[k] = temp[k]
            model_predicted = True
        else:
            win.blit(text_font.render('Here are the predictions!!', True, (0, 0, 0)), (370, 30))
            # sorting the probabilities from high to low + rounding the numbers
            temp_yPos = 80
            for k in prediction_dict.keys():
                win.blit(text_font.render(k + ': ' + str(round(prediction_dict[k], 7)), True,
                                          (0, 0, 0)),
                         (420, temp_yPos))
                temp_yPos += 50
            # quick description of what the probabilities mean
            captionBox = pygame.Rect(50, 380, 200, 100)
            caption = 'These numbers represent the probability of your blood type given your ' \
                      'parents blood types!'
            drawWrappedText(win, caption, (0, 0, 0), captionBox, caption_font, aa=True)
            # draw out a restart button
            restartButton = pygame.Rect(700, 450, 100, 50)
            pygame.draw.rect(win, (250, 135, 135), restartButton, border_top_left_radius=25)
            win.blit(caption_font.render('Restart?', True, (0, 0, 0)), (727, 467))

    pygame.display.update()

    # Update the screen one last time once the two blood types are inputted to show the inputs
    # to the user. Once this happens, the animation should then continue to display the predictions.
    if first_type != '' and second_type != '' and not isBloodInputted:
        isBloodInputted = True
        pygame.time.delay(1200)

    # If the user clicks the restart button, all the necessary boolean values need to be reset,
    # including the isRestart value itself.
    if isRestart:
        prediction_dict = {}
        blood_type_count = 0
        first_type = ''
        second_type = ''
        RBC_xPos = 80
        RBC_yPos = 80
        isBloodInputted = False
        isMovementDone = False
        isRightEnd = False
        model_predicted = False
        isRestart = False

