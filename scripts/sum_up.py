import os

OUTPUT_UBUNTU   = eval(os.environ.get('OUTPUT_UBUNTU', ''))
OUTPUT_MACOS    = eval(os.environ.get('OUTPUT_MACOS', ''))
OUTPUT_ALPINE   = eval(os.environ.get('OUTPUT_ALPINE', ''))
OUTPUT_WINDOWS  = eval(os.environ.get('OUTPUT_WINDOWS', ''))
OUTPUT_RV       = eval(os.environ.get('OUTPUT_RV', ''))

with open(os.environ.get('GITHUB_STEP_SUMMARY'), 'w') as f:
    any_file_looks_odd = False
    for key in OUTPUT_UBUNTU:
        assert all(key in d for d in [OUTPUT_UBUNTU, OUTPUT_MACOS, OUTPUT_ALPINE, OUTPUT_WINDOWS, OUTPUT_RV])
        this_file_looks_odd = False
        print(f'## {key}\n')
        f.write(f'## {key}\n')
        print(f'x86_64 Ubuntu 22.04')
        f.write(f'x86_64 Ubuntu 22.04\n')
        for line in OUTPUT_UBUNTU[key]:
            print(f'- {line}: {OUTPUT_UBUNTU[key][line]}')
            f.write(f'- {line}: {OUTPUT_UBUNTU[key][line]}\n')
            if 'CE' in OUTPUT_UBUNTU[key][line]:
                this_file_looks_odd = True
            if 'RE' in OUTPUT_UBUNTU[key][line]:
                this_file_looks_odd = True
            if 'WA' in OUTPUT_UBUNTU[key][line]:
                this_file_looks_odd = True
        print(f'Arm64 macOS 12.0')
        f.write(f'Arm64 macOS 12.0\n')
        for line in OUTPUT_MACOS[key]:
            print(f'- {line}: {OUTPUT_MACOS[key][line]}')
            f.write(f'- {line}: {OUTPUT_MACOS[key][line]}\n')
            if 'CE' in OUTPUT_UBUNTU[key][line]:
                this_file_looks_odd = True
            if 'RE' in OUTPUT_UBUNTU[key][line]:
                this_file_looks_odd = True
            if 'WA' in OUTPUT_UBUNTU[key][line]:
                this_file_looks_odd = True
        print(f'x86_64 Alpine with MUSL')
        f.write(f'x86_64 Alpine with MUSL\n')
        for line in OUTPUT_ALPINE[key]:
            print(f'- {line}: {OUTPUT_ALPINE[key][line]}')
            f.write(f'- {line}: {OUTPUT_ALPINE[key][line]}\n')
            if 'CE' in OUTPUT_UBUNTU[key][line]:
                this_file_looks_odd = True
            if 'RE' in OUTPUT_UBUNTU[key][line]:
                this_file_looks_odd = True
            if 'WA' in OUTPUT_UBUNTU[key][line]:
                this_file_looks_odd = True
        print(f'x86_64 Windows 10')
        f.write(f'x86_64 Windows 10\n')
        for line in OUTPUT_WINDOWS[key]:
            print(f'- {line}: {OUTPUT_WINDOWS[key][line]}')
            f.write(f'- {line}: {OUTPUT_WINDOWS[key][line]}\n')
            if 'CE' in OUTPUT_UBUNTU[key][line]:
                this_file_looks_odd = True
            if 'RE' in OUTPUT_UBUNTU[key][line]:
                this_file_looks_odd = True
            if 'WA' in OUTPUT_UBUNTU[key][line]:
                this_file_looks_odd = True
        print(f'RISC-V64 Ubuntu 22.04')
        f.write(f'RISC-V64 Ubuntu 22.04\n')
        for line in OUTPUT_RV[key]:
            print(f'- {line}: {OUTPUT_RV[key][line]}')
            f.write(f'- {line}: {OUTPUT_RV[key][line]}\n')
            if 'CE' in OUTPUT_UBUNTU[key][line]:
                this_file_looks_odd = True
            if 'RE' in OUTPUT_UBUNTU[key][line]:
                this_file_looks_odd = True
            if 'WA' in OUTPUT_UBUNTU[key][line]:
                this_file_looks_odd = True
        if this_file_looks_odd:
            any_file_looks_odd = True
            f.write(f'疑似存在未定义行为，请核实\n')