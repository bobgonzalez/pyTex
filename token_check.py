"""
WISH_LIST_OF_INLINE_MICROEXPRESSIONS:

"""


def token_check(line1):
    sp_line = line1.split()
    for i, token in enumerate(sp_line):
        if token[0:2] == "B{":
            sp_line[i] = "\\textbf" + str(token[1:])
        elif token[0:2] == "I{":
            sp_line[i] = "\\textit" + str(token[1:])
        elif token[0:2] == "->":
            sp_line[i] = "$\\rightarrow$"
        elif token[0:3] == "-->":
            sp_line[i] = "$\\longrightarrow$"
        elif token[0:3] == "<--":
            sp_line[i] = "$\\longleftarrow$"
        elif token[0:2] == "<-":
            sp_line[i] = "$\\leftarrow$"
        elif token[0:2] == "=>":
            sp_line[i] = "$\\Rightarrow$"
        elif token[0:3] == "==>":
            sp_line[i] = "$\\Longrightarrow$"
        elif token[0:3] == "<=>":
            sp_line[i] = "$\\Leftrightarrow$"
        elif token[0:3] == "<==":
            sp_line[i] = "$\\Longleftarrow$"
        elif token[0:2] == "<=":
            sp_line[i] = "$\\Leftarrow$"
        elif token[0:3] == "|->":
            sp_line[i] = "$\\mapsto$"

    new_line = ' '.join(sp_line)
    return new_line
