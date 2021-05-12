def extractDetails(gmail_message):
    headers = gmail_message['payload']['headers']

    date = safeGetHeader(headers, 'Date')
    subject = safeGetHeader(headers, 'Subject')

    content_type = safeGetHeader(headers, 'Content-Type')
    if content_type is not None:
        has_attachment = content_type.startswith('multipart/mixed')
    else:
        has_attachment = False

    return {
        'date': date,
        'subject': subject,
        'has_attachment': has_attachment
    }


def safeGetHeader(headers, target_header_name):
    header_names = [header['name'] for header in headers]
    try:
        return headers[header_names.index(target_header_name)]['value']
    except KeyError:
        return None

# TODO: convert extractDetails into extract_headers(message, headers)
# TODO: get attachment name
