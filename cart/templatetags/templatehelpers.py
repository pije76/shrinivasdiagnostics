from django import template

register = template.Library()

@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url


@register.simple_tag
def relative_url_select_page(value, field_name,page=1, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        filtered_querystring_data=[]
        for i in filtered_querystring:
            split_data= i.split('=')
            if split_data and split_data[0] and split_data[0]=='page':
                filtered_querystring_data.append('page=1')   
            else:
                filtered_querystring_data.append(i)
        
        encoded_querystring = '&'.join(filtered_querystring_data)
        
        url = '{}&{}'.format(url, encoded_querystring)
    return url


@register.filter
def prevPage(value):
    return value-1


@register.filter
def nextPage(value):
    return value+1

@register.simple_tag
def current_record(page_number,per_page_record,total_record):
    print(total_record)
    calculate_record=int(page_number)*int(per_page_record)
    if int(total_record) > int(calculate_record):
        total_record=calculate_record
    return total_record
