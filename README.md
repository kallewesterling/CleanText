# CleanText

CleanText is a Python package that I use in my research projects to clean social media captions but will likely be useful to others beyond that scope, so I wanted to make it available here as well.

## Dependencies

The package is dependent on some various other packages: `html2text`, `yaml`, and `unidecode`. They need all to be installed:

```sh
pip install html2text
```

```sh
pip install yaml
```

```sh
pip install unidecode
```

## Usage

To import the package, make sure that you run the following command:

```python
from CleanText import *
```

Next, set up an object with the default settings (see [below](specific-settings) for instructions on how to change the settings):

```python
text = "This is an advertisement to call # 222-109-1100 or go to http://www.apple.com. Maybe this will be replaced with definitely and perhaps also. If you're using quotation marks, those will be replaced."
cleaner = CleanText(text)
```

To access the cleaned text, simply call:

```python
cleaner.text
```

If you surround it with a `print()` function, it should generate the following result:

```python
advertisement call go maybe replaced definitely perhaps also
```

## Ingestation

A CleanText instance accepts three arguments. `text`, as seen above, is a required argument. You can also provide your own list of stopwords as well as replacements.

### Stopwords

A list of strings provided as `stopwords` will expand the numbers of words that will be removed in the stopword removal process. For example:

```python
text = "This is an advertisement to call # 222-109-1100 or go to http://www.apple.com. Maybe this will be replaced with definitely and perhaps also. If you're using quotation marks, those will be replaced."
cleaner = CleanText(text, stopwords=['replaced', 'advertisement', 'call'])
```

Once again calling ```print(cleaner.text)``` will provide you with a different result:

```python
go maybe definitely perhaps also using quotation marks
```

### Custom replacements

If you want to make sure that certain words get changed, perhaps from one verb form to another or something similar, you can do so using the `special_replacements` dictionary that can be provided in the ingestion phase. For example, using the same `text` variable as before:

```python
cleaner = CleanText(text, special_replacements={'advertisement': 'ad', 'quotation': 'bracket', 'call': 'give a ring'})
```

Once again calling ```print(cleaner.text)``` will provide you with a different result:

```python
ad give ring go maybe replaced definitely perhaps also using bracket marks replaced
```

*Note how the a from the "give a ring" in the replacement from the `special_replacement` dictionary has been removed. This is because the stopwords algorithm runs after your replacements have been made.*

## General settings

The standard settings in the package will:

- modify to your text:
  - make your text lowercase
  - expand contractions
  - remove stopwords
- remove elements of your text:
  - any hyperlinks
  - any digits
  - any emojis
  - any hashtags
  - any mentions (@usernames)
  - any punctuation

Any of those standards can be changed by modifying the "Standard Settings" at the top of the module file (`CleanText.py`):

| Setting             | If set to `True`
| -----------------   | --------------
| LOWER               | *Modifies* text to lowercase.
| EXPAND_CONTRACTIONS | *Modifies* text to expand any contractions (ex. `can't`, `won't`).
| REMOVE_STOPWORDS    | *Modifies* text to remove commonly occurring stopwords (ex. `I`, `you`, `me`).
| LINKS               | *Removes* any links in the text.
| DIGITS              | *Removes* any digits in the text.
| EMOJI               | *Removes* any emojies from the text.
| HASH                | *Removes* any hashtags from the text.
| AT                  | *Removes* any mentions of users from the text (ex. `@kallewesterling`)
| PUNCTUATION         | *Removes* any punctuation from the text.

You can also change those settings for each instantiation. Building on the example from above:

```python
cleaner = CleanText(text)
cleaner.lower = False
cleaner.clean()
```

*Note that if you change any settings this way, you need to re-run the `CleanText.clean()` method again, to clean the text that was ingested as the instance was created.*

To put what we learn above to the test, we can run:

```python
text = 'This is an Advertisement to Call # 222-109-1100 or go to http://www.apple.com. Maybe this will be replaced with definitely and perhaps also.'
cleaner = CleanText(text)
first_round = cleaner.text

cleaner.lower = False
cleaner.clean()
second_round = cleaner.text

print("Before:", first_round)
print("After:", second_round)
```

This should generate the following results:

```python
Before: advertisement call go maybe replaced definitely perhaps also
After: This Advertisement Call go Maybe replaced definitely perhaps also
```

## Future improvements

 ~~In the future, I want to remove the dependency on NLTK for stopwords and use a different, smaller package for this process. NLTK is too heavy for any users who do not need it.~~ The current version tries a different approach, [borrowed from YoastSEO](https://github.com/Yoast/YoastSEO.js/blob/develop/src/config/stopwords.js).