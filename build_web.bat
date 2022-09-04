@echo off
set project_name=Pirate
REM building web version using pygbag (toolchain to use pygame with WebAssembly aka wasm)
REM build can be found in bin\web
REM add --archive to crate web.zip (e.g. for easy deploy to itch.io)
REM see https://pypi.org/project/pygbag/ for more details

set current_dir=%CD%
cd ..
pygbag --build --archive --app_name %project_name% "%current_dir%"
cd "%current_dir%"
