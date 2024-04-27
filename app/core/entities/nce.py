import pandas as pd
import camelot
from .document import Document

class NCE(Document):

    def __merge_series(self, pivot, series):
        '''
        Merge the content of two Series
        '''
        merged = []
        for item in zip(pivot, series):
            merged.append(item[0] + " " + item[1])
        return pd.Series(data=merged, index=pivot.index)

    def __clean_dataframe(self, dataframe: pd.DataFrame):
        '''
        Clean the Dataframe
        '''
        dataframe = dataframe.iloc[3:] # remove headings
        dataframe = dataframe[dataframe.iloc[:, 0].str.contains('\d{2}[a-zA-Z]\d{4}|^\s*$')] # drop title rows 
        dataframe = dataframe.replace("\n", " ", regex=True) # remove blank space
        return dataframe

    def __to_dataframe(self, table_list):
        '''
        Transform a camelot's table in a well formatted pandas dataframe
        '''
        dataframe_list = []; bottom = pd.Series()
        for table in table_list:
            dataframe = table.df
            dataframe = self.__clean_dataframe(dataframe)
            if dataframe.empty: 
                continue
            if not dataframe.iloc[0, 0]:
                top = dataframe.iloc[0]
                dataframe = dataframe.iloc[1:]
                if not bottom.empty:
                    dataframe_list[-1].iloc[-1] = self.__merge_series(bottom, top)
            if not dataframe.empty: 
                bottom = dataframe.iloc[-1]
            dataframe_list.append(dataframe)
        return pd.concat(dataframe_list, ignore_index=True)

    def export_page_content(self, filepath, pages):
        '''
        Extract the content of the pdf file and create a camelot's table
        '''
        table_list = camelot.read_pdf(filepath=filepath, flavor="lattice", pages=f"{pages}")
        return self.__to_dataframe(table_list)
    