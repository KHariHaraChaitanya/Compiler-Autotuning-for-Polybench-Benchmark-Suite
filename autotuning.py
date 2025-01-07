import os
import sys
import subprocess
import argparse
def execute_binary(binary_path, thread_count):
	if thread_count !=0:
		os.environ['OMP_NUM_THREADS'] = str(thread_count)
	result = subprocess.run(binary_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE , shell=True)
	return result.stdout.decode("utf-8").strip()
def set_environment_from_file(env_file):
    with open(env_file, 'r') as file:
        for line in file:
            if "export" in line:
                env_var = line.replace('export ', '').strip()
                key, value = env_var.split('=', 1)
                value = value.strip('"').strip("'")
                os.environ[key] = value

def read_env_file(filename):
    env_vars = {}
    with open(filename) as f:
        for line in f:
            line = line.replace('export ', '').strip()
            key_value = line.split('=', 1)
            if len(key_value) == 2:
                key, value = key_value
                value = value.strip('"').strip("'")
                env_vars[key] = value
    return env_vars

def compileOptions(Nvalues):
    for N in Nvalues:
        command = "gcc -O3 -fopenmp -I polybench-c-4.2.1-beta/utilities -I polybench-c-4.2.1-beta/datamining/correlation "+enable_papi_libraries+" polybench-c-4.2.1-beta/utilities/polybench.c "+str(inputFile)+" "+dpolybenchMacro+" -o bin/"+str(outputBinaryName)+" -lm"
        exitcode=os.system(command) 
        if exitcode!=0:
            raise SystemExit("Invalid compilation command ")
def insertcommas(value):
    value = int(value)
    formatted_number = "{:,}".format(value)
    return formatted_number


def runPAPI(binary="./my_binary",thread_count=8):
    countername = ["PAPI_TOT_CYC","L1-DCACHE-LOADS","PAPI_L1_DCM","PAPI_L2_TCA","PAPI_L2_TCM","PAPI_TLB_DM","PAPI_RES_STL","PAPI_VEC_SP","PAPI_VEC_DP","PAPI_SP_OPS","PAPI_DP_OPS"]
    print(f'thread counts: {thread_count}')
    dict_counters={}
    for opt in Optimizations:
        resultsSum=0
        resultsArray=[]
        for j in range(1):
            opvalues=execute_binary(binary, thread_count) 
            counterValues = opvalues.split(" ")
            #counterValues_final = []
            for v in range(len(counterValues)):
                #counterValues[v] = insertcommas(counterValues[v])
                print(countername[v]+"   "+insertcommas(counterValues[v]))
                counterValues[v] = int(counterValues[v])
            dict_counters = dict(zip(countername, counterValues))
            total_instructions = dict_counters["PAPI_SP_OPS"] + dict_counters["PAPI_DP_OPS"]
            IPC = total_instructions / dict_counters["PAPI_TOT_CYC"]
            print(f'Average Instructions Per Cycle: {IPC:.6f}')
            total_vector_instructions = dict_counters["PAPI_VEC_SP"] + dict_counters["PAPI_VEC_DP"]
            vIPC = total_vector_instructions / dict_counters["PAPI_TOT_CYC"]
            print(f'Average Vector Instructions Per Cycle: {vIPC:.6f}')
            L1_miss_rate = (dict_counters["PAPI_L1_DCM"] / dict_counters["L1-DCACHE-LOADS"]) * 100
            print(f'Average L1 Data Cache Miss Rate: {L1_miss_rate:.6f}')
            total_cache_L2_accesses = dict_counters["PAPI_L2_TCA"]+dict_counters["PAPI_L2_TCM"]
            L2_miss_rate = (dict_counters["PAPI_L2_TCM"] / total_cache_L2_accesses) * 100
            print(f'Average L2 Data Cache Miss Rate: {L2_miss_rate:.6f}')
            L1AC = dict_counters["L1-DCACHE-LOADS"] / total_instructions
            print(f'Average Number of L1 Accesses Per Instruction: {L1AC:.6f}')
            vL1AC = dict_counters["L1-DCACHE-LOADS"] / total_vector_instructions
            print(f'Average Number of L1 Accesses Per vector Instruction: {vL1AC:.6f}')
            stall_percentage = (dict_counters["PAPI_RES_STL"] /dict_counters["PAPI_TOT_CYC"]) * 100
            print(f'Percentage of Cycles Stalled: {stall_percentage:.6f}')
    

def runOptimizations(binary="./my_binary",thread_count=8):
    for opt in Optimizations:
        resultsSum=0
        resultsArray=[]
        for j in range(10):
            time=execute_binary(binary, thread_count) 
            if not isinstance(time,str):
                print(time)
            else:
                time=float(time)
                resultsSum=resultsSum+time
                resultsArray.append(time)
        print(f'thread counts: {thread_count} min: {min(resultsArray):.6f} max: {max(resultsArray):.6f} avg: {(resultsSum)/10:.6f}')
