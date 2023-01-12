""" 
Setup a FAST.Farm suite of cases based on input parameters.

The extent of the high res and low res domain are setup according to the guidelines:
    https://openfast.readthedocs.io/en/dev/source/user/fast.farm/ModelGuidance.html

NOTE: If driving FAST.Farm using TurbSim inflow, the resulting boxes are necessary to
      build the final FAST.Farm case and are not provided as part of this repository. 
      If driving FAST.Farm using LES inflow, the VTK boxes are not necessary to exist.

"""

from pyFAST.fastfarm.FASTFarmCaseCreation import FFCaseCreation

def main():

    # -----------------------------------------------------------------------------
    # USER INPUT: Modify these
    # -----------------------------------------------------------------------------

    # ----------- Case absolute path
    path = '/complete/path/of/your/case'
    
    # ----------- Wind farm
    wts  = {
              0 :{'x':0.0,     'y':0,       'z':0.0,  'D':250,  'zhub':150},
              1 :{'x':1852.0,  'y':0,       'z':0.0,  'D':250,  'zhub':150},
              2 :{'x':3704.0,  'y':0,       'z':0.0,  'D':250,  'zhub':150},
              3 :{'x':5556.0,  'y':0,       'z':0.0,  'D':250,  'zhub':150},
              4 :{'x':7408.0,  'y':0,       'z':0.0,  'D':250,  'zhub':150},
              5 :{'x':1852.0,  'y':1852.0,  'z':0.0,  'D':250,  'zhub':150},
              6 :{'x':3704.0,  'y':1852.0,  'z':0.0,  'D':250,  'zhub':150},
              7 :{'x':5556.0,  'y':1852.0,  'z':0.0,  'D':250,  'zhub':150},
              8 :{'x':7408.0,  'y':1852.0,  'z':0.0,  'D':250,  'zhub':150},
              9 :{'x':3704.0,  'y':3704.0,  'z':0.0,  'D':250,  'zhub':150},
              10:{'x':5556.0,  'y':3704.0,  'z':0.0,  'D':250,  'zhub':150},
              11:{'x':7408.0,  'y':3704.0,  'z':0.0,  'D':250,  'zhub':150},
            }
    refTurb_rot = 0
    
    # ----------- General hard-coded parameters
    cmax     = 5      # maximum blade chord (m)
    fmax     = 10/6   # maximum excitation frequency (Hz)
    Cmeander = 1.9    # Meandering constant (-)
    
    # ----------- Additional variables
    tmax = 1800
    nSeeds = 6
    zbot = 1
    
    # ----------- Desired sweeps
    vhub       = [10]
    shear      = [0.2]
    TIvalue    = [10]
    inflow_deg = [0]
    
    # ----------- Turbine parameters
    # Set the yaw of each turbine for wind dir. One row for each wind direction.
    yaw_init = [ [0,0,0,0,0,0,0,0,0,0,0,0] ]
    
    # ----------- Low- and high-res boxes parameters
    # Should match LES if comparisons are to be made; otherwise, set desired values
    # High-res boxes settings
    dt_high_les = 0.6                # sampling frequency of high-res files
    ds_high_les = 10.0               # dx, dy, dz that you want these high-res files at
    extent_high = 1.2                # high-res box extent in y and x for each turbine, in D.
    # Low-res boxes settings
    dt_low_les  = 3                  # sampling frequency of low-res files
    ds_low_les  = 20.0               # dx, dy, dz of low-res files
    extent_low  = [3, 8,  3, 3, 2] 
    
    
    # ----------- Execution parameters
    ffbin = '/full/path/to/your/binary/.../bin/FAST.Farm'
    
    # ----------- LES parameters. This variable will dictate whether it is a TurbSim-driven or LES-driven case
    LESpath = '/full/path/to/the/LES/case'
    #LESpath = None # set as None if TurbSim-driven is desired
    
    
    # -----------------------------------------------------------------------------
    # ----------- Template files
    templatePath            = '/full/path/where/template/files/are'
    
    # Put 'unused' to any input that is not applicable to your case
    EDfilename              = 'ElastoDyn.T'
    SEDfilename             = 'SimplifiedElastoDyn.T'
    HDfilename              = 'HydroDyn.dat'
    SrvDfilename            = 'ServoDyn.T'
    ADfilename              = 'AeroDyn.dat'
    ADskfilename            = 'AeroDisk.dat'
    SubDfilename            = 'SubDyn.dat'
    IWfilename              = 'InflowWind.dat'
    BDfilepath              = 'unused'
    bladefilename           = 'Blade.dat'
    towerfilename           = 'Tower.dat'
    turbfilename            = 'Model.T'
    libdisconfilepath       = '/full/path/to/controller/libdiscon.so'
    controllerInputfilename = 'DISCON.IN'
    coeffTablefilename      = 'CpCtCq.csv'
    FFfilename              = 'Model_FFarm.fstf'
    
    # TurbSim setups
    turbsimLowfilepath      = './SampleFiles/template_Low_InflowXX_SeedY.inp'
    turbsimHighfilepath     = './SampleFiles/template_HighT1_InflowXX_SeedY.inp'
    
    # SLURM scripts
    slurm_TS_high           = './SampleFiles/runAllHighBox.sh'
    slurm_TS_low            = './SampleFiles/runAllLowBox.sh'
    slurm_FF_single         = './SampleFiles/runFASTFarm_cond0_case0_seed0.sh'


    # -----------------------------------------------------------------------------
    # END OF USER INPUT
    # -----------------------------------------------------------------------------


    # Initial setup
    case = FFCaseCreation(path, wts, cmax, fmax, Cmeander, tmax, zbot, vhub, shear,
                          TIvalue, inflow_deg, dt_high_les, ds_high_les, extent_high,
                          dt_low_les, ds_low_les, extent_low, ffbin, LESpath=LESpath,
                          verbose=1)

    case.setTemplateFilename(templatePath, EDfilename, SEDfilename, HDfilename, SrvDfilename, ADfilename,
                             ADskfilename, SubDfilename, IWfilename, BDfilepath, bladefilename, towerfilename,
                             turbfilename, libdisconfilepath, controllerInputfilename, coeffTablefilename,
                             turbsimLowfilepath, turbsimHighfilepath, FFfilename)

    case.copyTurbineFilesForEachCase()
    case.getDomainParameters()

    # TurbSim setup
    if LESpath is None:
        case.TS_low_setup()
        case.TS_low_slurm_prepare(slurm_TS_low)
        #case.TS_low_slurm_submit()

        case.TS_high_setup()
        case.TS_high_slurm_prepare(slurm_TS_high)
        #case.TS_high_slurm_submit()

    # Final setup
    case.FF_setup()
    case.FF_slurm_prepare(slurm_FF_single)
    #case.FF_slurm_submit()


if __name__ == '__main__':
    # This example cannot be fully run if TurbSim inflow is requested.
    main()