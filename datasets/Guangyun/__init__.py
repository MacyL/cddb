import re
from sinopy import sinopy

def prepare(dataset):

    with open(dataset.get_path('raw', 'sbgy.xml')) as f:
        data = f.readlines()
    
    D = [('ID', 'CHARACTER_ID', 'CHARACTER', 'DOCULECT', 'PINYIN', 'READING', 'FANQIE',
        'RHYME_ID', 'RHYME_NUMBER', 'VOLUME', 'NOTE', 'SOURCE')]
    volume, rhyme_id, rhyme, ipa, fanqie, text  = '', '', '', '', '', ''
    idx = 1
    for line in data:
        if '<volume id' in line:
            volume = re.findall('id="(.*?)"', line)[0]
            
        if 'rhyme id="' in line:
            rhyme_id = re.findall('id="(.*?)"', line)[0]
        
        if rhyme_id:
            
            if 'rhyme_num' in line:
                rhyme = re.findall('>(.*?)<', line)[0]

            if 'voice_part ipa' in line:
                ipa = re.findall('ipa="(.*?)"', line)[0]
            

            if '/word_head' in line and text:
                text = text.replace('\n', ' ').strip()
                charid, char = re.findall(
                        '<word_head id="(.*?)">(.*?)<',
                        text)[0]
                note = re.findall('<note>(.*?)</note>', text)
                note = note[0] if note else ''

                if 'fanqie' in text:
                    fanqie = re.findall(
                            '<fanqie>(.*?)</fanqie>',
                            text)[0]
                    pinyin = sinopy.pinyin(char)
                    if '?' in pinyin or sinopy.is_chinese(pinyin):
                        pinyin = ''
                if sinopy.is_chinese(char.strip()):
                    D += [(str(idx),
                        charid, char.strip(), 'Middle_Chinese', pinyin, ipa,
                        fanqie.strip(),
                        rhyme_id.strip(), rhyme.strip(), volume, note.strip(),
                        'Zhou1938')]
                    idx += 1
                else:
                    print('[ERROR]', char, sinopy.is_chinese(char), ipa, fanqie)
                text = ''
            
            if text:
                text += line
            
            if 'word_head id' in line:
                text = line



    with open(dataset.get_path('characters.tsv'), 'w') as f:
        for line in D:
            f.write('\t'.join([l.replace('\t', '') for l in line])+'\n')
            