Nvalues=[]
Optimizations=["-O3"] #default
inputFile="polybench-c-4.2.1-beta/datamining/correlation/correlation.c" #default
outputFile = "output.txt"
outputBinaryName = "my_binary_omp_opt" #default
dpolybenchMacro = "-DPOLYBENCH_TIME" #default
enable_papi_libraries =""
parser = argparse.ArgumentParser(description="Tool for tuning and exploring optimizations.")
parser.add_argument("--machine-info",action='store_true')
parser.add_argument("--read-environment", type=str)
parser.add_argument("--command", type=str)
parser.add_argument("--explore-threads",action='store_true')
parser.add_argument("--explore-polybench",type=str)
parser.add_argument("--explore-N",type=str)
parser.add_argument("--profile-papi",action='store_true')
parser.add_argument("--papi-counter-file",type=str)
args = parser.parse_args()
os.system("mkdir bin")
if args.profile_papi:
    outputBinaryName = "gemm_papi_counters"
    dpolybenchMacro = "-DPOLYBENCH_PAPI"
    enable_papi_libraries = "-I $HOME/cs553-hw4/papi/install/include -L $HOME/cs553-hw4/papi/install/lib -lpapi"
if args.papi_counter_file:
    os.system("mv polybench-c-4.2.1-beta/utilities/papi_counters.list backup_papi_counters.list")
    os.system("cp "+args.papi_counter_file+" polybench-c-4.2.1-beta/utilities/papi_counters.list")
if args.machine_info:
    	command = "grep 'model name' /proc/cpuinfo | head -1 | awk -F':' '{print $2}'"
    	result = subprocess.run(command, shell=True,capture_output=True, text=True)
    	print("Processor: ",result.stdout.strip())
    	command = "lscpu | grep 'Core(s) per socket:'| awk -F':' '{print $2}'| xargs"
    	result = subprocess.run(command, shell=True,capture_output=True, text=True)
    	print("Number of physical cores: ",result.stdout.strip())
    	command = "lscpu | grep '^CPU(s):'| awk -F':' '{print $2}'| xargs"
    	result = subprocess.run(command, shell=True,capture_output=True, text=True)
    	print("Number of logical CPUs: ",result.stdout.strip())
if args.read_environment:
    set_environment_from_file(args.read_environment)
if args.explore_polybench:
    inputFile = args.explore_polybench
if args.command:
    if args.explore_threads:
        max_threads = int(os.getenv('OMP_NUM_THREADS', '1'))
        print(f'# program: {args.command}')
        for thread_count in range(1, max_threads + 1):
            if args.profile_papi:
                runPAPI(args.command,thread_count)
            else:
                runOptimizations(args.command, thread_count)
    else:
        result = subprocess.run(args.command, shell=True, capture_output=True, text=True)
        print(result.stdout)       
    if args.command == "./test_env.sh":
        print("Testing environment variables by executing test_env.sh")
        subprocess.run("./test_env.sh", shell=True)
if args.explore_N:
    Nvalues = args.explore_N.split(",")
    compileOptions(Nvalues)
else:
	command = "gcc -O3 -fopenmp -I polybench-c-4.2.1-beta/utilities -I polybench-c-4.2.1-beta/datamining/correlation "+enable_papi_libraries+" polybench-c-4.2.1-beta/utilities/polybench.c "+str(inputFile)+" "+dpolybenchMacro+" -o bin/"+str(outputBinaryName)+".1200.1400"+" -lm"
	print("executed command "+command)
	exitcode = os.system(command)
	if exitcode!=0 :
		raise SystemExit("Invalid compilation command ")
	    
binarylist = os.listdir("bin")
binarylist.sort(key=lambda x: int(x.split('.')[1]))    
if args.explore_threads:
	max_threads = int(os.getenv('OMP_NUM_THREADS', '1'))
	for binary in binarylist :
		print(f'# program: {binary}')
		for thread_count in range(1, max_threads + 1) :
			if args.profile_papi:
				runPAPI("bin/"+binary,thread_count)
			else :
				runOptimizations("bin/"+binary, thread_count)
else:
	for binary in binarylist:
		if args.profile_papi:
			print(f'# program: {binary}')
			runPAPI("bin/"+binary)
		else:
			print(f'# program: {binary}')
			runOptimizations("bin/"+binary)
if args.papi_counter_file:
    os.system("mv backup_papi_counters.list polybench-c-4.2.1-beta/utilities/papi_counters.list")
os.system("rm -rf bin")
