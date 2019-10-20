import xlrd
import xlwt
import numpy as np
import copy
data = xlrd.open_workbook("shuju1.xlsx") # open xlsx
table = data.sheet_by_name("Sheet1")  # open sheet in xlsx
nrows = table.nrows  # get number of line
print nrows
result = []
for i in range(0,nrows):
    rows = table.row_values(i)  # get line date of xlsx table. row number strat from zero.
    result.append(rows)
# print result
location_B = []
for i in range(0,len(result[0])):  # get location of binary in each point
    if type(result[0][i]) == float:
        location_B.append(int(result[0][i]))
del result[0]
nrows = nrows -1
ncols = len(result[0])
#  translate str to float
for i in range(0,nrows):
    for j in range(0,ncols):
        try:
            result[i][j] = float(result[i][j])
        except:
            print i,j
result = np.array(result)
result_ = []
for i in range(0,ncols):
    if i+1 in location_B:
        result_.append(result[:,i])
result_ = np.array(result_).T  #  the array of binary variable in points
print result_.shape,"which has the whole rows and binary columns"
result_ceil = np.ceil(result_)
result_ceil = np.sum(result_ceil,1)
result_ = np.sum(result_,1)# if one binary variable of points is non-integral, the sum value of all binaries of this point include decimal fraction.
print result_.shape,"which is the sum of all binary columns with all rows"
B = result_ == result_ceil   # so the ceil of this sum value is not equal to itself.
book = xlwt.Workbook(encoding='utf-8', style_compression=0)
CNOV = book.add_sheet('CNOV', cell_overwrite_ok=True)
n = 0
for j in range(0,ncols):
    if j+1 in location_B:
        CNOV.write(0, j, "B")
    else:
        CNOV.write(0, j, "C")
for i in range(0,nrows):
    if B[i] == True:
        n += 1
        for j in range(0,ncols):
            CNOV.write(n,j,result[i,j])
book.save('shuju1_CONV.xls')