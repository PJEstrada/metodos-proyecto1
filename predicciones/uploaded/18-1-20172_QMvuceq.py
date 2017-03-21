from pylab import *
import matplotlib.pyplot as plt
from openpyxl import load_workbook

DEFAULT_SHEET = 'Sheet1'


def sheet_to_list(sheet):

    # Accumulators
    result = []
    keys = []

    # Initial row is important because we assume it cointains column headers
    first_row = True

    # Linealyze sheet as a list of rows
    sheet = list(sheet)

    for i in range(len(sheet)):

        # Linealyze row as a list of cells
        row = list(sheet[i])

        # Extract headers if it's the first row
        if first_row:

            # For each cell in the first row, accumulate'em as keys
            for cell in row:
                keys.append(cell.value)

            # After this line, we are no longer analyzing the first row
            first_row = False

        else:

            # New row object representation
            row_object = {}

            # For each cell in the row, build the row object using the
            # corresponding keys (parallel lists)
            for i in range(len(row)):
                row_object[keys[i]] = row[i].value

            result.append(row_object)

    return result


def load_xlsx(filename):

    print "Loading %s" % filename
    return sheet_to_list(load_workbook(filename=filename)[DEFAULT_SHEET])


x1 = linspace(0,2*pi)
x2 = linspace(0,2*pi)
x3 = linspace(1,10)
x4 = linspace(1,10000)

y1 = sin(x1)
y2 = cos(x2)
y3 = e**x3
y4 = log10(x4)
x = linspace(-100,100)

y5 = raw_input("Ingrese funcion 1 f(x): ")
y5 = eval(y5)
y6 = raw_input("Ingrese funcion 2 f(x): ")
y6 = eval(y6)

f, ((ax1, ax2), (ax3, ax4), (ax5, ax6))  = plt.subplots(3, 2)
ax1.plot(x1,y1)
ax1.set_xlim(0,2*pi)
ax2.plot(x2,y2)
ax2.set_xlim(0, 2*pi)
ax3.plot(x3,y3)
ax3.set_xlim(min(x3), max(x3))
ax3.set_ylim(min(y3), max(y3))
ax4.plot(x4,y4)
ax4.set_xlim(0, 1000)
ax4.set_ylim(0, 10)
ax5.plot(x4,y5)
ax6.plot(x4,y6)
ax1.set_title("Graficas")
plt.show()
