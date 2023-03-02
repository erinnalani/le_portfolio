"""This script uses basic logistic regression to predict the sentiments of tweets
This is a project for DeepLearning.AI NLP course on Coursera and features some blocks
of code given for testing written functions, indicated with "(given)". Assignment and
instructions were originally given in a Jupyter Notebook"""

import nltk
from nltk.corpus import twitter_samples
import numpy as np

import re
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer

nltk.download('twitter_samples')
nltk.download('stopwords')


def process_tweet(tweet):
    # clean tweet
    tweet2 = re.sub(r"^RT[\s]+", '', tweet)
    # remove hyperlinks
    tweet2 = re.sub(r"https?://[^\s\n\r]+", '', tweet2)
    # remove hashtags (hash sign only)
    tweet2 = re.sub(r"#", '', tweet2)
    # print(tweet2)

    # tokenize
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
    tweet_tokens = tokenizer.tokenize(tweet2)
    # print(f'Tokenized string: {tweet_tokens}')

    # remove stopwords and punctuation
    stopwords_english = stopwords.words('english')
    tweet_clean = []
    for word in tweet_tokens:
        if word not in stopwords_english and word not in string.punctuation:
            tweet_clean.append(word)
    # print(f'Clean tweet: {tweet_clean}')

    # stem
    stemmer = PorterStemmer()

    tweet_stem = []
    for word in tweet_clean:
        stem_word = stemmer.stem(word)
        tweet_stem.append(stem_word)
    # print(tweet_stem)
    return tweet_stem


def build_freqs(tweets_list, ys):
    # Convert label array to list
    yslist = np.squeeze(ys).tolist()
    freqs_dict = {}
    for y, tweet in zip(yslist, tweets_list):
        for word in process_tweet(tweet):
            pair = (word, y)
            freqs_dict[pair] = freqs_dict.get(pair, 0) + 1
    return freqs_dict


def sigmoid(z):
    # calculate the sigmoid of z
    h = 1 / (1 + np.exp(-z))
    return h


def gradientDescent(x, y, theta, alpha, num_iters):
    # get m, rows in matrix
    m = np.shape(x)[0]
    yT = np.transpose(y)
    xT = np.transpose(x)

    for i in range(0, num_iters):
        z = np.dot(x, theta)
        # get the sigmoid of z
        h = sigmoid(z)
        # calculate the cost function
        J = -1. / m * np.sum(np.dot(yT, np.log(h)) + np.dot((1 - yT), np.log(1 - h)))

        # update the weights theta
        theta = theta - (alpha / m) * (np.dot(xT, (h - y)))

    J = float(J)
    return J, theta


def extract_features(tweet, freqs, process_tweet=process_tweet):
    # process tweet into list of words
    word_list = process_tweet(tweet)
    # initialize feature vector
    x = np.zeros((1, 3))
    # bias term is set to 1
    x[0, 0] = 1

    # loop through each word in the list of words
    for word in word_list:
        if (word, 1.0) in freqs:
            # increment the word count for the positive label 1
            x[0, 1] += freqs.get((word, 1.0), -1)

        if (word, 0.0) in freqs:
            # increment the word count for the negative label 0
            x[0, 2] += freqs.get((word, 0.0), -1)

    assert (x.shape == (1, 3))
    return x


def predict_sentiment(tweet, freqs, theta):
    # extract features and store into matrix X
    x = extract_features(tweet, freqs)
    # make prediction
    y_pred = sigmoid(np.dot(x, theta))
    return y_pred


def logistic_reg(test_x, test_y, freqs, theta, predict_sentiment=predict_sentiment):
    # initialize prediction list
    y_hat = []
    for tweet in test_x:
        # get the label prediction for the tweet
        y_pred = predict_sentiment(tweet, freqs, theta)

        if y_pred > 0.5:
            # append 1.0 to the list
            y_hat.append(1.0)
        else:
            # append 0 to the list
            y_hat.append(0.0)
    # convert prediction list to array
    pred_val = np.squeeze(np.asarray(y_hat))
    Y_val = np.squeeze(test_y)
    m = np.shape(test_y)[0]
    # calc prediction accuracy
    accuracy = np.sum(pred_val == Y_val) / m
    return accuracy


