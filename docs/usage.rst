=====
Usage
=====

Launching
=========

If you installed the `snap <https://uappexplorer.com/app/mountain-tapir.tttppp>`_, then you can launch with::

    mountain-tapir

To launch Mountain Tapir Collage Maker from the command line::

    python -m mountain_tapir.mountain_tapir

Assuming Mountain Tapir has write access then a configuration file will be stored in::

    [user home]/.mountain_tapir/mountain_tapir.properties

User Interface
==============

At the top of the UI is a section containing recently used images. Initially this just contains a button labelled "Clear", but once a few images have been loaded then thumbnails can be selected here to allow filling regions by clicking.

The middle of the UI contains a preview of what the finished collage will look like. When a region is empty then it has a random solid colour to help distinguish it from neighbouring regions. This solid colour block will not appear in the final output.

At the bottom of the UI are several buttons representing different tools and methods of changing the layout of the collage.

Tools
-----

Load: This tool is selected when the application is first started, and causes a file selection dialog to appear when clicking on a region. The selected file (assuming it's an image file) will be loaded into that region.

Swap: When this tool is selected then the images in two regions can be swapped by clicking on one then the other.

Empty: Using this tool the current image in a region can be removed by clicking on it.

Rotate: When this tool is selected then clicks on an image will cause it to be rotated by ninety degrees. It will also cause any copies of the image to be rotated by ninety degrees too (a "copy" is created using the thumbnails at the top, using the Load button will create a separate version of the image).

Shuffle: Clicking this button will randomly rearrange the images within the regions (while keeping the layout the same).

Layout
------

Collage: Clicking this button converts the collage to the default "Collage" mode - i.e. a slightly random arrangement of rectangles. When in collage mode this button can be used to create a new arrangement of regions.

Grid: Clicking this button converts the collage to a grid of regions. All regions will be the same width and height.

Frame: This button generates a collage with a central picture surrounded by a border of other images. Note that if there are fewer than five regions then this uses grid mode instead.

Width and Height: These settings control the resolution in pixels of the finished collage.

-/+ regions: This controls the number of regions in the collage.

Save: This generates the finished collage, and saves it to a specified file. The default file extension is "\*.jpg", but other file formats can be chosen too.
