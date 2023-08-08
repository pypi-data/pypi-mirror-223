import pandas as pd

class denseDF2DBPlus:
    """
        :Description: This class create Data Base from DataFrame.

        :param inputDF: dataframe :
            It is dense DataFrame
        :param condition: str :
            It is condition to judge the value in dataframe
        :param thresholdValue: int or float :
            User defined value.
        :param tids: list :
            It is tids list.
        :param items: list :
            Store the items list
        :param outputFile: str  :
            Creation data base output to this outputFile.


        """

    def __init__(self, inputDF, thresholdConditionDF):
        self.inputDF = inputDF.T
        self.thresholdConditionDF = thresholdConditionDF
        self.tids = []
        self.items = []
        self.outputFile = ' '
        self.items = list(self.inputDF.index)
        self.tids = list(self.inputDF.columns)
        self.df = pd.merge(self.inputDF, self.thresholdConditionDF, left_index=True, right_index=True)


    def createTransactional(self, outputFile):
        """
        Create transactional data base

        :param outputFile: Write transactional data base into outputFile
        :type outputFile: str
        """

        self.outputFile = outputFile
        with open(outputFile, 'w') as f:
            for tid in self.tids:
                transaction = [item for item in self.items if
                               (self.df.at[item, 'condition'] == '>' and self.df.at[item, tid] > self.df.at[item, 'threshold']) or
                               (self.df.at[item, 'condition'] == '>=' and self.df.at[item, tid] >= self.df.at[item, 'threshold']) or
                               (self.df.at[item, 'condition'] == '<=' and self.df.at[item, tid] <= self.df.at[item, 'threshold']) or
                               (self.df.at[item, 'condition'] == '<' and self.df.at[item, tid] < self.df.at[item, 'threshold']) or
                               (self.df.at[item, 'condition'] == '==' and self.df.at[item, tid] == self.df.at[item, 'threshold']) or
                               (self.df.at[item, 'condition'] == '!=' and self.df.at[item, tid] != self.df.at[item, 'threshold'])]
                if len(transaction) > 1:
                    f.write(f'{transaction[0]}')
                    for item in transaction[1:]:
                        f.write(f',{item}')
                elif len(transaction) == 1:
                    f.write(f'{transaction[0]}')
                else:
                    continue
                f.write('\n')



    def createTemporal(self, outputFile):
        """
        Create temporal data base

        :param outputFile: Write temporal data base into outputFile
        :type outputFile: str
        """

        self.outputFile = outputFile
        with open(outputFile, 'w') as f:
            for tid in self.tids:
                transaction = [item for item in self.items if
                               (self.df.at[item, 'condition'] == '>' and self.df.at[item, tid] > self.df.at[item, 'threshold']) or
                               (self.df.at[item, 'condition'] == '>=' and self.df.at[item, tid] >= self.df.at[item, 'threshold']) or
                               (self.df.at[item, 'condition'] == '<=' and self.df.at[item, tid] <= self.df.at[item, 'threshold']) or
                               (self.df.at[item, 'condition'] == '<' and self.df.at[item, tid] < self.df.at[item, 'threshold']) or
                               (self.df.at[item, 'condition'] == '==' and self.df.at[item, tid] == self.df.at[item, 'threshold']) or
                               (self.df.at[item, 'condition'] == '!=' and self.df.at[item, tid] != self.df.at[item, 'threshold'])]
                if len(transaction) > 1:
                    f.write(f'{tid}')
                    for item in transaction:
                        f.write(f',{item}')
                elif len(transaction) == 1:
                    f.write(f'{tid}')
                    f.write(f',{transaction[0]}')
                else:
                    continue
                f.write('\n')

    def createUtility(self, outputFile):
        """
        Create the utility data base.

        :param outputFile: Write utility data base into outputFile
        :type outputFile: str
        """

        self.outputFile = outputFile
        with open(self.outputFile, 'w') as f:
            for tid in self.tids:
                df = self.inputDF.loc[tid].dropna()
                f.write(f'{df.index[0]}')
                for item in df.index[1:]:
                    f.write(f'\t{item}')
                f.write(f':{df.sum()}:')
                f.write(f'{df.at[df.index[0]]}')
                for item in df.index[1:]:
                    f.write(f'\t{df.at[item]}')
                f.write('\n')

    def getFileName(self):
        """


        :return: outputFile name
        """

        return self.outputFile