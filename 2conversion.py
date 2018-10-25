from pretty_midi import PrettyMIDI, Instrument, Note
from pandas import read_csv

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

colnames = ['ws', 'bar', 'sst']  #columns of storm#.csv


def _scale(min_wd, max_wd, data, min_midi, max_midi):
    '''
    linear scaling
    '''
    return min_midi * (1 - (data - min_wd) / (max_wd - min_wd)) + max_midi * (
        (data - min_wd) / (max_wd - min_wd))


def data2midi(i, barmin, barmax, sstmin, sstmax, wsmin, wsmax):
    '''
    datalist = [time, barometric pressure, sea surface temperature, wind speed]
    notelist = [[time, pitch, volume, duration]]
    '''
    data = read_csv('storm' + str(i) + '.csv', names=colnames, header=1)
    ws = data.ws.tolist()
    bar = data.bar.tolist()
    sst = data.sst.tolist()

    sm = PrettyMIDI(initial_tempo=60)  #initialize midi
    inst = Instrument(program=1)
    sm.instruments.append(inst)

    #midi array [bar (velocity), sst (pitch), data (start), data + ws (end)]
    for data in range(len(ws)):

        barmidi = _scale(barmin, barmax, bar[data], 1 / (barmax - barmin), 1)  #volume
        sstmidi = _scale(sstmin, sstmax, sst[data], 1 / 127, 1 / 25)  #pitch
        wsmidi = _scale(wsmin, wsmax, ws[data], 1 / 32, 16)  #duration

        inst.notes.append(
            Note(
                round(1 / barmidi),  #volume
                round(1 / sstmidi),  #pitch
                data,  #start
                data + 1 / wsmidi))  #end

    #output track to midi
    sm.write('sonifystorm' + str(i) + '.mid')


for i in range(1, num + 1):
    '''
    breaks:
    5290.1 m/s wind speed
    802.2 mbar pressure
    '''
    data2midi(i, barmin, barmax, sstmin, sstmax, wsmin, wsmax)  # output: [pitch, beat, duration, volume]