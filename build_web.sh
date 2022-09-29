#!/bin/zsh
project_name=Pirate
# building web version using pygbag (toolchain to use pygame with WebAssembly aka wasm)
# build can be found in bin\web
# add --archive to crate web.zip (e.g. for easy deploy to itch.io)
# see https://pypi.org/project/pygbag/ for more details

cd ..
#/Users/hubertnafalski/Library/Python/3.8/bin/
#/Users/hubertnafalski/Library/Python/3.8/bin/pygbag --build --archive --template $project_name/mobile.tmpl --app_name $project_name $project_name
/Users/hubertnafalski/Library/Python/3.8/bin/pygbag --build --archive --app_name $project_name $project_name
cd $project_name
