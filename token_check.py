"""
WISH_LIST_OF_INLINE_MICROEXPRESSIONS:
        - arrows (-> --> <- <-- => ==> <= <==)
        - textsc{} I{} (italicize)
"""


def token_check(line1):
    sp_line = line1.split()
    for i, token in enumerate(sp_line):
        if token[0:2] == "B{":
            sp_line[i] = "\\textbf" + str(token[1:])
    new_line = ' '.join(sp_line)
    return new_line
