# zd_sort
def get_field_list():
    global first_line

    char = os.read(0,1)
    first_line = ''
    
    while char != '\n':
        first_line = first_line + char
        char = os.read(0,1)
    
    first_line = first_line.rstrip()
    field_list = first_line.split('\t')

    return field_list

# zd_cut
def get_field_list():
    first_line = ''
    char = os.read(0,1)
    
    while char != '\n':
        first_line = first_line + char
        char = os.read(0,1)

    first_line = first_line.rstrip()
    field_list = first_line.split('\t')

    return field_list


# zd_select
def get_field_list():
    first_line = sys.stdin.readline()
    first_line = first_line.rstrip('\n')
    print first_line
    
    field_list = first_line.split('\t')
    return strip_spaces(field_list)



# zd_count
def get_field_list():
    first_line = sys.stdin.readline()
    first_line = first_line.rstrip('\n')

    print first_line
    field_list = first_line.split('\t')
    return strip_spaces(field_list)


# zd_combine
def get_field_list():
    first_line = sys.stdin.readline()
    first_line = first_line.rstrip()

    field_list = first_line.split('\t')
    return field_list
    #return strip_spaces(field_list)


# zd_add
def get_field_list():
    first_line = sys.stdin.readline()
    first_line = first_line.rstrip()

    field_list = first_line.split('\t')
    return strip_spaces(field_list)


# zd_stat
def get_field_list():
    first_line = sys.stdin.readline()
    first_line = first_line.rstrip()
    field_list = first_line.split('\t')
    
    return field_list

    
