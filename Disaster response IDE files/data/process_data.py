import sys
import numpy as np 
import pandas as pd
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    """
    The input is the path of the messages and the categories files
    
    Returns a dataframe
    """
    
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    df = pd.merge(messages, categories, on="id")
    return df


def clean_data(df):
    """
    The function aims at creating a cleanining the dataframe 
    Adjust the headers
    make the category data in integer form
    remove dublicated data
    """
    
    categories = df.categories.str.split(pat=';', expand=True)
    row = categories.iloc[0,:]
    category_colnames = row.apply (lambda x: x.rstrip ('- 1 0'))
    categories.columns = category_colnames
    
    # Iterate over columns to extract the number only from all entries
    for column in categories:
    # set each value to be the last character of the string
        categories[column] = categories[column].str[-1]
    
    # convert column from string to numeric
        categories[column] = categories[column].astype('int')
        
    df = df.drop(axis=1, columns='categories')
    #add the extracted categories columns into the dataframe and drop the missed category column
    df = pd.concat([df, categories], axis =1)
    
    ## drop dublicated entries from the dataframe
    df.drop_duplicates(inplace = True)
    return df
    
    
def save_data(df, database_filename):
    # extract the data to 
    engine = create_engine('sqlite:///{}'.format(database_filename))
    df.to_sql('{}'.format("DisasterResponse"), engine, index=False, if_exists='replace')
    
def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()
