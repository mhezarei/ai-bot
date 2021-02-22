def find_religious_time(string):
    """
	Gets whole input srtring

	"""

    religiuos_times_types = ['امساک', 'اذان عشائ', 'اذان مغرب', 'اذان عصر',
                             'اذان ظهر', 'اذان صبح', 'طلوع آفتاب',
                             'غروب آفتاب', 'نیمه شب شرعی']
    religious_type = []
    for religiuos in religiuos_times_types:
        if religiuos in string:
            religious_type.append(religiuos)
    adhan_times_types = ['اذان عشائ', 'اذان مغرب', 'اذان عصر', 'اذان ظهر',
                         'اذان صبح']
    if not bool(set(religious_type).intersection(adhan_times_types)):
        if 'اذان' in string:
            religious_type.append('اذان')
    indexes = []
    for elem in religious_type:
        indexes.append(string.find(elem))
    religious_type = [x for _, x in sorted(zip(indexes, religious_type))]
    return religious_type
