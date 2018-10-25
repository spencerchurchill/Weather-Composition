from pandas import read_csv, DataFrame

'''
Spencer Churchill
10/19/18
'''

hours = 156  #156 hours before and after hurricane

colnames = ['buoy', 'ws', 'bar', 'sst']  #columns of data.csv

data = read_csv('data.csv', header=2, delimiter=',', names=colnames, dtype={'buoy' : str, 'ws' : float, 'bar' : float, 'sst' : float}, low_memory=True)
buoy = data.buoy.tolist()
ws = data.ws.tolist()
bar = data.bar.tolist()
sst = data.sst.tolist()

storm = {'ws': [], 'bar': [], 'sst': []}
stormcp = {'ws': [], 'bar': [], 'sst': []}


def _stormappend(storm, i):
    storm['ws'].append(ws[i])
    storm['bar'].append(bar[i])
    storm['sst'].append(sst[i])


i = 0
num = 1
while i < len(buoy):
    if ws[i] >= 33 and buoy[i] == buoy[i - hours]:
        j = i
        while i <= j + hours:
            _stormappend(storm, i)
            i += 1
        stormcp['ws'] = storm['ws'][j - hours:j + hours]
        stormcp['bar'] = storm['bar'][j - hours:j + hours]
        stormcp['sst'] = storm['sst'][j - hours:j + hours]
        if buoy[j + hours] == buoy[j - hours]:
            stormdf = DataFrame(stormcp, columns=['ws', 'bar', 'sst']).dropna()
            if stormdf.empty == False:
                stormdf.to_csv('storm' + str(num) + '.csv', encoding='utf-8', index=False)
                print('i='+str(i)+' '+'num='+str(num))
                num += 1
    else:
        _stormappend(storm, i)
    i += 1