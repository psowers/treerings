from tridat.treerings import TreeRingSeries 

def read_rwl(filepath):
    """Read a raw decadal file into a list of TreeRingSeries."""
    # read file
    with open(filepath, 'r') as f:
        # pad each line to to ensure column breaks dont exceed line length
        lines = [l.rstrip().ljust(81) for l in f.readlines() if l.strip()]
    # define column breaks:
    #   site id (1-8), start year or decade (9-12),
    #   annual ring widths (size 6, columns 13-72)
    #   and extended id (74-80)
    indices = [0,8,12] + [i for i in range(18,67,6)] + [72, None]
    # instantiate a container for Tree Ring Series data
    series_group = {}
    for line in lines:
        # parse line
        id, yr, *rings = [line[indices[i]:indices[i+1]] for i in range(len(indices)-1)]
        id = id.strip()
        yr = int(yr)
        # separate extended id from rings list (columns 74-80)
        id_ext = rings.pop().strip()
        # format rings and check for sentinel value
        rings = [int(r.strip()) for r in rings if r.strip()]
        if rings[-1] in (-9999, 999):
            sentinel = rings.pop()
        else: 
            sentinel = None
        if yr % 10 == 0 and sentinel == None and len(rings) < 10:
            yr = yr + (10 - len(rings))
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
    ring_series = []
    for series in series_group.values():
        if not series['sentinel']:
            series['sentinel'] = -9999
        ring_series.append(
                TreeRingSeries(site_name = series['id'],
                    ring_widths = series['rings'],
                    start_year = series['decades'][0],
                    extended_id = series['id_ext'],
                    sentinel_value = series['sentinel']
                    )
                )

    # return list of TreeRingSeries
    return ring_series
