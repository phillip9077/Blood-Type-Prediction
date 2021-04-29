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
The accuracy of the saved model in this repo is 96.5%, but that is definitely due to overfitting and the lack of samples in my self-curated dataset. There is a possibility that if you try to train the model yourself the accuracy would be nowhere near 96.5%; Again, this is because the lack of samples and can only be corrected through acquiring a larger dataset. Additionally, the ANN is most likely not optimized, but there are several paths one could take to improve it:
  1. Stochastic Gradient Descent (SGD) is not the most efficient optimizer for the ANN, so an alternative one such as Adam or RMSprop could potentially reduce training times.
  2. As the dataset I used was curated by yours truly, it does not significantly indicate that the ANN has "learned" to predict blood types. This means, assuming a 
  proper dataset is used, the hyperparameters can definitely be altered to maximize the ANN efficiency.
  
Lastly, I want to add that this ANN is by no means accurate in terms of how blood type genetics actually works. The intended audience of this ANN is middle school students, so I
made the decision to simplify the concept by excluding proper genetics (A, B, O, and Rh alleles). Therefore, there are certain parts to the program that might make a biologist cringe a little bit, and I apologize. 
