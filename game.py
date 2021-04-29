import pygame
from tensorflow import keras
import numpy as np

pygame.init()
win = pygame.display.set_mode((800, 500))
pygame.display.set_caption('Blood Type Prediction Game')

clock = pygame.time.Clock()

RBC_right = pygame.image.load('images/RBC_right.png').convert()
chat = pygame.image.load('images/chat.png').convert()
text_font = pygame.font.SysFont('Georgia', 20)
legend_font = pygame.font.SysFont('Georgia', 14, italic=True)
text1 = text_font.render('Please enter the first blood type!', True, (0, 0, 0))
text2 = text_font.render('Please enter the second blood type!', True, (0, 0, 0))
legend = legend_font.render('A for type A, B for type B, O for type O', True, (0, 0, 0))
blood_type_count = 0
first_type = ''
second_type = ''
RBC_xPos = 80
RBC_yPos = 80
vel = 10
isRightEnd = False
isMovementDone = False

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
model_predicted = False


def assign_blood_type(e):
    blood_type = ''
    if e.key == pygame.K_a:
        blood_type = pygame.key.name(pygame.K_a).capitalize()
    elif e.key == pygame.K_b:
        blood_type = pygame.key.name(pygame.K_b).capitalize()
    elif e.key == pygame.K_o:
        blood_type = pygame.key.name(pygame.K_o).capitalize()
    return blood_type


def prob_array_to_dict(arr):
    prob_dict = {}
    index = 0
    for key in blood_types.keys():
        prob_dict[key] = arr[index]
        index += 1
    return prob_dict


run = True
while run:
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

    # display corresponding text for inputting first blood type
    if blood_type_count == 0:
        win.blit(chat, (250, 5))
        win.blit(text1, (380, 30))
        win.blit(legend, (405, 70))

    # display corresponding text for inputting second blood type
    elif blood_type_count == 1:
        win.blit(chat, (250, 5))
        win.blit(text2, (370, 30))
        win.blit(legend, (405, 70))

    # once the two blood types have been inputted, display some sort of animation of sorts
    # to indicate that the AI is working its magic
    else:
        if RBC_xPos < 600 and not isRightEnd:
            RBC_xPos += vel
            if RBC_xPos == 600:
                isRightEnd = True
                pygame.time.delay(800)
        elif RBC_xPos > 70:
            RBC_xPos -= vel
        elif RBC_yPos < 150:
            RBC_yPos += vel
            if RBC_yPos == 150:
                isMovementDone = True

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
            prediction_dict = prob_array_to_dict(prediction)
            model_predicted = True
        else:
            win.blit(text_font.render('AI predictions!!', True, (0, 0, 0)), (400, 30))
            win.blit(text_font.render('A+: ' + str(prediction_dict['A+']), True, (0, 0, 0)),
                     (350, 80))
            win.blit(text_font.render('A-: ' + str(prediction_dict['A-']), True, (0, 0, 0)),
                     (350, 130))
            win.blit(text_font.render('B+: ' + str(prediction_dict['B+']), True, (0, 0, 0)),
                     (350, 180))
            win.blit(text_font.render('B-: ' + str(prediction_dict['B-']), True, (0, 0, 0)),
                     (350, 230))
            win.blit(text_font.render('AB+: ' + str(prediction_dict['AB+']), True, (0, 0, 0)),
                     (350, 280))
            win.blit(text_font.render('AB-: ' + str(prediction_dict['AB-']), True, (0, 0, 0)),
                     (350, 330))
            win.blit(text_font.render('O+: ' + str(prediction_dict['O+']), True, (0, 0, 0)),
                     (350, 380))
            win.blit(text_font.render('O-: ' + str(prediction_dict['O-']), True, (0, 0, 0)),
                     (350, 430))

    pygame.display.update()
