# X32-OSC-Simplifier
A simple program for simplifying control of a Behringer X32 family sound board with OSC. This program was created for acting as a bridge from QLab to a Behringer X32 compact to simplify writing OSC command to control faders, mutes, and DCA assignments for theatre shows. This program is not limited to this however, and can be used as a bridge from any program that can send OSC to any X32 family console.

# Command Protocol

The address to use simple OSC commands is ```/SOSC``` (simple OSC). <br>
Anything sent to the OSC Simplifier server not on this adress will be passed directly to the X32 excactly the way it was sent to OSC Simplifier. This is to alow maximum flexibility and more advanced control if desired. 

## Command Flow and Stringing

OSC Simplifier works in a special way, in that every action is broken up into a string, for example, to mute channel 5 you would send <br>
```/SOSC "mc5:m"``` <br> 
and to unmute it you would send <br>
```/SOSC "mc5:l"```. <br>
<br>
This is remarkably flexible because it allows you to take an arbitrary number of actions in a single command, for example, <br>
```/SOSC "mc1:m" "mc2:m" "mc3:m" "mc4:l"``` <br>
would mute channels 1, 2, 3, and unmute channel 4 all in one command. See why this is so useful yet?

## Action Structure

All actions follow the basic structure: action character, channel type character, channel number, colin, parameter. <br>
For example, the action <br>
```"md4:l"``` <br>
has an action character of "m" (for mute), a channel type character of "d" (for DCA), a channel number of 4 (for DCA 4), a colon, and a parameter of "l" (for "live", meaning unmute the channel). <br>
<br>
A list of all the currently supported channel type characters and corresponding channel number ranges can be seen below.
| Channel Character | Description | Valid Channel Number Range | 
--- | --- | ---
| c | Standard input channels | 1-32 |
| a | Auxins | 1-8 |
| b | Mix Busses | 1-16 |
| d | DCAs | 1-8 |
<br>
A list of valid action characters and their valid parameters can be found in the actions section.

# Actions

## Mute ['m']
### Description
The mute action has an action character of 'm' and can be used to mute and unmute channels.
### Parameters
| Parameter | Description |
--- | ---
| 'm' | Standing for "mute", this means to mute the specified channel. |
| 'l' | Standing for "live", this means to unmute the specified channel. |
### Example Usage
```/SOSC "mc4:m"``` this action would mute standard input channel 4 <br>
```/SOSC "mc4:l"``` this action would unmute standard input channel 4 <br>
```/SOSC "mb7:m"``` this action would mute Mix Bus 7 <br>

## Fader Set ['f']
### Description
The Fader Set action has an action character of 'f' and can be used to set channel fader positions.
### Parameters
| Parameter | Description |
--- | ---
| [any number form 0.0-1.0] | this parameter sets the specified channel's fader linearly according to the number given in the parameter |
### Example Usage
```/SOSC "fc4:0.5"``` this action would set the standard input channel 4 fader to half way <br>
```/SOSC "fa4:0.0"``` this action would set the auxin 4 fader all the way down <br>
```/SOSC "fb7:1.0"``` this action would set the Mix Bus 7 fader all the way up <br>