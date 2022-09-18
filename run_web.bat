@echo off
set project_name=Pirate
REM building web version using pygbag (toolchain to use pygame with WebAssembly aka wasm)
REM build can be found in bin\web
REM http://localhost:8000         to run game locally in browser
REM when "Ready to start !" messages shows up, click mouse button to start game
REM http://localhost:8000/#debug  to debug game locally in browser (enforce page reaload)
REM press ctr + c to exit
REM see https://pypi.org/project/pygbag/ for more details

set current_dir=%CD%
cd ..
pygbag --bind 192.168.1.36 --template %project_name%/mobile.tmpl --app_name %project_name% "%current_dir%"
cd "%current_dir%"
