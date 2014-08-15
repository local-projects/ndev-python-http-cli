## Overview

The instructions here mirror http://nuancedev.github.io/samples/http/python/

## Installation

Use the requirements.txt file to perform installations, but there are some pre-requisites:

For OSX:

    brew install portaudio
    brew install libsndfile
    brew install libsamplerate


## Troubleshooting and Tips

If you have issues with pip installation, particularly pip version 1.5.x+, try the following:

    pip install --allow-all-external --allow-unverified pyaudio pyaudio
