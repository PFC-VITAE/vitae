import pandas as pd
import numpy  as np
import camelot
from .document import Document

class NCE(Document):

    def __init__(self):
        self.__fields = [

        ]

    def __merge_series(self, pivot, series):
        merged = []
        for item in zip(pivot, series):
            merged.append(item[0] + item[1])
        return pd.Series(data=merged, index=pivot.index)

    def __to_dataframe(self, table_list, end_file=False):
        dataframe_list = []; bottom = pd.Series()
        for table in table_list:
            dataframe = table.df
            dataframe = dataframe.iloc[3:] # remove header
            dataframe = dataframe[dataframe.iloc[:, 0].str.contains('^(?:\d+[a-zA-Z]\d+)?$')] # drop title rows
            dataframe = dataframe.replace("\\n|\s+", " ", regex=True) # replace blank space
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
        table = pd.concat(dataframe_list, ignore_index=True)
        table = table.replace(np.nan, "")
        if not end_file:
            table = table.iloc[:-1]
        return table
    
    def pages(self, filepath, pages):
        handler = camelot.handlers.PDFHandler(filepath)
        page_list = handler._get_pages(filepath, pages=pages)
        return page_list

    def export_page_content(self, filepath, pages):
        page_list = self.pages(filepath, pages)
        all_list = self.pages(filepath, "all")
        end_file = all_list[-1] == page_list[-1]
        print
        table_list = camelot.read_pdf(filepath=filepath, flavor="lattice", pages=pages)
        return self.__to_dataframe(table_list, end_file)
    