from tac_cfopt import optimize
import subprocess
import json
import bx2front
import os
import sys



from bx2front import bxfront
from bx_ast import Program
from bx2tac import bx2tac, bx2tacjson
from tac2x64 import compile_tac
from ast2tac import Prog
from tac_cfopt import optimize

bx_path = 'examples/'
bx_files = [os.path.join(dp, f)
             for dp, _, fn in os.walk(bx_path) for f in fn if f.endswith(".bx")]
bx_files = [os.path.join(dp, f)
             for dp, _, fn in os.walk(bx_path) for f in fn if f.endswith(".bx")]

nb_files = len([bx_file for bx_file in bx_files if "regression" not in bx_file ])




class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

def run_test_bx2front() :



    print('---------- TEST BX2FRONT -------------')
    counter = 0
    for bx_file in bx_files : 
        if "regression" in bx_file :
            try :
                with HiddenPrints():
                    bx2front.bxfront(bx_file)
                print(f'ERROR {bx_file} regression file should not be parsed correctly')
            except : 
                print("PASS")
                counter +=1
        else :
            try :
                with HiddenPrints():
                    bx2front.bxfront(bx_file)
                print("PASS")
                counter += 1
            except : print(f'ERROR {bx_file} error during parsing of correct file')

    print()
    print(len(bx_files) - counter, " / ", counter, " ERRORS")



def run_test_optim() :


    # print('---------- TEST OPTIM USING TACRUN-------------')
    # counter = 0
    # for bx_file in bx_files : 

    #     if "regression" not in bx_file :
    #         print(bx_file)
    #         try :
            
    #             with HiddenPrints():
    #                 program = bxfront(bx_file)
    #                 prog = Prog(program)  # Create ast + tac
    #                 tac = prog.js_obj  # Create json for tac
    #                 tac_optim = optimize(tac) # Optimize tac
    #                 with open('to_del_optim.tac.json','w') as tac_file :
    #                     json.dump(tac, tac_file, indent=2)
    #                 with open('to_del.tac.json','w') as optim_tac_file :
    #                     json.dump(tac_optim, optim_tac_file, indent=2)



    #                 cmd = ['python3', 'tacrun.py','to_del.tac.json' ]
    #                 output1 = subprocess.Popen(cmd, stdout=subprocess.PIPE ).communicate()[0]
    #                 cmd = ['python3', 'tacrun.py','to_del_optim.tac.json' ]
    #                 output2 = subprocess.Popen(cmd, stdout=subprocess.PIPE ).communicate()[0]
    #                 print(output1 == output2)
    #                 counter +=1
    #         except Exception as e :
    #             print(e)
    
    # print()
    # print(nb_files - counter, " / ", counter, " ERRORS")

    print('---------- TEST COMPILATION USING TAC2X64-------------')
    counter = 0
    for bx_file in bx_files : 

        if "regression" not in bx_file :
            print(bx_file)
            try :
            
                with HiddenPrints():
                    program = bxfront(bx_file)
                    prog = Prog(program)  # Create ast + tac
                    tac = prog.js_obj  # Create json for tac
                    tac_optim = optimize(tac) # Optimize tac
                    # with open('to_del_optim.tac.json','w') as tac_file :
                    #     json.dump(tac, tac_file, indent=2)
                    # with open('to_del.tac.json','w') as optim_tac_file :
                    #     json.dump(tac_optim, optim_tac_file, indent=2)


                
                    compile_tac(tac_optim,"to_del_optim.s")
                    compile_tac(tac,"to_del.s")

                    cmd = ['gcc', '-o','test_optim.exe', "bx_runtime.c","to_del_optim.s" ]
                    p = subprocess.Popen(cmd)
                    p.wait()
                    cmd = ['gcc', '-o','test.exe', "bx_runtime.c","to_del.s"  ]
                    p = subprocess.Popen(cmd)
                    p.wait()
                    print("PASS")
                    counter += 1
                        
            except Exception as e:
                print("FAIL",e)

    print()
    print(nb_files - counter, " / ", counter, " ERRORS")

        
    print('---------- TEST EXECUTION -------------')
    counter = 0

    for bx_file in bx_files : 

            if "regression" not in bx_file :
                print(bx_file)
                try :
                
            
                
                    program = bxfront(bx_file)
                    prog = Prog(program)  # Create ast + tac
                    tac = prog.js_obj  # Create json for tac
                    tac_optim = optimize(tac) # Optimize tac


                    with HiddenPrints():

                        compile_tac(tac_optim,"to_del_optim.s")
                        compile_tac(tac,"to_del.s")

                    
                    cmd = ['gcc', '-o','test_optim.exe', "bx_runtime.c","to_del_optim.s" ]
                    p = subprocess.Popen(cmd)
                    p.wait()
                    cmd = ['gcc', '-o','test.exe', "bx_runtime.c","to_del.s"]
                    p = subprocess.Popen(cmd)
                    p.wait()


                    cmd = ['timeout' ,'2','./test_optim.exe' ]
                    output1 = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
                    
                    cmd = ['timeout' ,'2','./test.exe' ]
                    output2 = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]

                    print("PASS" if output1==output2 else "FAIL")
                    counter += (1 if output1==output2 else 0)


                   
                   

                        
                                
                except Exception as e:
                    print("FAIL ",e)
    print()
    print(nb_files - counter, " / ", counter, " ERRORS")

    cmd = ['rm' ,'./test.exe', './test_optim.exe', "to_del_optim.s", "to_del.s" ] #, 'to_del.tac.json', 'to_del_optim.tac.json']
    p = subprocess.Popen(cmd)
    p.wait()
                    



        
        
        



    

        
    
        

if __name__ == '__main__':

    run_test_bx2front()
    run_test_optim()
    

    