if __name__ == "__main__":
    # Define data sets
    all_positive_tweets = twitter_samples.strings('positive_tweets.json')
    all_negative_tweets = twitter_samples.strings('negative_tweets.json')

    # Split data in to train & test sets
    train_pos = all_positive_tweets[:4000]
    test_pos = all_positive_tweets[4000:]
    train_neg = all_negative_tweets[:4000]
    test_neg = all_negative_tweets[4000:]

    train_x = train_pos + train_neg
    test_x = test_pos + test_neg

    # Create np label arrays
    train_y = np.append(np.ones((len(train_pos), 1)), np.zeros((len(train_neg), 1)), axis=0)
    test_y = np.append(np.ones((len(test_pos), 1)), np.zeros((len(test_neg), 1)), axis=0)
    # print("train_y.shape = " + str(train_y.shape))
    # print("test_y.shape = " + str(test_y.shape))

    # Build frequency dictionary
    freqs = build_freqs(train_x, train_y)
    # print("type(freqs) = " + str(type(freqs)))
    # print("len(freqs) = " + str(len(freqs.keys())))

    # ***DICT CHECK***(given)
    # print('This is an example of a positive tweet: \n', train_x[0])
    # print('\nThis is an example of the processed version of the tweet: \n', process_tweet(train_x[0]))

    # ***SIGMOID TEST***(given)
    # if sigmoid(0) == 0.5:
    #     print('SUCCESS!')
    # else:
    #     print('Oops!')
    #
    # if sigmoid(4.92) == 0.9927537604041685:
    #     print('CORRECT!')
    # else:
    #     print('Oops again!')

    # # ***GRADIENT DESC TEST***(given)
    # np.random.seed(1)
    # # X input is 10 x 3 with ones for the bias terms
    # tmp_X = np.append(np.ones((10, 1)), np.random.rand(10, 2) * 2000, axis=1)
    # # Y Labels are 10 x 1
    # tmp_Y = (np.random.rand(10, 1) > 0.35).astype(float)
    # # Apply gradient descent
    # tmp_J, tmp_theta = gradientDescent(tmp_X, tmp_Y, np.zeros((3, 1)), 1e-8, 700)
    # print(f"The cost after training is {tmp_J:.8f}.")
    # print(f"The resulting vector of weights is {[round(t, 8) for t in np.squeeze(tmp_theta)]}")

    # *** TEST FEATURE EXTRACTION***(given)
    # tmp1 = extract_features(train_x[0], freqs)
    # print(tmp1)
    # tmp2 = extract_features('blorb bleeeeb bloooob', freqs)
    # print(tmp2)

    # Train Model
    # Stack features into matrix X
    X = np.zeros((len(train_x), 3))
    for i in range(len(train_x)):
        X[i, :] = extract_features(train_x[i], freqs)
    # training labels corresponding to X
    Y = train_y

    # Apply gradient descent
    J, theta = gradientDescent(X, Y, np.zeros((3, 1)), 1e-9, 1500)
    print(f"The cost after training is {J:.8f}.")
    print(f"The resulting vector of weights is {[round(t, 8) for t in np.squeeze(theta)]}")

    # # *** TEST PREDICT *** (given)
    # for tweet in ['I am happy', 'I am bad', 'this movie should have been great.', 'great', 'great great',
    #               'great great great', 'great great great great']:
    #     print('%s -> %f' % (tweet, predict_sentiment(tweet, freqs, theta)))

    # *** TEST LOGISTIC REG***
    tmp_accuracy = logistic_reg(test_x, test_y, freqs, theta)
    print(f"Logistic regression model's accuracy = {tmp_accuracy:.4f}")
    print(f'Not bad! :D') if tmp_accuracy > .99 else 0

    # Use Logistic Regression to predict sentiment!
    user_tweet = input('Test it on your own tweet: ')
    print(process_tweet(user_tweet))
    y_hat = predict_sentiment(user_tweet, freqs, theta)
    print(y_hat)
    if y_hat > 0.5:
        print("It's positive! :)")
    else:
        print("It's negative! :(")
