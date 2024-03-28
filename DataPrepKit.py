import pandas as pd
import numpy as np

class DataPrep:
    #fuction to read a dataframe from several formats
    def readData(self, filename):
        if len(filename) > 3:
            if filename[-3:] == '.db' or filename[-4:] == '.sql':
                df = pd.read_sql(filename)
                return df
            elif filename[-4:] == '.csv':
                df = pd.read_csv(filename)
                return df
        elif len(filename>=5):
            if filename[-4:] == '.xls' or filename[-5:] == '.xlsx' :
                df = pd.read_excel(filename)
                return df
            elif filename[-5:] == '.json':
                df = pd.read_json(filename)
                return df
            elif filename[-5:] == '.html':
                df = pd.read_html(filename)
                return df
        return 0
    
    #fuction to deal with missing values
    def fixNull(self, df, method):
        if method == 'mean':
            df.fillna(df.dropna().mean(), inplace=True)
        elif method == 'median':
            df.fillna(df.median,inplace=True)
        elif method == 'drop':
            df.dropna(inplace=True)
        return df
    
    #function to remove NULL columns
    def removeNullCols(self, df):
        for col in df:
            if df[col].isnull().all():
                df.drop(col, axis=1, inplace=True)
        return df
    
    #function to categorically encode specific columns
    def encode(self, df, encode_cols):
        for col in encode_cols:
            values = df[col].unique()
            encode_dict = {}
            i = 1
            for value in sorted(values):
                encode_dict[value] = i
                i += 1
            df[col + '_encoded'] = df[col].apply(lambda x: encode_dict[x])
        return df

    #function to print a statistical summary
    def printStats(self,df,numerical_cols=[], category_cols=[]):
        print('***Key Statistical Data***')
        #print mean and median for all numerical columns
        if numerical_cols==0:
            print('Mean and Median for numerical columns:')
            for col in df:
                try:
                    print('{}: mean= {}, median= {}'.format(col, df[col].mean(), df[col].median()))
                except:
                    continue
            print()
        #print mean and columns for specified numerical columns
        else:
            print('Mean and Median for numerical columns:')
            for col in numerical_cols:
                print('{}: mean= {}, median= {}'.format(col, df[col].mean(), df[col].median()))
            print()

        #print value counts for string columns if specific columns are not specified
        if category_cols == 0:
            print('Value Counts for str-type columns:')
            category_cols = [col for col in df if type(df[col]==str)]
            for col in category_cols:
                print(df[col].value_counts())
                print()
        #print value counts for specified columns
        else:
            print('Value Counts for categorically encoded columns:')
            for col in category_cols:
                print(df[col].value_counts())
                print()

    #function to save files to different formats
    def saveFile(self, df, filename):
        if filename[-4:] == '.csv':
            df.to_csv(filename)
        elif filename[-5:] == '.xlsx' or filename[-4:] == '.xls':
            df.to_excel(filename)
        elif filename[-5:] == '.json':
            df.to_json(filename)
        elif filename[-5:] == '.html':
            df.to_html(filename)
        elif filename[-4:] == '.sql' or filename[-3:] == '.db':
            df.to_sql(filename)
        else:
            return False
        return True
