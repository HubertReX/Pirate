#!/bin/zsh
project_name=Pirate
# building web version using pygbag (toolchain to use pygame with WebAssembly aka wasm)
# build can be found in bin\web
# http://localhost:8000         to run game locally in browser
# when "Ready to start !" messages shows up, click mouse button to start game
# http://localhost:8000/#debug  to debug game locally in browser (enforce page reaload)
# press ctr + c to exit
# see https://pypi.org/project/pygbag/ for more details

#   -h, --help            show this help message and exit
#   --bind ADDRESS        Specify alternate bind address [default: localhost]
#   --directory DIRECTORY
#                         Specify alternative directory [default:/$CD/build/web]
#   --app_name APP_NAME   Specify user facing name of application [default:Pirate]
#   --ume_block UME_BLOCK
#                         Specify wait for user media engagement before running [default:1]
#   --cache CACHE         md5 based url cache directory
#   --package PACKAGE     package name, better make it unique
#   --title TITLE         App nice looking name
#   --version VERSION     override prebuilt version path [default:0.2.0]
#   --build               build only, do not run test server
#   --archive             make build/web.zip archive for itch.io
#   --icon ICON           icon png file 32x32 min should be favicon.png
#   --cdn CDN             web site to cache locally [default:https://pygame-web.github.io/archives/0.2.0/]
#   --template TEMPLATE   index.html template [default:default.tmpl]
#   --ssl SSL             enable ssl with server.pem and key.pem
#   --port [PORT]         Specify alternate port [default: 8000]

cd ..
#/Users/hubertnafalski/Library/Python/3.8/bin/
#pygbag --bind 127.0.0.1 --template $project_name/default.tmpl --app_name $project_name $project_name
/Users/hubertnafalski/Library/Python/3.8/bin/pygbag --bind 192.168.1.18 --template $project_name/mobile.tmpl --app_name $project_name $project_name
cd $project_name
