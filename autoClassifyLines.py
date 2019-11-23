# -*- coding:utf-8 -*-

import pandas as pd

'''
先得到数据集的行数，并给数据集新建一列叫style,初始值为0，用它来作为分类依据。
先将所有同lineName的数据，都改成同一个style,
统计style值的个数，生成一个oldStyleNum
然后生成一个NewStyleNum = oldStyleNum +1 
if newStyleNum =! oldStyleNum:
    oldStyleNum = newStyleNum
    将所有同saleLineGroupID的数据，都改成一个最小的style,
    再将所有同lineName的数据，都改成一个最小的style,
    生成newStyleNum
'''


def filterDataSet(dataSet):
    length = dataSet.shape[0]
    for i in range(0, length):
        if dataSet.loc[i, 'style'] == 0:
            style = i + 1
            currentLineName = dataSet.loc[i, 'lineName']
            # 将所有lineName相同的数据，都归类于同一style
            dataSet.loc[dataSet['lineName'] == currentLineName, 'style'] = style

    groupList = dataSet['saleLineGroupID'].unique()
    lineNameList = dataSet['lineName'].unique()
    oldStyleNum = len(dataSet['style'].unique())
    newStyleNum = oldStyleNum - 1
    while newStyleNum < oldStyleNum:
        oldStyleNum = newStyleNum
        for groupID in groupList:
            minStyle = dataSet[dataSet['saleLineGroupID'] == groupID]['style'].min()
            dataSet.loc[dataSet['saleLineGroupID'] == groupID, 'style'] = minStyle
        for lineName in lineNameList:
            minStyle = dataSet[dataSet['lineName'] == lineName]['style'].min()
            dataSet.loc[dataSet['lineName'] == lineName, 'style'] = minStyle
        newStyleNum = len(dataSet['style'].unique())
    return dataSet


dataSet = pd.read_csv(r'E:\My Documents\拼团数据.csv', sep=',')
dataSet['style'] = 0  # 给数据集新建一个列style，初始值为0。后面的操作就是变动它，以它的值来确定线路的分类
changedDataSet = filterDataSet(dataSet)
changedDataSet.drop_duplicates(subset=['lineName'], keep='first', inplace=True)  # 以线路名称为依据，删掉重复行
newFile = '.\线路分组结果.xlsx'
with pd.ExcelWriter(newFile, mode='w') as writer:
    changedDataSet.to_excel(writer, index=False, header=False)
