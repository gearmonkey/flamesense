flamesense
==========
Using sentiment tools to judge other people's conversations since 2011.

firealarm.py
------------
This is a simple commandline script that works with [@jwheare](http://twitter.com/jwheare)'s [exquistietweets](http://exquisitetweets.com) tweet conversation archive to determine how nasty a conversation is and where it all went wrong.

Uses the [sentiment analyzer api](http://musicmetric.com/sf-api) from [Musicmetric](http://musicmetric.com) to determine if tweets are positive, neutral or negative and declares the troll to be the author of the largest single downward shift in tone across the conversation.

Note that to get the script running you need to [apply for a musicmetric api key](https://secure.semetric.com/sf-api-signup) and put your key in `apikey.py`

Not sure where to start?  After putting your key in the right place try running 

`$python firealarm.py http://www.exquisitetweets.com/collection/atl/410`