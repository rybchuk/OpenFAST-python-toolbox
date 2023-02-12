class AMRWindSimulation:
    '''
    This class is used to help prepare sampling planes for an AMR-Wind
      simulation. The sampling planes will be used to generate inflow
      data for FAST.Farm simulations.
    Specifically, this class contains info from the AMR-Wind input file
    '''

    def __init__(self, dt: float, prob_lo: tuple, prob_hi: tuple, 
                    n_cell: tuple, max_level: int, 
                    incflo_velocity_hh: tuple, 
                    postproc_name='sampling'):
        '''
        Values from the AMR-Wind input file
        Inputs:
          * dt: this should be a fixed dt value
          * incflo_velocity_hh: velocity vector, specifically at hub height
        '''
        self.dt = dt
        self.prob_lo = prob_lo
        self.prob_hi = prob_hi
        self.n_cell = n_cell
        self.max_level = max_level
        self.incflo_velocity_hh = incflo_velocity_hh
        self.postproc_name = postproc_name

        self._checkInputs()

    def _checkInputs(self):
        '''
        Check that the AMR-Wind inputs make sense
        '''
        if len(self.prob_lo) != 3:
            raise ValueError(f"prob_lo must contain 3 elements, but it has {len(self.prob_lo)}")
        if len(self.prob_hi) != 3:
            raise ValueError(f"prob_hi must contain 3 elements, but it has {len(self.prob_hi)}")
        if len(self.incflo_velocity_hh) != 3:
            raise ValueError(f"incflo_velocity_hh must contain 3 elements, but it has {len(self.incflo_velocity_hh)}")
        if (self.prob_lo[0] >= self.prob_hi[0]):
            raise ValueError("x-component of prob_lo larger than x-component of prob_hi")
        if (self.prob_lo[1] >= self.prob_hi[1]):
            raise ValueError("y-component of prob_lo larger than y-component of prob_hi")
        if (self.prob_lo[2] >= self.prob_hi[2]):
            raise ValueError("z-component of prob_lo larger than z-component of prob_hi")
            
