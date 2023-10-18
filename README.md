# nested-godot-project-manager
CLI that helps manage nested godot projects

# motivation
to get started, suppose we have two separate godot projects (directories containing a `project.godot` file in their respective roots) `A` and `B`, suppose we'd like to use `B` inside of `A`, suppose that we place `B` inside of `A` like so: `A/B`, unfortunately this will not work correctly and godot will throw errors because:
* inside of any `*.tscn` file in `B`, all `res://...` links will break because they are relative to the root of `B`, they need to be correct to be `res://B/...`
* the godot ide will complain if there is more than one `project.godot` file in the project, which there now is because of `A/project.godot` and `A/B/project.godot`

# usage
Consider the setup as described in the motivation, next clone in `ngpm` with `git clone git@github.com:frag-z/nested-godot-project-manager.git` in the root directory of `A` and change directory to `nested-godot-poject-manager` and then run `python ngpm.py -nest` you should now be able to successfully open the root project within godot and make changes.

# suggested organizaion
suppose you have two godot projects `A` and `B`, create github repositories for each one, next inside of `A` use git submodules to add `B` dependency (`git submodule add git@github.com:<TODO>/B.git`), and use `git submodule update --init --recursive` to clone in all the content, and if `B` relied on another project say `C`, that would also be cloned in as well.

At this point `A` is probably going to throw a ton of errors if opened in godot because of the issues described in the motivation, so we clone (or add as a submodule) in this project inside of the root of `A` follow the usage as described above, when done editing if you'd like to revert the changes close godot and run `python ngpm.py -un-nest`.
# notes
there are [potential plans](https://github.com/godotengine/godot-proposals/issues/1205) for subprojects but as of right now, there's not a simple way to work with them. 

Also one day if we do get sub-projects supported within godot, most likely you will manage your subproject with git, and then godot will have some method of nesting them them by specifing a subproject to be nested, that is to say for most developers git is going to be part of the equation in some way, so using submodules is another valid route that doesn't add anything new to the tech stack
