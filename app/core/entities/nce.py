import pandas as pd
import numpy  as np
import camelot
import re
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
            dataframe = self.__clean_dataframe(dataframe)
            if dataframe.empty:
                continue
            if not re.match(r'^\d{2}[a-zA-Z]\d{4}.*', dataframe.iloc[0, 0]):
                top = dataframe.iloc[0]
                dataframe = dataframe.iloc[1:]
                if not bottom.empty:
                    dataframe_list[-1].iloc[-1] = self.__merge_series(bottom, top)
            if not dataframe.empty: 
                bottom = dataframe.iloc[-1]
            dataframe_list.append(dataframe)
        dataframe = pd.concat(dataframe_list, ignore_index=True)
        dataframe = dataframe.replace(np.nan, "")
        if not end_file:
            dataframe = dataframe.iloc[:-1]
        return dataframe
    
    def __clean_dataframe(self, dataframe):
        df2 = dataframe.replace('\n', ' ', regex=True)
        df3 = df2[2:]
        if df3.empty:
            return df3
        df3.columns = df2.iloc[1]
        s = df3.pop('Conhecimento Específico/Aplicação')
        df4 = df3[df3.iloc[:, 0] != '']
        
        knowledge_index = s[s == 'Conhecimento Específico'].index
        application_index = s[s == 'Aplicação'].index
        
        if len(df4.index) > len(knowledge_index):
            diff = set(df4.index) - set(knowledge_index)
            knowledge_index = [i - 1 for i in diff] + list(knowledge_index)

        knowledge = [s[i + 1] for i in knowledge_index]
        application = [s[i + 1] for i in application_index]
        application = [''] if not application else application  
        
        df5 = pd.DataFrame({
            "Conhecimento Específico": knowledge,
            "Aplicação": application
        }, index=df4.index)
        df6 = pd.concat([df4, df5], axis=1).reset_index(drop=True)
        
        return df6
    
    def pages(self, filepath, pages):
        handler = camelot.handlers.PDFHandler(filepath)
        page_list = handler._get_pages(filepath, pages=pages)
        return page_list

    def export_page_content(self, filepath, pages):
        page_list = self.pages(filepath, pages)
        all_list = self.pages(filepath, "all")
        end_file = all_list[-1] == page_list[-1]
        table_list = camelot.read_pdf(filepath=filepath, flavor="lattice", pages=pages)
        return self.__to_dataframe(table_list, end_file)
    