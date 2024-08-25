import os
import subprocess

mainfiles, auxfiles, examples, skiptests = eval(os.environ.get("FILES_TO_TEST"))
runs_on = os.environ.get("RUNS_ON")

ACCEPTED = 0
ERR_CE = 1
ERR_RE = 2
ERR_WA = 3
SKIPPED = -1

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
BLUE = "\033[0;34m"
PURPLE = "\033[0;35m"
CYAN = "\033[0;36m"
WHITE = "\033[0;37m"
RESET = "\033[0m"

def ub_check(mainfile, auxfiles, examples, skiptest):
    """
    Check for undefined behavior.
    """

    # print(f"::group::Test for {mainfile}...")
    print(f"Test for {mainfile}...")
    # 是否跳过测试
    if skiptest:
        # summary += f'- {mainfile}\n\t- 测试跳过\n'
        print(f'{BLUE}test skipped because file {mainfile + ".skip_test"} exists{RESET}')
        return ['SKIPPED']
        # print(f'::endgroup::')
        # return SKIPPED, summary
    
    CALL_VCVARS_BAT = r'call "C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvars64.bat"'
    # 编译指令和编译产物
    compile_commands = [f'clang++ -std=c++17 -O0 {" ".join(auxfiles)} -o {mainfile.split(".")[0]}.Clang.O0',
                        f'clang++ -std=c++17 -O2 {" ".join(auxfiles)} -o {mainfile.split(".")[0]}.Clang.O2',
                        f'clang++ -std=c++17 -O3 {" ".join(auxfiles)} -o {mainfile.split(".")[0]}.Clang.O3',
                        f'g++ -std=c++17 -O0 {" ".join(auxfiles)} -o {mainfile.split(".")[0]}.GCC.O0',
                        f'g++ -std=c++17 -O2 {" ".join(auxfiles)} -o {mainfile.split(".")[0]}.GCC.O2',
                        f'g++ -std=c++17 -O3 {" ".join(auxfiles)} -o {mainfile.split(".")[0]}.GCC.O3',
                        f'{CALL_VCVARS_BAT} && cl /std:c++17 /Od {" ".join(auxfiles)} /Fe:{mainfile.split(".")[0]}.MSVC.O0',
                        f'{CALL_VCVARS_BAT} && cl /std:c++17 /O2 {" ".join(auxfiles)} /Fe:{mainfile.split(".")[0]}.MSVC.O2',
    ]
    compile_products = [f'{mainfile.split(".")[0]}.Clang.O0',
                        f'{mainfile.split(".")[0]}.Clang.O2',
                        f'{mainfile.split(".")[0]}.Clang.O3',
                        f'{mainfile.split(".")[0]}.GCC.O0',
                        f'{mainfile.split(".")[0]}.GCC.O2',
                        f'{mainfile.split(".")[0]}.GCC.O3',
                        f'{mainfile.split(".")[0]}.MSVC.O0',
                        f'{mainfile.split(".")[0]}.MSVC.O2',
    ]

    return_status = {}
    for compile_command, compile_product in zip(compile_commands, compile_products):
        print(compile_command, end=' ')
        result = subprocess.run(compile_command, shell=True)
        if result.returncode != 0:
            print(f'{RED}CE({result.returncode}){RESET}')
            status_vector = [f'{RED}CE{RESET}']
        else: 
            status_vector = [f'{GREEN}Compile OK{RESET}']
            print(f'{GREEN}OK{RESET}')
            for e in examples:
                print(f'{compile_product} < {e} > {e.replace(".in", ".out")}', end=' ')
                with open(e, 'r') as fstdin:
                    with open(e.replace(".in", ".out"), 'w') as fstdout:
                        result = subprocess.run(f'./{compile_product}', stdin=fstdin, stdout=fstdout, shell=True)
                if result.returncode != 0:
                    print(f'{RED}RE({result.returncode})){RESET}')
                    status_vector.append(f'{RED}RE{RESET}')
                else:
                    print(f'{GREEN}OK{RESET}')
                    print(f'diff -b -B {e.replace(".in", ".out")} {e.replace(".in", ".ans")}', end=' ')
                    result = subprocess.run(f'diff -b -B {e.replace(".in", ".out")} {e.replace(".in", ".ans")}', shell=True)
                    if result.returncode != 0:
                        print(f'{RED}WA{RESET}')
                        status_vector.append(f'{RED}WA{RESET}')
                    else:
                        print(f'{GREEN}AC{RESET}')
                        status_vector.append(f'{GREEN}AC{RESET}')
        print(f'{compile_product.split(os.path.pathsep)[-1]}: ', end='')
        for _ in status_vector:
            print(_, end='; ')
        print()
        return_status[compile_product] = status_vector

    print(f'{BLUE}Result for {mainfile}: {RESET}')
    for key in return_status:
        print(f'-  {key}: ', end='')
        for _ in return_status[key]:
            print(_, end='; ')
        print()
    print()
    # do something!
    return return_status


mainfiles, auxfiles, examples, skiptests = eval(os.environ.get("FILES_TO_TEST"))

cnt_ac, cnt_error, cnt_skip = 0, 0, 0
for mainfile, auxfile, example, skiptest in zip(mainfiles, auxfiles, examples, skiptests):
    checkres = ub_check(mainfile, auxfile, example, skiptest)

with open(os.environ.get('GITHUB_STEP_SUMMARY'), 'w') as f:
    f.write(f'# TOTAL {len(mainfiles)} TESTS, {cnt_ac} ACCEPTED, {cnt_skip} SKIPPED, {cnt_error} ERROR\n\n')
    print(f'::group::TOTAL {len(mainfiles)} TESTS, {cnt_ac} ACCEPTED, {cnt_skip} SKIPPED, {cnt_error} ERROR\n::endgroup::')

