import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    # TODO implement the recognizer
    # return probabilities, guesses
        
    for word_id in test_set._data:      # 对于test_set中的每个word_id，
        prob = {} 
        best_score = float('-inf')
        best_guess = ''
        
        try:
              

            for word, model in models.items():
                
                    
                X_thisWord, lengths_thisWord = test_set.get_item_Xlengths(word_id)
                logl_thisWord = model.score(X_thisWord, lengths_thisWord)
                if logl_thisWord > best_score:
                    best_score = logl_thisWord
                    best_guess = word
                
                prob[word] = logl_thisWord

        except:
             probabilities.append(prob)
             guesses.append(best_guess)
             continue

        probabilities.append(prob)
        guesses.append(best_guess)

    return probabilities, guesses