# Pirate

Educational project based on course prepared by **Clear Code**: 
[Creating a Mario style platformer in python with Pygame](https://www.youtube.com/watch?v=KJpP85tnOKg&t=2s&ab_channel=ClearCode "Youtube")

All the credit goes to @clear-code-projects:
https://www.patreon.com/clearcode

Original author's repo: 

https://github.com/clear-code-projects/2D-Mario-style-platformer

## Play on-line:
[Pirate on itch.io!](https://hubertnafalski.itch.io/pirate)

## My additions are:

- integration with pygbag (Webassambly) to run game in **browser** (also on **mobile** phones - tested on **Android**, currently not working on iOS)
- additional control handling (**touchscreen** and **gamepad**)
- debug features (config and GUI - still in progress)
- regening health when collecting hearts
- **level 4** prepared by my sons (**Tymon & Mateusz**)
- screen resolution detection and fullscreen mode

## Control mapping

| Action      | Keyboard |  Gamepad |
| --------- |:-----:|:---------:|
| move left | left arrow | L joystick left |
| move right | right arrow | L joystick right |
| jump/select | space | A |
| back/quit | q, Esc | B |
| debug view | ~ | X |

Gamepad functionality tested using Xbox One Wireless pad.
On Mac there was problem of detecting gamepad, but after installing this tool it all worked as on Windows:
[https://generalarcade.com/gamepadtool/](https://generalarcade.com/gamepadtool/)

debug view requires GOD_MODE flag in settings.py to be set to True 

## Compatibility

| Browser OS | Windows | Linux | Mac | Android | iOS |
| ---- | ---- | ---- | ---- | ---- | ---- |
| Chrome | :white_check_mark: works | :question: not tested | :white_check_mark: works | :white_check_mark: works | :x: hangs |
| Safari | :question: not tested | :question: not tested | :x: hangs | :question: not tested | :x: hangs |
