Data aware blits.

python data_aware_blits.py


Just a demo to prove that data aware blit can improve performance.

This only shows off the case where there is a transparent image.

Instead of using a single blitter for the whole image,
we use a specialised one for each piece of the data.

I call this data aware blit/JIT.


There are other options as well.

Including::

    * 8 bit RLE encoded sub surfaces
    * pure fill colours.

Additionally this could test which types of blit routines are
quicker on the particular hardware being used. What is the fast path?


zlib license
