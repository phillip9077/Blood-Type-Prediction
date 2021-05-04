# Blood-Type-Prediction
A simple Artificial Neural Network (ANN) using Tensorflow and Keras to predict possible offspring blood types by inputting parent blood types.

# Usage
There are two Python files in this repository: training.py and game.py. Training.py contains the ANN architecture as well as a short text output to test the trained model. Game.py contains a small Pygame-based game I developed to make this project more interesting for middle school students.

Both files can be run via whatever terminal interface you use,
```
/ python training.py
/ python main.py
```
or though an IDE if you have one installed.

# Reflection
The accuracy of the saved model in this repo is ~~96.5%, but that is definitely due to overfitting and the lack of samples in my self-curated dataset. There is a possibility that if you try to train the model yourself the accuracy would be nowhere near 96.5%; Again, this is because the lack of samples and can only be corrected through acquiring a larger dataset.~~ 100% after I curated a new dataset. I discovered that, despite the original accuracy of 96.5%, the actual model outputs were incorrect due to discrepancies in the original dataset. Therefore, I made a new dataset, retrained the model, and voilà: **a 100% accurate model with the expected outputs.**  Additionally, the ANN is most likely not optimized, but there are several paths one could take to improve it:
  1. ~~Stochastic Gradient Descent (SGD) is not the most efficient optimizer for the ANN, so an alternative one such as Adam or RMSprop could potentially reduce training times.~~ I have made the change from SGD to Adam, though how much faster the training occurs I have not measured. 
  2. The hyperparameters can be altered to maximize the ANN efficiency. For anyone who knows more about machine learning and AI in general than me, give this a shot!
  
Lastly, I want to add that this ANN is by no means accurate in terms of how blood type genetics actually works. The intended audience of this ANN is middle school students, so I
made the decision to simplify the concept by excluding proper genetics (A, B, O, and Rh alleles). Therefore, there are certain parts to the program that might make a biologist cringe a little bit, and I apologize. 

It would definitely be interesting to see a model developed that can accurately predict blood types based on alleles and whether the model predictions would reflect the famous Mendelian ratios as well. 
