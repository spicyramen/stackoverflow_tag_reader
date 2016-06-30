def get_file_documents(file_name):
    """

    :param file_name:
    :return:
    """
    if not file_name:
        print 'get_file_documents() Not a valid file'
        return

    document_list = []
    # Get file records from output file.

    with open(file_name) as f:
        file_records = [line.decode('utf-8').strip() for line in f.readlines()]

    for file_record in file_records:
        file_record = file_record.encode('ascii', errors='ignore')  # Remove Non-Ascii
        document_list.append(file_record.strip('\n'))  # Remove New Line.

    print len(document_list)
    return document_list
