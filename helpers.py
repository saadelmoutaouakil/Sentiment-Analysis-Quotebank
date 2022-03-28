import pandas as pd
import numpy as np
from datetime import *
import nltk
from nltk.stem import WordNetLemmatizer 
from nltk import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import plotly.graph_objects as go 
import string
from scipy.ndimage.filters import gaussian_filter1d

def split_speakers(proba):
	'''
	Extract the speakers from the probas array of the dataframe
	'''
	splitted = proba.split('\'')
	speakers =[]
	for i in range(len(splitted)//4):
		speakers.append(splitted[1+4*i])
  
	return speakers


def count_by_speaker(speaker, df):
  '''
  Counts the number of quotations of the speaker
  '''
  quotations_of_speaker = df[df['most_likely_speaker']==speaker][['most_likely_speaker', 'month']]
  return quotations_of_speaker.groupby('month')['most_likely_speaker'].count().reset_index(name='counts')

def plot_count_speaker(speakers, df_bitcoin):
	'''
	Plots the number of quotationss of each spaeker of spaekers over time
	'''
	fig = go.Figure()
	for speaker in speakers:
		df = pd.DataFrame(count_by_speaker(speaker, df_bitcoin))
		df['month'] = pd.to_datetime(df['month'].apply(lambda x: x.to_timestamp()))
		fig.add_trace(go.Scatter(x=df['month'], y=df['counts'], name=speaker))
	fig.update_layout(
		title="Number of quotations by speaker over the years",
		xaxis_title="Date",
		yaxis_title="Number of quotes",
		)
	return fig

def remove_punctuation(s):
	'''
	Removes the punction from s
	'''
	return s.apply(lambda x: x.translate(str.maketrans('', '', string.punctuation)))

def lemmatize_text(s):
	'''
	Lemmatizes all the word of the string s
	'''
	lm = WordNetLemmatizer()
	wk = nltk.tokenize.WhitespaceTokenizer()
	return " ".join([lm.lemmatize(w) for w in wk.tokenize(s)])

def process(df_bitcoin):
	'''
	Processing the dataframe quotations
	'''
	df = df_bitcoin.copy()
	nltk.download('wordnet')
	df['quotation'] = remove_punctuation(df['quotation'])
	df['quotation'] = df['quotation'].apply(lambda s: lemmatize_text(s))
	return df

def normalize(column):
	'''
	Normalizes the data of the column
	'''
	min_ = column.min()
	max_min = column.max() - column.min()
	return (column-min_)/max_min
