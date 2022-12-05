import os, os.path, sys
import math
import json
import yaml
import glob 
import argparse
import subprocess
import numpy as np

from CP3SlurmUtils.Configuration import Configuration
from CP3SlurmUtils.SubmitWorker import SubmitWorker



def postprocessing(process, mH, mA, outdir, do):
    
    if do == 'tanb_vs_mass':

        cba    = run_opts[do]['cba'] 
        mTofix = run_opts[do]['m_tofix']
        _type  = run_opts[do]['type']

        full_dict = {'HToZA': {}, 'AToZH': {} }
        full_dict['cos(b-a)']= cba
        full_dict['type']=_type
        full_dict['model']='2HDM'

        for jsF in glob.glob( os.path.join(outdir, 'outputs', '*', "2hdmc1.8.0-br_cba-{}_mAorH-{}_2hdm-type{}.yml".format(cba, mTofix, _type))):
                
            if not os.path.isfile(jsF):
                continue

            with open(jsF) as f_:
                data = yaml.safe_load(f_)
            
            full_dict['HToZA'].update(data['HToZA'])
            full_dict['AToZH'].update(data['AToZH'])

        TotFile = os.path.join(outdir, "2hdmc1.8.0-br_cba-{}_mAorH-{}_2hdm-type{}.yml".format(cba, mTofix, _type))
        with open(TotFile, 'w') as _f:
            yaml.dump(full_dict, _f, default_flow_style=False)

        print( 'Done finalizing tasks, result file can be found in :: %s'%TotFile)
    
    elif do == 'tanb_vs_cosba':
        
        mode    = process[-1]
        if mode == 'H':
            light   = 'A'
            heavy   = 'H'
            m_heavy = mH
            m_light = mA
        elif mode == 'A':
            light   = 'H'
            heavy   = 'A'
            m_heavy = mA
            m_light = mH
        
        results = {
            'tb': [],
            'cba': [],
            'sigma': [],
            'sigma_errIntegration': [],
            'TotBR': []
            }

        fullscan = list(np.arange(0.01, 5., 0.5))+list(np.arange(5., 51.1, 0.5))
        for i, tb in enumerate(fullscan):
            for j, ba in enumerate(np.arange(0.13, math.pi, 0.1)):
            
                cba = math.cos(ba) 
                
                filename  = 'sigmaBR_%sZ%s_type-2_M%s-%s_M%s-%s_tb-%s_cba-%s.json' %(
                        heavy, light, heavy, str(round(m_heavy,2)), light, str(round(m_light,2)), str(round(tb,2)), str(round(cba, 5)))
                
                jsF = os.path.join(outdir, 'results', filename)
                
                print('processing ::', jsF)
                if not os.path.exists(jsF):
                    continue
                
                with open(jsF) as f:
                    cfg = json.load(f)
                if not cfg:
                    continue
                for k in cfg.keys():
                    results[k.decode("utf-8")] += cfg[k]
        

        jsF_result = os.path.join(outdir, 'sigmaBR_%s_%sZ%s_type-2_M%s-%s_M%s-%s_tb_cba.json'%(
                    process, heavy, light, heavy, str(round(m_heavy,2)), light, str(round(m_light,2)))
                    )    
        
        print( len(results['tb']), len(results['cba']))
        print( max(results['tb']), max(results['cba']) ,  min(results['tb']), min(results['cba']))
        
        with open(jsF_result, 'w+') as f:
           json.dump(results, f)
        print( 'result file is saved in ::' , jsF_result)


