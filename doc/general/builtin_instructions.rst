..
	Generated at sphinx build. DO NOT EDIT.


************
Instructions
************

colour, colours, color, colors
==============================
Simple style declaration.

arguments: COLOUR_BEFORE COLOUR_DURING, COLOUR_AFTER

+-----------------+-----------------+-------------------------+
| argument name   | argument type   | description             |
+=================+=================+=========================+
| COLOUR_BEFORE   | RGB or RGBA     | SecondaryColour         |
|                 | hexadecimal     |                         |
|                 | sequences       |                         |
+-----------------+-----------------+-------------------------+
| COLOUR_DURING   | RGB or RGBA     | KaraokeColour           |
|                 | hexadecimal     |                         |
|                 | sequences       |                         |
+-----------------+-----------------+-------------------------+
| COLOUR_AFTER    | RGB or RGBA     | PrimaryColour           |
|                 | hexadecimal     |                         |
|                 | sequences       |                         |
+-----------------+-----------------+-------------------------+

Generated styles are named "Default#" where # is replaced by an increasing number to avoid collisions (starting at 1).

Examples:

::

    # declare a style with colours RED => GREEN => BLUE
    %colour FF0000 00FF00 0000FF

credit, credits
===============
Simple credit event generation.

arguments: START END TEXT

+-----------------+-----------------+-------------------------+
| argument name   | argument type   | description             |
+=================+=================+=========================+
| START           | timestamp in cs | begining of the event   |
+-----------------+-----------------+-------------------------+
| END             | timestamp in cs | end of the event        |
+-----------------+-----------------+-------------------------+
| TEXT            | text            | text to display         |
+-----------------+-----------------+-------------------------+

Create an event with the "Credit" style timed between START ANDEND.
A default "Credit" style is created if none exists when the line is processed).
If the "fading" effect is available, a ``fading 500 500`` is included.

Examples:

::

    # add a credit line at the begining of the video
    %credit 0 400 [Serie - Type]

effect
======
Manage event-level effects

available_effects:

cursor
------
Add a line of cursors matching the karaoke syllables.

Active by default.

arguments: STATUS

+-----------------+-----------------+-------------------------+
| argument name   | argument type   | description             |
+=================+=================+=========================+
| STATUS          | text            | 'y', 'yes', 't',        |
|                 |                 | 'true',                 |
|                 |                 | 'on' or '1' to enable   |
|                 |                 | the effect, 'n', 'no',  |
|                 |                 | 'f', 'false', 'off',    |
|                 |                 | or '0' to disable it.   |
+-----------------+-----------------+-------------------------+

If the cursor is disabled or (re-enabled) in the middle of an event, place-holder components are inserted to avoid misalignment of syllables.

Examples:

::

    # disable the cursor
    %effect cursor off

fading
------
Add a fade in and fade out effect to the events.

Active by default with presets:
  - fade in duration: 750ms
  - fade out duration: 500ms
  - fade in delay: -100cs
  - fade out delay: 50cs

arguments: FADEIN_DURATION FADEOUT_DURATION FADEIN_DELAY FADEOUT_DELAY

+------------------+-----------------+------------------------+
| argument name    | argument type   | description            |
+==================+=================+========================+
| FADEIN_DURATION  | integer (in ms) | Duration of the fade   |
|                  |                 | in effect              |
+------------------+-----------------+------------------------+
| FADEOUT_DURATION | integer (in ms) | Duration of the fade   |
|                  |                 | in effect              |
+------------------+-----------------+------------------------+
| FADEIN_DELAY     | integer (in cs) | Shift the beginning    |
|                  |                 | of the event to avoid  |
|                  |                 | overlapping fading     |
|                  |                 | effect and sung        |
|                  |                 | syllables.             |
+------------------+-----------------+------------------------+
| FADEOUT_DELAY    | integer (in cs) | Shift the end of       |
|                  |                 | the event to avoid     |
|                  |                 | overlapping fading     |
|                  |                 | effect and             |
|                  |                 | sung syllables.        |
+------------------+-----------------+------------------------+

