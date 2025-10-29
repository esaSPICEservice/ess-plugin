## ESS Cosmographia Plugin

The ESA Spice Service cosmographia plugin 

### Requirements

* Linux/Mac operating system
* Cosmographia 4.2
* Spice Kernel Datasets of the missions that are available at
https://www.cosmos.esa.int/web/spice/operational-kernels

### Installation

* Clone this repository

`git clone https://s2e2.cosmos.esa.int/bitbucket/scm/spice/ess-plugin.git`

### Plugin launcher (linux/macos)

* Open a terminal
* Navigate to this repository directory

`cd ess-plugin`
* Execute the generic launcher script. The first time, it will ask for the full path of the Cosmographia installation.
It saves that path in **~/.cosmo_path**. On subsequent runs, it uses the saved path automatically. You can reset the saved path anytime, deleting the file.
The launcher allows multiple options (use **-h** argument to list them):
```
Options:
  juice_ptr     JUICE pointing request plugin
  juice_mk      JUICE metakernel loader plugin
  cosmo_main    Multi-mission plugin (default)
  stardb        Run the stardb database utility
```
As example, if we want to launch the JUICE pointing request plugin, we will execute the following command:

`./plugin_launcher.sh juice_ptr`



