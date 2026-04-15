# define

If there is no photo attached, this should be consider an error and no further action taken.  If there is a photo attached, it will be a screenshot of a definition from the Zanichelli website.  Read the contents of the photo, which will be the definition.  Actually read the text of the photo.  Do not assume, do not skim, do not make it up or otherwise invent the text of the screen shot.  If you are unable to read the image yourself or are confused, check if tesseract is availble on the local system and try using it to read the image.  Do not try checking online resources for a definition.  From this point, there are two possible courses of action -

1. If the there is not a file matching the word, create a new file under the vocabulario folder, with a name that matches the word (minus any accents), and add the vocabulary entry to that file following the structure of schema.json, which is also found in the vocabulary folder.  Do not try to populate the hints section.  Do not change glosses, phrases, or examples except to fix typos.  Do not attempt to add information to the glosses, phrases, or typos.  Only use the text from the image.

2.  If there is already a file with a matching name, ensure the glosses, examples, and phrases match the text found in the image.  Do not try to add information not found in the image unless there is a typo.  Do not attempt to readd any glosses, examples, or phrases that may have been deleted.  Inform the user of this missing information and allow the user to make the choice to readd the missing information.

The following are general consideration when dealing with the definitions -

1. The syllables (syl according the schema.json) should include the accent found in the headword.
2. Hints should always be left null

This command will be available in chat with /define