If the cursor is disabled or (re-enabled) in the middle of an event, place-holder components are inserted to avoid misalignment of syllables.

Examples:

::

    # at apparition text fade in for 0.75s
    # then stays still for 0.25s
    # then is sung
    # then disappear in a fade out during 0.5s
    %effect fading 750 500 -100 50

move
----
Move an event text across the screen.

arguments: STATUS X_START Y_START X_END Y_END

+-----------------+-----------------+-------------------------+
| argument name   | argument type   | description             |
+=================+=================+=========================+
| STATUS          | text            | 'y', 'yes', 't',        |
|                 |                 | 'true',                 |
|                 |                 | 'on' or '1' to enable   |
|                 |                 | the effect, 'n', 'no',  |
|                 |                 | 'f', 'false', 'off',    |
|                 |                 | or '0' to disable it.   |
+-----------------+-----------------+-------------------------+
| X_START         | integer         | X coordinate at the     |
|                 |                 | beginning               |
+-----------------+-----------------+-------------------------+
| Y_START         | integer         | Y coordinate at the     |
|                 |                 | beginning               |
+-----------------+-----------------+-------------------------+
| X_END           | integer         | X coordinate at the     |
|                 |                 | end                     |
+-----------------+-----------------+-------------------------+
| Y_END           | integer         | Y coordinate at the     |
|                 |                 | end                     |
+-----------------+-----------------+-------------------------+

(x=0 ; y=0) correspond to the top left corner.
Reference coordinate of the text depends on its Alignment.

Examples:

::

    # move event from top left to bottom right
    %effect move on 0 0 1280 720

passing
-------
make the event text scroll horizontally across the screen.

arguments: STATUS DIRECTION ARRIVAL_DISTANCE ARRIVAL_DELAY DEPARTURE_DISTANCE DEPARTURE_DELAY

+--------------------+---------------+------------------------+
| argument name      | argument type | description            |
+====================+===============+========================+
| STATUS             | text          | 'y', 'yes', 't',       |
|                    |               | 'true',                |
|                    |               | 'on' or '1' to enable  |
|                    |               | the effect, 'n', 'no', |
|                    |               | 'f', 'false', 'off',   |
|                    |               | or '0' to disable it.  |
+--------------------+---------------+------------------------+
| DIRECTION          | integer       | '0' for right to left, |
|                    |               | '1' for left to right. |
|                    |               |                        |
+--------------------+---------------+------------------------+
| ARRIVAL_DISTANCE   | integer       | Y coordinate from the  |
|                    |               | arriving edge of the   |
|                    |               | event, at              |
|                    |               | ARRIVAL_DELAY          |
|                    |               | milliseconds after the |
|                    |               | event begins.          |
+--------------------+---------------+------------------------+
| ARRIVAL_DELAY      | integer       | time in milliseconds   |
|                    | (in ms)       | between the event      |
|                    |               | beginning and its      |
|                    |               | arrival at             |
|                    |               | ARRIVAL_DISTANCE       |
+--------------------+---------------+------------------------+
| DEPARTURE_DISTANCE | integer       | Y coordinate from the  |
|                    |               | departing edge of the  |
|                    |               | event, at              |
|                    |               | DEPARTURE_DELAY        |
|                    |               | milliseconds before    |
|                    |               | the event ends.        |
+--------------------+---------------+------------------------+
| DEPARTURE_DELAY    | integer       | time in milliseconds   |
|                    | (in ms)       | between the event      |
|                    |               | end and its            |
|                    |               | departure from         |
|                    |               | DEPARTURE_DISTANCE     |
+--------------------+---------------+------------------------+

Reference coordinate of the text depends on its Alignment.

Examples:

::

    # text scroll from right of the screen to the left
    %effect passing on 0 500 500 500 500

position
--------
Force event text position on the screen.

arguments: STATUS X Y

