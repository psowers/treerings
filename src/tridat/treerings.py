"""TreeRingSeries Doc string. 
"""

class TreeRingSeries:

    def __init__(self, site_name, 
            ring_widths, 
            start_year, 
            extended_id=None, 
            sentinel_value=None):
        self.site_name = site_name
        self.ring_widths = ring_widths
        self.start_year = start_year
        self.extended_id = extended_id
        self.sentinel_value = sentinel_value
        if self.sentinel_value == 999:
            self.mm_conversion = lambda x: x * 0.01
        elif self.sentinel_value == -9999: 
            self.mm_conversion = lambda x: x * 0.001
        else:
            self.mm_conversion = lambda x: x 


