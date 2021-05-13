def get_headers(gmail_message, headers):
    result = {}

    for header in headers:
        result[header] = get_header(gmail_message, header)

    return result


def get_header(gmail_message, target_header_name):
    headers = gmail_message['payload']['headers']
    header_names = [header['name'] for header in headers]
    try:
        return headers[header_names.index(target_header_name)]['value']
    except KeyError:
        return None


def get_attachment_details(gmail_message):
    if not gmail_message['payload']['mimeType'].startswith('multipart'):
        return []

    if 'parts' not in gmail_message['payload']:
        return []

    return [
        {
            'id': part['body']['attachmentId'],
            'filename': part['filename']
        }
        for part in gmail_message['payload']['parts']
        if part['filename'] != ''
    ]


def get_attachment(gmail_message):
    pass
