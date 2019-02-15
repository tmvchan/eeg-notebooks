"""
Generate N170
=============

Face vs. house paradigm stimulus presentation for evoking present.

Edited so that it takes arguments for ITI, SOA, and jitter.

"""

from time import time
from optparse import OptionParser
from glob import glob
from random import choice

import numpy as np
from pandas import DataFrame
from psychopy import visual, core, event
from pylsl import StreamInfo, StreamOutlet


def present(duration=120, iti=0.8, soa=0.2, jitter=0.2):

    # Create markers stream outlet
    info = StreamInfo('Markers', 'Markers', 1, 0, 'int32', 'myuidw43536')
    outlet = StreamOutlet(info)

    markernames = [1, 2]
    start = time()

    # Set up trial parameters
    n_trials = 2010
    # iti = 0.8
    # soa = 0.2
    # jitter = 0.2
    record_duration = np.float32(duration)

    # Setup trial list
    image_type = np.random.binomial(1, 0.5, n_trials)
    trials = DataFrame(dict(image_type=image_type,
                            timestamp=np.zeros(n_trials)))

    # Setup graphics

    def load_image(filename):
        return visual.ImageStim(win=mywin, image=filename)

    mywin = visual.Window([1600, 900], monitor='testMonitor', units='deg', winType='pygame',
                          fullscr=True)
    faces = list(map(load_image, glob(
        'stimulus_presentation/stim/face_house/faces/*_3.jpg')))
    houses = list(map(load_image, glob(
        'stimulus_presentation/stim/face_house/houses/*.3.jpg')))

    for ii, trial in trials.iterrows():
        # Intertrial interval
        core.wait(iti + np.random.rand() * jitter)

        # Select and display image
        label = trials['image_type'].iloc[ii]
        image = choice(faces if label == 1 else houses)
        image.draw()

        # Send marker
        timestamp = time()
        outlet.push_sample([markernames[label]], timestamp)
        mywin.flip()

        # offset
        core.wait(soa)
        mywin.flip()
        if len(event.getKeys()) > 0 or (time() - start) > record_duration:
            break
        event.clearEvents()

    # Cleanup
    mywin.close()


def main():
    parser = OptionParser()

    parser.add_option("-d", "--duration",
                      dest="duration", type='int', default=120,
                      help="duration of the recording in seconds.")
    
    # Added for easy editing of task parameters 14-2-19
    parser.add_option("-i", "--iti",
                      dest="iti", type='float', default=0.8,
                      help="time between stimuli in seconds.")
    
    parser.add_option("-s", "--soa",
                      dest="soa", type='float', default=0.2,
                      help="duration of stimulus presentation in seconds.")
    
    parser.add_option("-j", "--jitter",
                      dest="jitter", type='float', default=0.2,
                      help="average amount of random jitter added to ITI in seconds.")

    (options, args) = parser.parse_args()
    present(options.duration, options.iti, options.soa, options.jitter)


if __name__ == '__main__':
    main()
