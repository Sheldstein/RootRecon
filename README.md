# RootRecon
A more practical way to manage AS and IP prefixes while doing ASN Recon

# Disclaimer
This tool is made for responsible use only, the developpers reject any responsability regarding its use.

This tool is still under development, so you can expect some bugs. Please share them to allow us to improve it.

# Installation
1. Clone this repositery : `git clone https://github.com/Sheldstein/RootRecon.git`
2. Install requirements : `pip3 install -f requirements.txt`

# Usage
Launch the console with :
`python3 RootRecon.py`

Some useful commands :
`get -s cie_name` : Searches ASN belonging to cie
`get -s cie_name -d save_directory` : Searches ASN belonging to cie and save it to save_directory

Default mode is using the build-in console, but you can also pass a get command as arguments for your automation, which does not start the console:
`python3 RootRecon.py get -s cie_name -d save_directory`

For more help, you can check the build-in help : just type any command's name followed by '-h'. You can find  the list of commands just by pressing 'Enter' in the console.

# Credits
This tool was inspired by the work of j3ssie [metabigor](https://github.com/j3ssie/Metabigor) and of yassineaboukir [Asnlookup](https://github.com/yassineaboukir/asnlookup), check their work.
