from pretty_midi import PrettyMIDI, Instrument, Note
from pandas import read_csv

#Spencer Churchill
#10/6/18
#
#FOR PRESENTATION

num = 1  #number of csv's

colnames = ['ws', 'bar', 'sst']  #columns of storm#.csv


def _scale(min_wd, max_wd, data, min_midi, max_midi):
    #linear scaling
    
    return min_midi * (1 - (data - min_wd) / (max_wd - min_wd)) + max_midi * (
        (data - min_wd) / (max_wd - min_wd))


def data2midi(i):
    #datalist = [time, barometric pressure, sea surface temperature, wind speed]
    #notelist = [[time, pitch, volume, duration]]

    data = read_csv('storm' + str(i) + '.csv', names=colnames, header=1)
    ws = data.ws.tolist()
    bar = data.bar.tolist()
    sst = data.sst.tolist()

    sm = PrettyMIDI(initial_tempo=60.0)  #initialize midi
    inst = Instrument(program=27)  # 1 is piano, 27 is jazz guitar
    sm.instruments.append(inst)

    #midi array [bar (velocity), sst (pitch), data (start), data + ws (end)]
    for data in range(len(ws)):

        barmidi = _scale(min(bar), max(bar), bar[data], 1 / 127, 1 / 35)  #volume
        sstmidi = _scale(min(sst), max(sst), sst[data], 1 / 110, 1 / 30)  #pitch
        wsend = _scale(min(ws), max(ws), ws[data], 1 / 4, 16)  #duration

        inst.notes.append(
            Note(
                round(1 / barmidi),  #volume
                round(1 / sstmidi),  #pitch
                data / 2.6,  #start
                data / 2.6 + 1 / wsend))  #end

    #output track to midi
    sonify = 'sonifystorm' + str(i)
    sm.write(sonify + '.mid')

    print("\nSonification " + str(i) + " Complete...\n")


for i in range(1, num + 1):
    #breaks:
    #5290.1 m/s wind speed
    #802.2 mbar pressure
    data2midi(i)  # output: [pitch, beat, duration, volume]