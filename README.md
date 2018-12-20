# Trololo

CLI program for Trello hacks.

Program is called "Edward", by the name
of famous Soviet singer [Edward Khil](https://en.wikipedia.org/wiki/Eduard_Khil), who performed vocalise ["Trololo"](https://www.youtube.com/watch?v=OfaCTg_2les)
(I am very happy because I am finally back home).

## Requirements

For general use and packaging Python 3.5+ is required.

For running unit tests, PyTest is required.


# Usage

Everything currently should be executed in the current directory,
unless packaged otherwise.

## Setup

You should obtain Trello API key and API tokens, also know your Trello
UID name. Copy `edward.conf.sample` to `edward.conf` in the same
directory and update it with the earlier mentioned data.

## Accessing Trello elements

Normally Trello elements are accessed by their IDs. However, the more
data is navigated and explored, the more data "edward" collects into
file `edward.bin`, which is currently in the current directory. This
file can be safely deleted and is created automatically.

For example, to navigate a board by names/strings instead by IDs, you
have to let Edward collect all the items. This is possible to simply
display the entire board map. First you have to find the board:

```
./edward board -s
```

E.g. the above command had returned something like this:

```
--------------------------------------------------------------------------------
01. test board
Id: 6c193462e6c51b35708ce3df
--------------------------------------------------------------------------------
```

At this point it is possible to issue:

```
./edward board -d 6c193462e6c51b35708ce3df

```

But it is also now possible to issue this:

```
./edward board -d "test board"
```

At this point Edward now knows about the entire board, and now it is
possible to e.g. list cards in the list or comments in the card:


```
./edward card -s "Card with comments"
```

Please note that Edward is looking for partial string from the
beginning or the entire string (up to you).


## Adding labels

In order to add a label, they need to be already defined in the
board. First you need to know what kind of labels you have:

```
./edward -l "test board"
```

This will return you a list of labels with their IDs. If the labels
has also text in it, you will be lucky accessing them by
name. Otherwise please use IDs.

## Adding a card

In order to add a card, you need to know where you're adding it
to. You can either specify a name or part of it of the list, or
specify an exact ID:

```
./edward card -a "Some list" -t "Prio" -e "Hi there" -d "Something"
```

In this case we are also optionally adding the label, called
"Prio".

## Adding a comment

To add a comment, you should tell Edward to what card it should add
it:

```
./edward card -c "This is my comment :wink:" -i 5c193c97d3f2f04aa254c238
```

Or do the same by name (experimental):

```
./edward card -c "This is my comment :wink:" -i "Another card"
```

## Bonus feature

Comma-separated IDs are also supported. If you pass them so, then the
operation will be applied to multiple objects. This is working only if
passed IDs (not strings/names).

For example, if you want to add the same card twice to a different
boards/lists, simply define different IDs, as so:

```
./edward card -a 5c198c658f58123c4191cf0e,5c1b806789df345fd746730 \
    -t "Prio" -e "Hi there" -d "Something"

```
