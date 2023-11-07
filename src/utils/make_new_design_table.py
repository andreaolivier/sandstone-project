

def make_new_design_table(big_dict):
    '''This takes the full data dictionary and returns a dictionary containing lists of the appropriate columns, maintaining the same structure otherwise.'''
    design_table = big_dict['design']
    
    if design_table['design_id'] == []:
        return {}

    design_columns = ['design_id', 'design_name', 'file_location', 'file_name']

    dim_design = {key: design_table[key] for key in design_columns}


    return dim_design

