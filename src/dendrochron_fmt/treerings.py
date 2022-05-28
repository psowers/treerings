"""TreeRingSeries Doc string. 
"""

class TreeRingSeries:

    # add init later

    @classmethod
    def from_rwl(cls, filepath):
        """Read a raw decadal file into a list or TreeRingSeries."""
        # read file
        with open(filepath, 'r') as f:
            # pad each line to to ensure column breaks dont exceed line length
            lines = [l.rstrip().ljust(81) for l in f.readlines()]
        # define column breaks:
        #   site id (1-8), start year or decade (9-12),
        #   annual ring widths (mm)(size 6, columns 13-72)
        #   and extended id (74-80)
        indices = [0,8,12] + [i for i in range(18,67,6)] + [72, None]
        # instantiate a container for Tree Ring Series data
        series_group = {}
        for line in lines:
            # parse line
            id, yr, *rings = [line[indices[i]:indices[i+1]] for i in range(len(indices)-1)]
            # separate extended id from rings list (columns 74-80)
            id_ext = rings.pop().strip()
            # format rings and check for sentinel value
            rings = [int(r.strip()) for r in rings if r.strip()]
            if rings[-1] in (-9999, 999):
                sentinel = rings.pop()
            else: 
                sentinel = None
            if yr % 10 == 0 and sentinel == None and len(rings) < 10:
                yr = yr + len(rings) 
            # append ring widths to existing series, or add a new series
            if id in series_group:
                series_group[id]['decades'].append(yr)
                series_group[id]['rings'].extend(rings)
                series_group[id]['id_ext'].append(id_ext)
                series_group[id]['sentinel'] = sentinel
            else:
                series_group[id] = {
                        'id': id,
                        'decades': [yr,], 
                        'rings': rings,
                        'id_ext': [id_ext,],
                        'sentinel': sentinel
                    }
        # final series formatting
        for series in series_group.values():
            sentinel = series['sentinel']
            if sentinel == 999:
                series['to_float'] = lambda x: x * 0.01
            elif sentinel == -9999: 
                series['to_float'] = lambda x: x * 0.001
            elif not sentinel:
                series['sentinel'] = -9999
                series['to_float'] = lambda x: x * 0.001
        # return list of TreeRingSeries
