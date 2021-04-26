# Blood-Type-Prediction
A simple Artificial Neural Network (ANN) using Tensorflow and Keras to predict possible offspring blood types by inputting parent blood types

# Usage
Once the program is run, input two blood types (doesn't have to be your parents', of course) and see the ANN output the probabilities of your potential blood type! Since not everyone
knows whether their blood is + or -, I've excluded the need to have to enter + or - in the inputs. 

# Reflection
Most of the code to train the neural network has been commented out as the process takes about ~5-7 minutes; to save time
as I was testing the model I just saved my model (the .pb file in this repo) and loaded that every time I ran the program. The ANN is most likely not optimized, but there are 
several paths one could take to improve it:
  1. Stochastic Gradient Descent (SGD) probably is not the most efficient optimizer for the ANN, so an alternative one such as Adam or RMSprop could potentially reduce training times
  2. As the dataset I used was curated by yours truly, it is not large enough to significantly indicate that the ANN has "learned" to predict blood types. This means, assuming a 
  proper dataset is used, the hyperparameters can definitely be altered to ensure the highest possible accuracy with this ANN.
  
Lastly, I want to add that this ANN is by no means accurate in terms of how blood type genetics actually works. The intended audience of this ANN is middle school students, so I
made the decision to simplify the concept by excluding genetics (A, B, O, and Rh alleles). Therefore, there are certain parts to the program that might make a biologist cringe a
little bit, and I apologize. 
