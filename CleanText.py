

#########################################
####### Standard Settings ###############
#########################################

# Modifying original text
LOWER = True
EXPAND_CONTRACTIONS = True
REMOVE_STOPWORDS = True

# Removing elements of original text
LINKS = True
DIGITS = True
EMOJI = True
HASH = True
AT = True
PUNCTUATION = True

#########################################




import html2text, yaml, re, string
from nltk.corpus import stopwords


class CleanText():
    '''
    Will help clean text.
    '''
    
    def __init__(self, text, special_replacements = {}, stopwords = []):
        if not isinstance(text, str): text = "" # this function only takes strings, so whatever else is fed to it needs to be neutralized
        if stopwords and not isinstance(stopwords, list): raise RuntimeError("stopwords provided needs to be a list of strings.")
        if special_replacements and not isinstance(special_replacements, dict): raise RuntimeError("special_replacements provided needs to be a dictionary.")

        self.original_text = text
        
        # process variables
        self.lower = LOWER
        self.expand_contractions = EXPAND_CONTRACTIONS
        self.remove_stopwords = REMOVE_STOPWORDS
        self.special_replacements = special_replacements
        self.stopwords = stopwords

        # remove
        self.links = LINKS
        self.digits = DIGITS
        self.emoji = EMOJI
        self.hash = HASH
        self.at = AT
        self.punctuation = PUNCTUATION
        
        # cleaning process
        self.text = self.original_text
        self.clean()

    def clean(self):
      _ = self.original_text
      if self.special_replacements: _ = self._special_replacement(_)
      _ = self._clean_html(_)
      if self.lower: _ = _.lower()
      if self.links: _ = self._clean_links(_)
      if self.hash: _ = self._clean_hashtags(_)
      if self.at: _ = self._clean_ats(_)
      if self.digits: _ = self._clean_digits(_)
      if self.emoji: _ = self._clean_emojis(_)
      if self.punctuation: _ = self._clean_punctuation(_)
      if self.expand_contractions: _ = self._expand_contractions(_)
      _ = self._clean_stopwords(_)
      _ = _.strip()
      self.text = _
      return(_)

    def _special_replacement(self, text):
        c_re = re.compile('(%s)' % '|'.join(self.special_replacements.keys()))
        def replace(match):
            return self.special_replacements[match.group(0)]
        return(c_re.sub(replace, text))
    
    def _clean_html(self, text):
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.bypass_tables = True
        return(h.handle(text).strip())
    
    def _clean_links(self, text): # todo: also replace www.????.co/m?
        _ = re.sub(r"(?i)\b((?:[a-z][\w-]+:(?:\/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}\/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))", "", text)
        return(_.strip())
    
    def _clean_hashtags(self, text):
        return(re.sub(r"#[\w-]+", "", text))
    
    def _clean_ats(self, text):
        return(re.sub(r"@[\w-]+", "", text))
    
    def _clean_digits(self, text):
        return(re.sub(r"[{}]".format(string.digits)," ", text))
    
    def _clean_emojis(self, text):
        _ = ""
        for character in text:
            try:
                character.encode("ascii")
                _ += character
            except UnicodeEncodeError:
                _ += ' '
        return(_.strip())
    
    def _clean_punctuation(self, text):
        _ = re.sub("[{}]".format(string.punctuation)," ", text)
        _ = re.sub("[¡“”’]"," ", _)
        return(_)
    
    def _clean_stopwords(self, text):
        stops = stopwords.words('english')
        stops.extend(self.stopwords)
        stops = set(stops)
        _ = " ".join([word for word in text.split() if word not in stops])
        return(_)
    
    def _expand_contractions(self, text):
        with open("./configuration/contractions.yml") as f:
            contractions = yaml.load(stream=f)
        c_re = re.compile('(%s)' % '|'.join(contractions.keys()))
        def replace(match):
            return contractions[match.group(0)]
        return(c_re.sub(replace, text))
    
    def __repr__(self):
        return(self.current_text)