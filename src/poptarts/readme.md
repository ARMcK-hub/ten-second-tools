# POptArts
poptarts, or PowerShell Option Arguments, is just that - template code, bringing the functionality of PowerShell's Opt Args to shell scripts.

poptarts' development was influenced by the developers personal needs to making shell scripts more user-friendly and includes the following features:
- helpFunction: a helper function that displays general usage information
- getops: parsing and mapping of input $OPTARGS
- emptyEcho: echo which parameters are empty and display the helpFunction

## Usage
Usage is simple! Copy and paste, changing parameters as seen fit.

Code to modify to match your inputs:
- helpFunction: Usage and each parameter flag/description
- getopts: parameter flags and script name mapping
- emptyEcho: each script parameter

> Note: you can view an example implementation of POptArts used in [`nSync`](../nsync/).