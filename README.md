# mergepbx #

A tool for merging Xcode project files in git

Version: 0.6 - 2nd Oct 2014
Status: Alpha

* Follow us on twitter: https://twitter.com/mergepbx
* Website: http://simonwagner.github.io/mergepbx/

Buy me a cup of tea: [![Donate to mergepbx](https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=UX3YTWH8DRYVN)

## Why mergepbx? ##

Tracking a Xcode project in a version control system is annoying. Simply adding files can lead to merge conflicts that have to be solved manually, although it would be possible to resolve the conflict automatically, if the merge algorithm would be aware of the structure of Xcode's project file.

After long and annoying merge sessions in one of my projects, I came to the conclusion, that writing a merge driver for git which understands the structure of the project file would be a worthwhile endeavour, as it would save me from solving the merge conflicts for my co-workers.

Unfortunately, that script was finished only after the project ended. However, as I didn't want to let the work go to waste, this script is now published as open source under the GNU GPL 3.

## Status ##

This script needs knowledge about the structure of Xcode's project. However, there doesn't seem to be any documentation (and I would be surprised if there were any). Luckily, the format of the project file is a plain text Plist, so reverse engineering the structure is rather easy.

Nevertheless, I do not know all possible variants of project files that are out there. Currently, this script works for the projects I worked on, however, you might encounter a project file that has some structures in it that I haven't seen yet.

If the script doesn't work, you might want to open an issue and attach your project file to it.

Note also, that this script can't solve conflicts, that are really conflicts. For example, if you rename a file and a co-worker of yours is going to delete it, well, then you are going to end up in a pretty weird state.

## Usage ##

To use this script, you have to configure it as a merge driver for you project file. To do this, you have to take the following steps:

### Building ###

Execute the following command in the directory of the cloned project:

```
./build.py
```

That should build the mergepbx executable that you can use. It is a specially crafted zip file that contains all needed python files and can directly be executed on the commandline

### Using mergepbx as merge tool ###

You can add mergepbx as a merge tool, so you can use it to manually start merging the project file with `git mergetool --tool=mergepbx PROJECT.pbxproj`.

#### Add mergepbx as a merge tool ####

Open `~/.gitconfig` (create if it does not exist) and add the following lines to it:

```
#driver for merging Xcode project files
[mergetool "mergepbx"]
	cmd = mergepbx "$BASE" "$LOCAL" "$REMOTE" -o "$MERGED"
```

#### Merging project files ####

After you have encountered a failed automatic merge, you can now use the following command to start the automatic merge with `mergepbx`:

```
git mergetool --tool=mergepbx PROJECT.pbxproj
```

Afterwards, the project file should be merged and marked as resolved.

### Using mergepbx as a merge driver ###

You can also configure git to always use `mergepbx` automatically, when it encounters a conflict in a project file

Open `~/.gitconfig` (create if it does not exist) and add the following lines to it:

```
#driver for merging Xcode project files
[merge "mergepbx"]
        name = Xcode project files merger
        driver = mergepbx %O %A %B
```

Replace mergepbx with the path to the file you downloaded (You might want to add that file to your $PATH)

#### Configure your repository to use the driver ####

In your repository root directory, open the file `.gitattributes` (create if it does not exist). Add the following lines to it:

```
*.pbxproj merge=mergepbx
```

#### Merging project files ####

If you merge branches with git now, git will automatically use mergepbx for .pbxproj files. You don't have to do anything special, simply merge your branches as before.

Note that this script is not really fast, I didn't optimize it for speed and especially the plist parser is not very fast.

## Alternatives ##

An alternative to using this script, is to use the union merge driver of git, by adding the following line to `.gitattributes`:

```
*.pbxproj merge=union
```

This tells git to combine the files by adding lines from both, the remote file and your local file. That works most of the time, however it is not bulletproof, as git still has no idea what it is doing here.
If my script does not work for you, you can however try out this strategy.

## How to help ##

If you encounter a project file that can not be parsed, please open an issue and attach the project file to it. I will then take a look at it and add the missing parts to the script

## Disclaimer ##

This code published here and any programs that are created from it are not claimed to be fit for any purpose.
Running them might lead to your project being eliminated, kittens killed and the end of the world.

Be careful, you have been warned!

## Contributers ##

* Simon Wagner
