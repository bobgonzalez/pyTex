from __future__ import print_function
import sys
from datetime import date
from subprocess import call
from token_check import token_check
from micro_exp import MicroExpressions
"""
    *TODO: handle empty lines
    *TODO: support tables
    **TODO: flag for explicit filename extensions
    **TODO: adjust vertical spacing of LINE
"""

def init():
    file_name = sys.argv[1]
    out = file_name.replace(".txt", ".tex")
    try:
        text_file = open(file_name, 'r')
    except (IOError, OSError) as e:
        print("file " + file_name + " not found! \n" +
              "Please enter file in local directory or absolute path to file.")
        return
    sys.stdout = open(out, 'w')
    file_name = file_name.replace("_", "\\_")

    print(make_header())
    #print(make_title(file_name))
    me = MicroExpressions()
    for line in text_file:
        row = line.split()
        for op in me.exps:
            if op.macro == row[0]:
                print(op.handler(line))
                break
        else:
            print(token_check(line))

    print("\n\\end{document}")
    text_file.close()
    sys.stdout = sys.__stdout__
    call(["pdflatex", str(out)])


def make_header():
    ret = ["\\documentclass{article}",
           "\\pagestyle{plain}",
           "\\usepackage{graphicx, wrapfig, mathpazo, csquotes, float, tcolorbox}\n",
           "\\begin{document}\n"]
    return '\n'.join(ret)


def make_title(file_name):
    cur_date = date.today()
    ret = ["\\title{\\textbf{" + file_name[:-4] + "}}",
           "\\author{\\textsc{}}",
           "\\date{" + str(cur_date.month) + "/" + str(cur_date.day) + "/" + str(cur_date.year) + "}",
           "\\maketitle\n"]
    return '\n'.join(ret)
