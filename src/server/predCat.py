"""
Predict model for demo page ver2.
load module, get predict data for just one sample
~ 08.25.2017
Stackcat - just summation.
technically, other teamate help it
"""
import random, os, csv, re
import tensorflow as tf
import numpy as np
from sklearn.externals import joblib
from utilCat import *


r = random.Random()
lim_unigram = 5000
target_size = 4
hidden_size = 100
train_keep_prob = 0.6
l2_alpha = 0.00001
initial_learn_rate = 0.01
clip_ratio = 5
batch_size_train = 500
epochs = 1000
w2v_size = 300
feature_size = 10002

features_pl = tf.placeholder(tf.float32, [None, feature_size], 'features')
stances_pl = tf.placeholder(tf.int64, [None], 'stances')
keep_prob_pl = tf.placeholder(tf.float32)
phase = tf.placeholder(tf.bool, name="phase")

batch_size = tf.shape(features_pl)[0]

# Define multi-layer perceptron
hidden_layer = tf.nn.dropout(tf.nn.relu(tf.contrib.layers.linear(features_pl, hidden_size)), keep_prob=keep_prob_pl)
logits_flat = tf.nn.dropout(tf.contrib.layers.linear(hidden_layer, target_size), keep_prob=keep_prob_pl)
logits = tf.reshape(logits_flat, [batch_size, target_size])

# Define L2 loss
tf_vars = tf.trainable_variables()
l2_loss = tf.add_n([tf.nn.l2_loss(v) for v in tf_vars if 'bias' not in v.name]) * l2_alpha

# Define overall loss
loss = tf.reduce_sum(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=stances_pl) + l2_loss)

# Define prediction
softmaxed_logits = tf.nn.softmax(logits)


def get_lftm_stances(head, body):
    hidden_size2 = 20
    hidden_layer = tf.nn.dropout(tf.nn.relu(tf.contrib.layers.linear(features_pl, hidden_size)), keep_prob=keep_prob_pl)
    hidden_layer2 = tf.nn.dropout(tf.nn.relu(tf.contrib.layers.linear(hidden_layer, hidden_size2)), keep_prob=keep_prob_pl)
    logits_flat = tf.nn.dropout(tf.contrib.layers.linear(hidden_layer2, target_size), keep_prob=keep_prob_pl) 
    bow_vec = joblib.load("/home/fndetect/server/pickle/bow_vec_lftm.pkl")
    tfreq_vec = joblib.load("/home/fndetect/server/pickle/tfreq_vec_lftm.pkl")
    tfidf_vec = joblib.load("/home/fndetect/server/pickle/tfidf_vec_lftm.pkl")
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        feature_vector = get_w2v_feature_vector(head, body, bow_vec, tfreq_vec, tfidf_vec)
        test_feed_dict = {features_pl:feature_vector.T, keep_prob_pl:1.0, phase:False}
        softmaxed_logit = sess.run(softmaxed_logits, feed_dict=test_feed_dict)
    return softmaxed_logit


def get_w2v_stances(head, body):
    bow_vec = joblib.load("/home/fndetect/server/pickle/bow_vec_w2v.pkl")
    tfreq_vec = joblib.load("/home/fndetect/server/pickle/tfreq_vec_w2v.pkl")
    tfidf_vec = joblib.load("/home/fndetect/server/pickle/tfidf_vec_w2v.pkl")
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        feature_vector = get_w2v_feature_vector(head, body, bow_vec, tfreq_vec, tfidf_vec)
        test_feed_dict = {features_pl: feature_vector.T, keep_prob_pl: 1.0}
        softmaxed_logit = sess.run(softmaxed_logits, feed_dict=test_feed_dict)
    return softmaxed_logit

def get_result_stances(head, bodyid):
    w0, w1 = 0.8, 0.2
    head = head
    f = open("/home/fndetect/server/test_bodies.csv", "r", encoding="utf-8")
    r = csv.DictReader(f)
    bodies = {}
    for line in r:
        bodies[line["Body ID"]] = line["articleBody"]
    body = bodies[bodyid]
    w2v_stances = get_w2v_stances(head, body)[0]
    lftm_stances = get_lftm_stances(head, body)[0]
    result = w2v_stances*w0 + lftm_stances*w1
    result /= (w0+w1) 
    return result.tolist() 

if __name__ == "__main__":
    head = "Police find mass graves with at least '15 bodies' near Mexico town where 43 students disappeared after police clash"
    bodyid = 712
    s = get_result_stances(head,bodyid)
    print(s)
