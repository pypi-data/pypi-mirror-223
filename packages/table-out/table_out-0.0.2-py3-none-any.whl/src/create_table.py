def create_table(rows, columns, values, formatting="center"):
    max_width = max(len(i) for i in values)

    if max_width % 2 == 0:
        reformat = 0
    else:
        reformat = 1
    
    width = max_width
    width += reformat
    width *= 2

    x = (('x' +('-'*width))*columns + 'x')
    y = '\n'
    table = ""
    index = 0

    for _ in range(rows):
        for _ in range(columns):
            l = len(values[index])
            padding = ((width) - l) // 2
            reformat = 0

            if l % 2 == 0:
                reformat = 0
            else:
                reformat = 1

            if formatting == "left-align":
                padding_l = width // 4
                padding_r = width - l - padding_l
            elif formatting == "right-align":
                padding_r = width // 4
                padding_l = width - l - padding_r
            else:
                padding_l = padding
                padding_r = padding + reformat
            
            y += ('|' + ' '*padding_l + (values[index] + ' '*padding_r))
            index += 1
        y += '|' + '\n' + x + '\n'
    table += x + y

    return table