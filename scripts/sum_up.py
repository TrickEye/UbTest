import os

OUTPUT_UBUNTU   = eval(os.environ.get('OUTPUT_UBUNTU', ''))
OUTPUT_MACOS    = eval(os.environ.get('OUTPUT_MACOS', ''))
OUTPUT_ALPINE   = eval(os.environ.get('OUTPUT_ALPINE', ''))
OUTPUT_WINDOWS  = eval(os.environ.get('OUTPUT_WINDOWS', ''))
OUTPUT_RV       = eval(os.environ.get('OUTPUT_RV', ''))

with open(os.environ.get('GITHUB_STEP_SUMMARY'), 'w') as f:
    for key in OUTPUT_UBUNTU:
        assert all(key in d for d in [OUTPUT_UBUNTU, OUTPUT_MACOS, OUTPUT_ALPINE, OUTPUT_WINDOWS, OUTPUT_RV])
        print(f'## {key}\n')
        print(f'x86_64 Ubuntu 22.04\n')
        for line in OUTPUT_UBUNTU[key]:
            print(f'{line}: {OUTPUT_UBUNTU[key][line]}\n')
        print(f'Arm64 macOS 12.0\n')
        for line in OUTPUT_MACOS[key]:
            print(f'{line}: {OUTPUT_MACOS[key][line]}\n')
        print(f'x86_64 Alpine 3.14\n')
        for line in OUTPUT_ALPINE[key]:
            print(f'{line}: {OUTPUT_ALPINE[key][line]}\n')
        print(f'x86_64 Windows 10\n')
        for line in OUTPUT_WINDOWS[key]:
            print(f'{line}: {OUTPUT_WINDOWS[key][line]}\n')
        print(f'RISC-V64 Ubuntu 22.04\n')
        for line in OUTPUT_RV[key]:
            print(f'{line}: {OUTPUT_RV[key][line]}\n')
