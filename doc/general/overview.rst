********
Overview
********

The goal of this document is to provide a wide overview of the atcgen
including:

 - What is atcgen ?
 - How does atcgen works ?
 - How is atcgen source code structured ?


Definitions
###########


generator:
	In our context, a generator is a software which process the
	input of one or more karaoke related files (usually .lyr files for lyrics and
	.tim or .frm files for timings) to produce a subtitle file (usually .ass,
	.tass or .txt).



Principles
##########


Key Elements
************


Generator
=========
The ``Generator`` is the central part of atcgen, it compiles the data
from a lyrics & a timings file and use a renderer to export the result as a
subtitle file.


Context
-------
The ``context`` is a data structure holding the state of the generator
instance at any point during the generation process.
It's the data structure sent to the renderer after the compilation of the
lyrics & timing files.


Instructions
============
An ``Instruction`` is a special behaviour triggered by an
instruction line in the lyrics file. It can have multiple purposes such as
declaring a style, creating credit events or adding a passing effect to events.


Event
=====
An ``Event`` represents anything displayed by the generated subtitles when
read by a video player.

Event Component
---------------
An ``Event Component`` (or ``component``) represent a part of the text
contained in an event. It can represent displayed text (ex: a syllable) or an
in-line effect (ex: a logo, a fading effect, ...).
Each event can contain one or more components.


Style
=====
A ``Style`` represent the aspect the text will have in the subtitles when
read by a video player. A subtitle file can contains different styles.

Style Attribute
---------------
A ``Style Attribute`` (or ``attribute``) represent one aspect the Style.
Each attribute control one aspect of the style (ex: font size, color,
font name, outline size, ...).


Renderer
========
A ``Render`` process the data compiled during the processing of the
``Generator`` to convert it into a subtitle file.


Workflow
********


1. Init:
	The first step is to create a ``Generator`` instance.

	1. Setting of internal values:
		Upon creation, the ``Generator`` loads the ``instructions`` available
		in its ``instrutions_directory`` and the ``renderers`` available in
		its ``renderers_directory``.

	2. Load instructions:
		The ``Generator`` gather the instructions contained in the
		``instructions_directory``.

	3. Load renderers:
		The ``Generator`` gather the renderers contained in the
		``renderers_directory``.

2. The ``generate`` method:
	The generation process is started by the ``generate`` method of a
	``Generator`` instance.

	1. Reload the renderers and instructions which may have changed since the
		init of the generator instance.

	2. Run the ``_compile`` method.

		1 Init the ``context`` of the ``generator`` instance.
			The ``set_up``methods of the available instructions are executed,
			then, the ``context.post_init`` hooks are called.

		2 Prepare lyrics and timing data.
			Add the lyrics and timing data to the context.
			Initialize the parsers for lyrics and timings.

		3 Enter the compilation main loop.
			The compilation is done by iterating over the lines of the lyrics
			using the previously initialize lyrics parser to create the
			corresponding karaoke events.

			First a line is retrieved from the lyrics parser.

			If the line is an instruction, an instance of the corresponding
			instruction is created and it's ``process`` method is called.

			Else the generator checks if the line correspond to a lyrics line,
			if it does not, the line is ignored.

			If the line is a valid lyrics line the process continues.

			An ``Event`` is created, the ``event.pre_create`` and
			``event.post_create`` hooks are called respectively just before
			and right after this creation. The ``current_event`` attribute of
			the context is set to reference the newly created ``Event``.
			**In the case of the line is a
			continuation of a previous one this step is ignored**.

			The current style is registered as active.

			The compilation process the syllables of the lyrics line.

			A syllable ``Component`` is created, the ``component.pre_create``
			and ``component.post_create`` hooks are called respectively just
			before and right after this creation.

			The created ``Component`` is appended to the ``Event``'s components
			the ``component.pre_append`` and ``component.post_append`` hooks
			are called respectively just before and right after this insertion.

			Once all the syllabs are processed for the given lyrics line, the
			``Event`` is ready to be completed.

			When ``Event`` is completed, it's ```complete`` method is called.
			``event.pre_complete`` and ``event.post_complete`` hooks are called
			respectively just before and right after the method call.

			The event is then added to the list of processed events in the
			``context``.

			Then the loop start a new iteration with the next line.

	3. Rendering:
		Once the input files are compiled, the rendering step which will
		genrate the output file can start.
		In this step the generator instanciate the ``Renderer``  matching the
		requested output format and loaded during the "Init" phase.
		Then it calls it's ``render`` method with the ``context`` populated
		during the compilation.
		Then the output of the method is returned.


Source code
###########


Architecture
************

One of the main goals of atcgen is to provide a simple and easily extensible
code base. All the parts are stored in separate places as much as possible.


The ``Generator`` class manage the generation process.
When ``Generator`` is instanciated.


instructions
************

Instructions classes are located in the ``instruction`` folder.

renderers
*********

Renderers are located in the ``renderers`` folder.


.. raw:: pdf

	PageBreak oneColumn