+---------------+---------------+-----------------------------+
| argument name | argument type | description                 |
+===============+===============+=============================+
| STATUS        | text          | 'y', 'yes', 't', 'true',    |
|               |               | 'on' or '1' to enable       |
|               |               | the effect, 'n', 'no',      |
|               |               | 'f', 'false', 'off',        |
|               |               | or '0' to disable it.       |
+---------------+---------------+-----------------------------+
| X             | integer       | X coordinate                |
+---------------+---------------+-----------------------------+
| Y             | integer       | Y coordinate                |
+---------------+---------------+-----------------------------+

(x=0 ; y=0) correspond to the top left corner.
Reference coordinate of the text depends on its Alignment.

Examples:

::

    # display text at 190 110
    %effect position on 190 110

snap
----
Snap successive syllables with close enough timings.

Active by default.
arguments: VALUE

+---------------+---------------+-----------------------------+
| argument name | argument type | description                 |
+===============+===============+=============================+
| VALUE         | integer       | Maximum timing difference   |
|               |               | to snap                     |
+---------------+---------------+-----------------------------+

Snaping is done by moving the beginning of the syllable at the centisecond following the end of the previous syllable.

Examples:

::

    # disable snapping
    %effect snap 0

info
====
Declare subtitle file global information.

arguments: NAME VALUE

+---------------+---------------+-----------------------------+
| argument name | argument type | description                 |
+===============+===============+=============================+
| NAME          | text          | Name of the info variable   |
|               |               | to declare                  |
+---------------+---------------+-----------------------------+
| VALUE         | text          | Value of the declared       |
|               |               | variable                    |
+---------------+---------------+-----------------------------+

The "script_info.ini" file stored in the generator containssome pre-declared informations.
/!\ script infos act on the whole subtitle file no matter hisposition in the lyr.

Examples:

::

    # disable ligatures
    %info Ligatures 0

style
=====
Declare and/or activate styles.

arguments: NAME_AND_PARENT ATTRIBUTES...

+----------------+--------------------------------+-----------+
| argument name  | argument type                  |description|
+================+================================+===========+
| NAME_AND_PARENT| text                           |  Name of  |
|                |                                |  the style|
|                |                                |  & name   |
|                |                                |  of its   |
|                |                                |  parent   |
|                |                                |  (if any) |
|                |                                |  separated|
|                |                                |  by a     |
|                |                                |  colon    |
|                |                                |  (':')    |
+----------------+--------------------------------+-----------+
| ATTRIBUTES     |zero or more groups of text     | A sequence|
|                |formatted like                  | of        |
|                |'ATTRIBUTE_NAME=ATTRIBUTE_VALUE'| attributes|
|                |ATTRIBUTE_VALUE can be a        | to define |
|                |quoted text if it has           | for the   |
|                |to contain white spaces         | newly     |
|                |                                | created   |
|                |                                | style.    |
|                |                                | If empty  |
|                |                                | and the   |
|                |                                | style name|
|                |                                | already   |
|                |                                | exists,   |
|                |                                | set the   |
|                |                                | style     |
|                |                                | as the    |
|                |                                | active    |
|                |                                | style.    |
+----------------+--------------------------------+-----------+

A "parent" is a styles which the newly created style is derived from the newly created style attributes have the same values as the ones in the parent, except for the attributes redefined in the attribute sequence of the child declaration.

Attributes list:
  - Fontname
  - Fontsize
  - PrimaryColour
  - SecondaryColour
  - KaraokeColour
  - OutlineColour
  - BackColour
  - Bold
  - Italic
  - Underline
  - StrikeOut
  - ScaleX
  - ScaleY
  - Spacing
  - Angle
  - BorderStyle
  - Outline
  - Shadow
  - Alignment
  - MarginL
  - MarginR
  - MarginV
  - Encoding

The "Styles.ini" file stored in the generator contains some pre-declared styles.

Examples:

::

    # declare a style named "Main"
    %style Main Alignment=8 PrimaryColour=&H0003FF31 SecondaryColour=&H002522FF KaraokeColour=&H0040FFEC
    # declare a style derived from "Main" named "Choir"
    # with diffrent colours and Alignment
    %style Choir:Main Alignment=2 PrimaryColour=&H00310FF3 SecondaryColour=&H002FF225 KaraokeColour=&H00ECFF40
