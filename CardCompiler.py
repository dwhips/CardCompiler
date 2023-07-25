

import numpy as np
import cv2, os, math
# import PIL
# from PIL import Image

#Private Variables
strBasePath = ''
cols = 3 #TODO might want to support different file sizes
rows = 0 #will be calc'd from number of images in the filepath
maxRowsPerPage = 3 #TODO might need to support resized images

#Functions
def GetBasePath():
    strPath = os.getcwd()
    strPath = strPath.replace('\\CardCompiler', '')
    strPath += '\\HomeHub'
    return strPath

def GetIMGFilePath(pstrFileName):
    return strBasePath + "\\CardComp\\" + pstrFileName
def GetOutputIMGPath(pstrPageNumber):
    return strBasePath + "\\CardOutput\\CardsPage" + pstrPageNumber + ".png"

def GetRowMinElem(pRow, pColumns):
    # print("min: " + str((pRow - 1)*pColumns))
    return (pRow - 1)*pColumns
def GetRowMaxElem(pRow, pColumns):
    # print("max: " + str(pRow * pColumns))
    'TODO needs to know if we are going over the max. seems like python already handles this'
    return pRow * pColumns

def CreateWhiteFiller(pcv2RowData, pcols):
    nMissingCols = pcols - len(pcv2RowData)
    if nMissingCols == 0: return pcv2RowData

    'Making blank elem'
    'TODO this assumes all elements are the same size'
    test = pcv2RowData[0].shape
    img_1 = np.zeros([test[0],
                      test[1],
                      test[2]],
                      dtype=np.uint8)
    img_1.fill(255)

    for icol in range(nMissingCols):
        pcv2RowData.append(img_1)
    return pcv2RowData

def concat_vh(list_2d):
      # return final image
      #This requires the rows to have equal columns
    return cv2.vconcat([cv2.hconcat(list_h) 
                        for list_h in list_2d])

#Main
print("Initializing... \nGetting images from folder:" + strBasePath)

strBasePath = GetBasePath()
#Loop through each photo
photoList = os.listdir(GetIMGFilePath(''))
rows = math.ceil(len(photoList) / 3)

cv2_templist = []
cv2_pagelist = []
for irow in range(1,rows+1):
    page = str(math.ceil(irow/maxRowsPerPage))
    for photo in photoList[GetRowMinElem(irow, cols):GetRowMaxElem(irow, cols)]:
        'TODO need to ensure images are sized correctly. If they are not, have some output warning'
        img = cv2.imread(GetIMGFilePath(photo))
        cv2_templist.append(img)

    if len(cv2_templist) < cols:
        'the row is incomplete. The final concatenation requires all rows to be filled'
        CreateWhiteFiller(cv2_templist, cols)

    'Adding current row list to the page array'
    cv2_pagelist.append(cv2_templist)
    test = cv2_templist[0].shape
    cv2_templist = []

    if irow % maxRowsPerPage == 0 or irow == rows:
        print('Printing page: ' + page)

        if not cv2.imwrite(GetOutputIMGPath(page), concat_vh(cv2_pagelist)): Exception("Failed to generate photo for page" + page)
        cv2_pagelist = []

print("Finished")

