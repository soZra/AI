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
    probabilities = []      # a list of Dicts,   每个字典含有不同word及其对应可能性(根据当前id即当前测试id为该'word的概率’)
    guesses = []            # a list of 'word'
    # TODO implement the recognizer
    # return probabilities, guesses
        
    for word_id in test_set._data:      # 对于test_set中的每个word_id，
        prob = {}                   # 存所有'word'的score/logl
        best_score = float('-inf')  # 可能性最大的'word'对应的score,根据score来选word
        best_guess = ''             # 存当前word_id最有可能的'word'
        
    

        for word, model in models.items():         #每个word遍历所有model寻找概率最高的一个，即为最可能的'word'
            try:
                
                X_thisWord, lengths_thisWord = test_set.get_item_Xlengths(word_id)  # 取遍历中的'word'的sample和features数据
                logl_thisWord = model.score(X_thisWord, lengths_thisWord)   # 是当前model/'word'的可能性
                if logl_thisWord > best_score:              # 概率更高则存进best_score，目前'word’便为当前最可能'word'
                    best_score = logl_thisWord
                    best_guess = word
                
                
            except:
                prob[word] = 0      # 出错就随便加点东西进去，继续遍历
                continue
            prob[word] = logl_thisWord


        probabilities.append(prob)
        guesses.append(best_guess)

    return probabilities, guesses