
# use for wrapper tools (calls UNIX commands) like zd_cut and zd_sort
# since 
def get_field_list_os():
    first_line = ''
    char = os.read(0,1)
    
    while char != '\n':
        first_line = first_line + char
        char = os.read(0,1)

    first_line = first_line.rstrip()
    field_list = first_line.split('\t')

    return field_list

# use for all other tools
def get_field_list():
    first_line = sys.stdin.readline()
    first_line = first_line.rstrip()
    field_list = first_line.split('\t')
    
    return field_list

    
