# ct-analysis
CryptoTwitter-Analysis 

This is the place for the devolpment of my first text/sentiment analysis. The idea is to build multiple pipelines/automations to send a report of all the tweets seen on a crypto twitter account. This way a user will get some kind of summary of the info seen on it's timeline. 

## Focus points
### Daily or an other (short) frequency (short range data)
- extract tweets of the accounts that are followed by the useraccount.
- store the summary information about the seen tweets in a standardised format.

### Weekly or other (longer) frequency (long range data)
- combine the short range data to one larger long range dataset.
- generate a report on the long range dataset.
- send this report to specified email adresses.


## Summarry data
The following ideas are the result of some active brainstorming.

All records MUST to have a timestamp.

The summarry info that needs to be stored, or the info the needs to be reported, are:
- the counts of the tickers ($) that are mentioned (total, total + different accounts, frequency of total mentions (num mentions/hour), max frequency of mentions sort by user (num mentions/hour) <-- in second case also mention the account names);
- sentiment of the tweets/mentions of the ticker mentions;

## Report information
The following ideas are the result of some active brainstorming.

The content of the report can change over time to the needs of the user.

The long range report has to contain some of the following:
- the counts of the tickers ($) that are mentioned (total, total + different accounts, frequency of total mentions (num mentions/hour), max frequency of mentions sort by user (num mentions/hour) <-- in second case also mention the account names);
- sentiment of the tweets/mentions of the ticker mentions;
- (maybe) an analysis of the new tickers that are mentioned, their counts and seen sentiment.
- (maybe) add a general sentiment (lunarcrush data or some) as somewhat of a general benchmark.
