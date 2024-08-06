import os

mainfiles, auxfiles, examples, skiptests = eval(os.environ.get("FILES_TO_TEST"))
runs_on = os.environ.get("RUNS_ON")

ACCEPTED = 1
ERROR = 0
SKIPPED = -1

def ub_check(mainfile, auxfiles, examples, skiptest):
    """
    Check for undefined behavior.
    """

    print(f"::group::Test for {mainfile}...")
    # 是否跳过测试
    if skiptest:
        summary += f'## 跳过：{mainfile}\n测试因 {mainfile + ".skip_test"} 文件存在而跳过\n\n'
        print(f'::group::{mainfile}: test skipped')
        print(f'::endgroup::')
        return SKIPPED, summary
    
    # 编译指令和编译产物
    compile_commands = [f'clang++ -std=c++17 -O0 {" ".join(auxfiles)} -o {mainfile.split(".")[0]}.Clang.O0',
                        f'clang++ -std=c++17 -O2 {" ".join(auxfiles)} -o {mainfile.split(".")[0]}.Clang.O2',
                        f'clang++ -std=c++17 -O3 {" ".join(auxfiles)} -o {mainfile.split(".")[0]}.Clang.O3',
                        f'g++-13 -std=c++17 -O0 {" ".join(auxfiles)} -o {mainfile.split(".")[0]}.GCC.O0',
                        f'g++-13 -std=c++17 -O2 {" ".join(auxfiles)} -o {mainfile.split(".")[0]}.GCC.O2',
                        f'g++-13 -std=c++17 -O3 {" ".join(auxfiles)} -o {mainfile.split(".")[0]}.GCC.O3',
    ]
    compile_products = [f'{mainfile.split(".")[0]}.Clang.O0',
                        f'{mainfile.split(".")[0]}.Clang.O2',
                        f'{mainfile.split(".")[0]}.Clang.O3',
                        f'{mainfile.split(".")[0]}.GCC13.O0',
                        f'{mainfile.split(".")[0]}.GCC13.O2',
                        f'{mainfile.split(".")[0]}.GCC13.O3',
    ]

    # do something!
    return ACCEPTED, summary

mainfiles, auxfiles, examples, skiptests = eval(os.environ.get("FILES_TO_TEST"))
summary = ''

cnt_ac, cnt_error, cnt_skip = 0, 0, 0
for mainfile, auxfile, example, skiptest in zip(mainfiles, auxfiles, examples, skiptests):
    checkres, summary = ub_check(mainfile, auxfile, example, skiptest, summary)
    cnt_ac = cnt_ac + 1 if checkres == ACCEPTED else cnt_ac
    cnt_error = cnt_error + 1 if checkres == ERROR else cnt_error
    cnt_skip = cnt_skip + 1 if checkres == SKIPPED else cnt_skip

with open(os.environ.get('GITHUB_STEP_SUMMARY'), 'w') as f:
    f.write(f'# TOTAL {len(mainfiles)} TESTS, {cnt_ac} ACCEPTED, {cnt_skip} SKIPPED, {cnt_error} ERROR\n\n')
    f.write(summary)
    print(f'::group::TOTAL {len(mainfiles)} TESTS, {cnt_ac} ACCEPTED, {cnt_skip} SKIPPED, {cnt_error} ERROR\n::endgroup::')

