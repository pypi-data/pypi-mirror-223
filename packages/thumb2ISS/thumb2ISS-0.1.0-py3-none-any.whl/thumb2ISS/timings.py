#
# Copyright (c) 2023 Thibaut Zeissloff.
#
# This file is part of Thumb2ISS
# (see https://github.com/TZe-0xff/thumb2ISS).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#
from collections import defaultdict

class Architecture:
    CortexM0 = 0
    CortexM0p= 1
    CortexM3 = 2
    CortexM4 = 3
    CortexM23= 4
    CortexM33= 5

    @staticmethod
    def fromString(s):
        if '0+' in s or '0p' in s:
            return Architecture.CortexM0p
        elif '23' in s:
            return Architecture.CortexM23
        elif '33' in s:
            return Architecture.CortexM33
        elif 'M0' in s:
            return Architecture.CortexM0
        elif 'M3' in s:
            return Architecture.CortexM3
        elif 'M4' in s:
            return Architecture.CortexM4


class Timings:
    core_specific_timings = {
        Architecture.CortexM0 : 
            {'MULS': 32, 'BL' : 2, 'MRS': 4, 'MSR' : 4, 'branchpenalty' : 2},

        Architecture.CortexM0p : 
            {'BL' : 2, 'MRS': 3, 'MSR' : 3, 'branchpenalty' : 1},

        Architecture.CortexM3 : 
            {'MLA' : 2, 'MLS' : 2, 'SMULL' : 5, 'UMULL' : 5, 'SMLAL' : 7, 'UMLAL' : 7, 'SDIV': 12, 'UDIV': 12, 'TBB' : 3, 'TBH': 3,  'MRS': 3, 'MSR' : 3, 'branchpenalty' : 2},

        Architecture.CortexM4 : 
            {'MLA' : 2, 'MLS' : 2, 'SDIV': 12, 'UDIV': 12, 'TBB' : 3, 'TBH': 3,  'MRS': 3, 'MSR' : 3, 'branchpenalty' : 2},
    }

    def __init__(self, arch):
        spec_tm = self.core_specific_timings.get(arch, {'branchpenalty' : 3})

        self._branch_penalty = spec_tm['branchpenalty']
        self._cycle_per_mnem = spec_tm

    def getTiming(self, mnem, address):
        if mnem.upper() in ['IT', 'NOP']:
            if address & 3 == 2:
                # loaded with previous thumb instruction, 0 cycles
                return 0

        return self._cycle_per_mnem.get(mnem.upper(), 1)
