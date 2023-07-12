text="M.Sc. in Biotechnology"

if 'master' in text.lower():
    degree='Masters'
elif 'masters' in text.lower():
    degree='Masters'
elif 'm.' in text.lower():
    degree='Masters'
elif 'm.' and 'b.' in text.lower():
    degree='Masters'
elif 'b.' and 'm.' in text.lower():
    degree='Masters'
elif 'bachelor' in text.lower():
    degree='Bachelors'
elif 'bachelors' in text.lower():
    degree='Bachelors'
elif 'b.' in text.lower():
    degree='Bachelors'
elif 'pg' in text.lower():
    degree='Diploma'
elif 'p.g.' in text.lower():
    defree='Diploma'
elif 'diploma' in text.lower():
    degree='Diploma'
elif 'ph.d.' in text.lower():
    degree='Doctorate'
else:
    pass

if 'm.' and 'b.' in text.lower():
    print('zzz')
