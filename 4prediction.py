from pretty_midi import PrettyMIDI

'''
Spencer Churchill
10/6/18
'''

num = 1  #number of csv's

wsmin = 0.0
wsmax = 96.0
barmin = 800.7
barmax = 1110.0
sstmin = 0.0
sstmax = 50.0


def _invscale(min_wd, max_wd, data, min_midi, max_midi):
    return (-1 * min_wd * max_midi + min_wd * data + max_wd * min_midi -
            max_wd * data) / (min_midi - max_midi)


#given midi, convert back to weather data
def midi2data(i, barmin, barmax, wsmin, wsmax):
    file = 'predict' + str(i) + '.mid'
    midi = PrettyMIDI(file)

    dur = []
    vel = []
    for k in range(len(midi.instruments[0].notes)):
        dur.append(midi.instruments[0].notes[k].end -
                   midi.instruments[0].notes[k].start)
        vel.append(midi.instruments[0].notes[k].velocity)

    maxws = _invscale(wsmin, wsmax, 1 / min(dur), 1 / 32, 16)
    minbar = _invscale(barmin, barmax, 1 / max(vel), 1 / (barmax - barmin), 1)

    pretime = min(midi.instruments[0].notes[dur.index(min(dur))].start,
                  midi.instruments[0].notes[vel.index(max(vel))].start)

    #Saffir-Simpson Hurricane Wind Scale
    if maxws < 33:
        cat = 0
    elif maxws >= 33  and maxws < 43:
        cat = 1
    elif maxws >= 43 and maxws < 50:
        cat = 2
    elif maxws >= 50 and maxws < 58:
        cat = 3
    elif maxws >= 58 and maxws < 70:
        cat = 4
    elif maxws >= 70:
        cat = 5
    else:
        return -1

    print("Catagory " + str(cat) + " Storm Prediction in " +
          str(round(pretime, 1) + 1) + " hour(s)\n   Wind Speed: " +
          str(round(maxws, 1)) + " m/s\n   Barometric Pressure: " +
          str(round(minbar, 1)))


for i in range(1, num + 1):
    '''
    breaks:
    5290.1 m/s wind speed
    802.2 mbar pressure
    '''
    midi2data(i, barmin, barmax, wsmin, wsmax)  # output: prediction