def SlurmRun2HDMCalculator(output, process, mH, mA, finalize=False, do=''):
    config = Configuration()
    config.sbatch_partition = 'cp3'
    config.sbatch_qos = 'cp3'
    config.cmsswDir = os.path.dirname(os.path.abspath(__file__))
    config.sbatch_chdir = os.path.join(output, 'slurm', process)
    config.sbatch_time = '00:59:00'
    config.sbatch_memPerCPU = '500'
    config.stageoutDir = config.sbatch_chdir
    #config.stageoutFiles = ['*.json']
    #config.environmentType = 'cms'
    #config.inputSandboxContent = []
    #config.numJobs=1
    config.inputParams = []
    
    cmssw  = config.cmsswDir
    outdir = config.sbatch_chdir
    
    if finalize:
        postprocessing(process, mH, mA, outdir, do)
    
    else:
        if do == 'tanb_vs_cosba':
            config.inputParamsNames = ["cmssw", "outdir", "process", "mH", "mA", "tb", "ba"]
            
            for ki, kf in [[0.01, 5.], [5., 10.], [10., 15.], [15, 20.], [20., 25.], [25., 30.], [30., 35.], [35., 40.], [40., 45.], [45., 50.1]]: # to avoid running into max job submission allowed
                for i, tb in enumerate(np.arange(ki, kf, 0.1)):
                    for j, ba in enumerate(run_opts[do]['ba']):
                        
                        #if i !=0 or j!=0: # run a test
                        #    continue
                        config.inputParams.append([cmssw, outdir, process, mH, mA, tb, ba])
                    
                config.payload = \
                """
                python ${cmssw}/example/produce_xsec_for_ZA_tanb_cosba.py -o ${outdir} --cmssw ${cmssw} --process ${process} --mH ${mH} --mA ${mA} --tb ${tb} --ba ${ba}
                """
                submitWorker = SubmitWorker(config, submit=True, yes=True, debug=True, quiet=True)
                submitWorker()

        elif do =='tanb_vs_mass':
            config.inputParamsNames = ["cmssw", "mass", "tanbeta", "outdir"]
            
            for i, mass in enumerate(run_opts[do]['mass']):
                for j, tanbeta in enumerate(run_opts[do]['tb']):
                    
                    #if i !=0 or j!=0: # run a test
                    #    continue
                    config.inputParams.append([cmssw, mass, tanbeta, outdir])
                
            config.payload = \
            """
            jobid=${SLURM_ARRAY_TASK_ID}
            python ${cmssw}/example/sushi_for_2hdm__ver2.py --mass ${mass} --tanbeta ${tanbeta} --jobid ${jobid} --slurm -o ${outdir}
            """
            submitWorker = SubmitWorker(config, submit=True, yes=True, debug=True, quiet=True)
            submitWorker()


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='slurm for 2hdmc and sushi', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-o", "--output", default=None, required=True, help="output dir")
    parser.add_argument("-p", "--process", type=str, choices=['ggH', 'ggA', 'bbH', 'bbA'], default ='', required=False,
                        help="This will decide the mode (H-> ZA or A -> ZH) also the renormalisation and factorisation scale")
    parser.add_argument('--mH', type=float, default=500., help='mass of the Higgs bosons H')
    parser.add_argument('--mA', type=float, default=300., help='mass of the pseudo-scalar A')
    parser.add_argument("--finalize", default=False, action='store_true', help='This is a post-processing step to combine all results in one json File')
    
    options = parser.parse_args()
    
    
    Extra  = [ 50., 100., 200., 250., 300., 400., 450., 1000.]
    Extra += [ 55.16, 566.51, 160.17, 87.1, 298.97, 186.51, 118.11, 137.54, 40.68, 47.37, 779.83, 350.77, 664.66, 74.8, 34.93, 254.82, 101.43, 217.19, 482.85, 411.54, 64.24, 30.0]
    
    run_opts = { 'tanb_vs_mass' : { 
                        'tb'  : np.arange(0.05, 50.5, 0.5),
                        'mass': sorted(Extra + np.arange(10., 1000., 50.).tolist()),
                        'cba' : 0.01,
                        'm_tofix': 500.,
                        'type': 2,
                        },
                 'tanb_vs_cosba': { 
                        'tb': np.arange(0.01, 5., 0.5), 
                        'ba': np.arange(0.13, math.pi, 0.03),
                        },
                 }

    for do_what in ['tanb_vs_mass']:#, 'tanb_vs_cosba']:

        SlurmRun2HDMCalculator(output  = options.output, 
                               process = options.process, 
                               mH      = options.mH, 
                               mA      = options.mA, 
                               finalize= options.finalize, 
                               do      = do_what
                              )
