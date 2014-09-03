#coding=utf-8
from os import environ, system, unlink
from re import (split as re_split, compile as re_compile)
import time
from urllib import quote
from urllib2 import Request, urlopen, HTTPError
from tempfile import NamedTemporaryFile
from translate import Translator

LANG_CODES = {
        "Afrikaans":"af",
        "Albanian":"sq",
        "Arabic":"ar",
        "Armenian":"hy",
        "Azerbaijani":"az",
        "Basque":"eu",
        "Belarusian":"be",
        "Bengali":"bn",
        "Bosnian":"bs",
        "Bulgarian":"bg",
        "Catalan":"ca",
        "Cebuano":"ceb",
        "Chinese (Simplified)":"zh-CN",
        "Chinese (Traditional)":"zh-TW",
        "Croatian":"hr",
        "Czech":"cs",
        "Danish":"da",
        "Dutch":"nl",
        "English":"en",
        "Esperanto":"eo",
        "Estonian":"et",
        "Filipino":"tl",
        "Finnish":"fi",
        "French":"fr",
        "Galician":"gl",
        "Georgian":"ka",
        "German":"de",
        "Greek":"el",
        "Gujarati":"gu",
        "Haitian Creole":"ht",
        "Hausa":"ha",
        "Hebrew":"iw",
        "Hindi":"hi",
        "Hmong":"hmn",
        "Hungarian":"hu",
        "Icelandic":"is",
        "Igbo":"ig",
        "Indonesian":"id",
        "Irish":"ga",
        "Italian":"it",
        "Japanese":"ja",
        "Javanese":"jw",
        "Kannada":"kn",
        "Khmer":"km",
        "Korean":"ko",
        "Lao":"lo",
        "Latin":"la",
        "Latvian":"lv",
        "Lithuanian":"lt",
        "Macedonian":"mk",
        "Malay":"ms",
        "Maltese":"mt",
        "Maori":"mi",
        "Marathi":"mr",
        "Mongolian":"mn",
        "Nepali":"ne",
        "Norwegian":"no",
        "Persian":"fa",
        "Polish":"pl",
        "Portuguese":"pt",
        "Punjabi":"pa",
        "Romanian":"ro",
        "Russian":"ru",
        "Serbian":"sr",
        "Slovak":"sk",
        "Slovenian":"sl",
        "Somali":"so",
        "Spanish":"es",
        "Swahili":"sw",
        "Swedish":"sv",
        "Tamil":"ta",
        "Telugu":"te",
        "Thai":"th",
        "Turkish":"tr",
        "Ukrainian":"uk",
        "Urdu":"ur",
        "Vietnamese":"vi",
        "Welsh":"cy",
        "Yiddish":"yi",
        "Yoruba":"yo",
        "Zulu":"zu"
        }

SELECTEDTEXT= environ['POPCLIP_TEXT']
DESTLANG = environ['POPCLIP_OPTION_DESTLANG']
TTSLANG = environ['POPCLIP_OPTION_TTSLANG']
GTRANSLATEIP = environ['POPCLIP_OPTION_GTRANSIP'].strip()

def google_tts(text, tl='en', ip_addr=None):
    """
    this function is adapted from https://github.com/hungtruong/Google-Translate-TTS, thanks @hungtruong.
    """
	#process text into chunks
    text = text.replace('\n','')
    text_list = re_split('(\,|\.)', text)
    combined_text = []
    for idx, val in enumerate(text_list):
        if idx % 2 == 0:
            combined_text.append(val)
        else:
            joined_text = ''.join((combined_text.pop(),val))
            if len(joined_text) < 100:
                combined_text.append(joined_text)
            else:
                subparts = re_split('( )', joined_text)
                temp_string = ""
                temp_array = []
                for part in subparts:
                    temp_string = temp_string + part
                    if len(temp_string) > 80:
                        temp_array.append(temp_string)
                        temp_string = ""
                #append final part
                temp_array.append(temp_string)
                combined_text.extend(temp_array)
    #download chunks and write them to the output file
    f = NamedTemporaryFile(delete=False)
    host = ip_addr if ip_addr else "translate.google.com"
    headers = {"Host":"translate.google.com",
      "Referer":"http://www.gstatic.com/translate/sound_player2.swf",
      "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36"}
    for idx, val in enumerate(combined_text):
        mp3url = "http://%s/translate_tts?tl=%s&q=%s&total=%s&idx=%s" % (host, tl, quote(val), len(combined_text), idx)
        req = Request(mp3url, headers=headers)
        if len(val) > 0:
            try:
                response = urlopen(req)
                f.write(response.read())
            except HTTPError as e:
                pass
    f.close()
    system('afplay {0}'.format(f.name))
    unlink(f.name)


if __name__ == '__main__':
    ip_addr = GTRANSLATEIP
    ip_pattern = re_compile('^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$')
    ip_match = ip_pattern.search(GTRANSLATEIP)
    if not ip_match:
        ip_addr = 'translate.google.com'
    if TTSLANG != 'Disabled':
        google_tts(SELECTEDTEXT, LANG_CODES[TTSLANG], ip_addr)
    translator = Translator(to_lang=LANG_CODES[DESTLANG])
    translation = translator.translate(SELECTEDTEXT, ip_addr)
    result = translation.encode('utf-8')
    print result
