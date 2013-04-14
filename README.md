# Sebastian

**Sebastian** is a symbolic music analysis and composition library written in
Python.

I partly think of it as being a "Mathematica for music". By symbolic, I mean
that it is focused more on the sorts of abstractions made by music notation
and theories of harmony and counterpoint than lower level numerical
operations that one might use in, say, music synthesis.

I hope it to be very practical as an analysis tool for existing compositions
(especially from the common practice period) and also a tool for
computer-assisted composition. It will also be a bit of a test bed for ideas
I've had for a while around applying linguistics and abstract algebra to
music.

## PyCon 2013 Talk

I spoke about Sebastian at PyCon 2013 and my slides are available at:

<https://speakerdeck.com/jtauber/music-theory-and-performance-analysis-with-sebastian-and-czerny>

The video of the talk is available on YouTube at:

<http://www.youtube.com/watch?v=06h21nBqwec>

## Mailing List

You can join the Sebastian mailing list by emailing `sebastian@librelist.com`

## IRC Channel

We're using `#sebastian-dev` on Freenode.

## License

Sebastian is open source under an MIT license. See the LICENSE file.

## Running Tests

    pip install nose
    nosetests

or with coverage:

    nosetests --with-coverage --cover-erase --cover-package=sebastian --cover-html
    open cover/index.html

## IPython Notebook Integration

    pip install ipython
    pip install tornado
    pip install pyzmq
    
and install Lilypond, making sure commandline `lilypond` is on your path then:

    ipython notebook
