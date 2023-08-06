
# slugify_python

```py
import slugify

slugify.slugify('some string')  # some-string

# If you prefer something other than '-' as the separator
slugify.slugify('some string', '_')  # some_string
```

- Written in Python
- No external dependencies
- Coerces foreign symbols to their English equivalent (check out the charMap for more details)


## Options

```py
slugify.slugify('some string', {
  'replacement': '-',  # Replace spaces with the replacement character (default is '-')
  'remove': None,      # Remove characters that match the regex (default is None)
  'lower': False,      # Convert to lowercase (default is False)
  'strict': False,     # Strip special characters except replacement (default is False)
  'locale': 'vi',      # Language code of the locale to use
  'trim': True         # Trim leading and trailing replacement characters (default is True)
})
``` 

## Remove

For example, to remove *+~.()'"!:@ from the result slug, you can use slugify.slugify('..', {'remove': r'[*+~.()'"!:@]'}).

* If the value of remove is a regular expression, it should be a character class with the global flag (e.g., r'[*+~.()'"!:@]'). Otherwise, the remove option might not work as expected.

* If the value of `remove` is a string, it should be a single character.
  Otherwise, the `remove` option might not work as expected.

## Locales

The main `charmap.json` file contains all known characters and their transliteration. All new characters should be added there first. In case you stumble upon a character already set in `charmap.json`, but not transliterated correctly according to your language, then you have to add those characters in `locales.json` to override the already existing transliteration in `charmap.json`, but for your locale only.

You can get the correct language code of your language from [here](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes).

## Extend

Out of the box `slugify` comes with support for a handful of Unicode symbols. For example the `☢` (radioactive) symbol is not defined in the [`charMap`][charmap] and therefore it will be stripped by default:

```py
slugify('unicode ♥ is ☢') // unicode-love-is
```

However you can extend the supported symbols, or override the existing ones with your own:

```py
slugify.extend({'☢': 'radioactive'})
slugify('unicode ♥ is ☢') // unicode-love-is-radioactive
```

Keep in mind that the `extend` method extends/overrides the default `charMap` for the entire process. In case you need a fresh instance of the slugify's `charMap` object you have to clean up the module cache first:

```py
delete require.cache[require.resolve('slugify')]
var slugify = require('slugify')
```
