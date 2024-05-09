$ErrorActionPreference = "Stop"

if (test-path _skbuild) {
    cmd.exe /c rd /s /q _skbuild
}
if (test-path dist) {
    cmd.exe /c rd /s /q dist
}
if (test-path venv_ngs) {
    cmd.exe /c rd /s /q venv_ngs
}

Set-Location ../..
python.exe -m venv .\venv_ngs
.\venv_ngs\scripts\Activate.ps1
$env:PATH += Join-Path ";" (Get-Item .).FullName "venv_ngs\bin"

pip3 install scikit-build wheel numpy twine mkl-devel==2022.* mkl==2022.* setuptools==69.5.1 setuptools_scm==8.1.0
pip3 install -r .github/workflows/ngsolve_version.txt

#$env:NGSolve_DIR = "$env:Python3_ROOT_DIR\lib\site-packages\ngsolve\cmake"
#$env:Netgen_DIR = "$env:Python3_ROOT_DIR\lib\site-packages\netgen\cmake"

python setup.py bdist_wheel -G"Visual Studio 16 2019" -d wheelhouse
