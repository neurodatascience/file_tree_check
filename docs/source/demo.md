# Demo

To demonstrate some basic functionality of file tree check, lets explore the demographics of some ponds in the area and the families of ducks that live there.

## Running the Demo

### 1. Installation

Make sure you have file_tree_check and all dependencies downloaded. See [installation](https://file-tree-check.readthedocs.io/en/latest/usage.html#installation-as-cli) for details on this.
Now that you have everything installed properly navigate to your file_tree_check folder. (This is not
absolutely necessary you can just adjust inputted paths as necessary.)

### 2. First run, find  pond populations, and duck families.

To begin, let's do a a simple search of file and directorie counts.
```
tree_check -r Demo -f duck_demo -mf -md
```
`-r` is the command used to indicate directory we are searching on. (If you aren't in file_tree_check folder, prepend whatever is relevant to Demo)
`-f` is the command to indicate which file tree template we are using. In this situation the file tree is built in to file_tree_check but this can also be a path to a file tree.
`-mf` is the command to toggle file count measure.
`-md` is the command to toggle directory count measure.

After you have run that command, check your current directory for a folder called results. This is where the output is returned.
Open the 'summary.txt' file. At the top you should see a list of configurations, that is for every type of directory the differing configurations of contents.
```
Configurations for directory **pond-{pond}**:
     Configuration #1 was found in 2 directories. Contains the following:
            ['momma_duck-{momma_duck}', 'momma_duck-{momma_duck}']
     Configuration #2 was found in 1 directories. Contains the following:
            ['momma_duck-{momma_duck}', 'momma_duck-{momma_duck}', 'momma_duck-{momma_duck}', 'momma_duck-{momma_duck}']
Configurations for directory **momma_duck-{momma_duck}**:
     Configuration #1 was found in 7 directories. Contains the following:
            ['baby_duck_jpg', 'baby_duck_jpg', 'baby_duck_jpg', 'momma_txt']
     Configuration #2 was found in 1 directories. Contains the following:
            ['baby_swan-imposter.jpg']
```
This shows that two ponds have two momma ducks, and one has four. Furthermore we can see that 7 of the momma ducks have 3 ducklings and their own identification file.
One momma duck is harboring an imposter baby swan.
If you scroll down the 'summary.txt' file you will see similar information, but in a different format.

### 3. Second run, let's get more specific.

The first run gave us a pretty good idea about the demographics of the ponds and duck families, but lets dig a little deeper.
This time we will use a different file tree. It is almost the exact same except it has a sub tree that has three different kinds of ducks.
```
pond-{pond}
    momma_duck-{momma_duck}
         momma_duck-{momma_duck}.txt (momma_txt)
        -> duck_demo_sub
```
The symbol '->' indicates that a sub tree follows. Let's look at the contents of that subtree.
```
baby_duck-{baby_duck}_color-blue.jpg (blue_duckling)
baby_duck-{baby_duck}_color-yellow.jpg (yellow_duckling)
baby_duck-{baby_duck}_color-green.jpg (green_duckling)
```
In the original subtree duckling color was not specified. All different colors were grouped together.
```
         baby_duck-{baby_duck}[_color-{color}].jpg (baby_duck_jpg)
```
The '[]' indicates that this is an optional placeholder. So 'baby_duck-theduck.jpg' and 'baby_duck-theduck_color-thecolor.jpg' will both be classified as this type.

Let's try running a similar command as the first run.
```
tree_check -r Demo -f duck_demo_withsub -mf -ms
```
This time we are using `-ms` the file size measure instead of `-md` num directories measure.

Let's take a look a the 'summary.txt' file again.

Now we can see in configurations, more configurations for momma_duck directory.
```
Configurations for directory **momma_duck-{momma_duck}**:
     Configuration #1 was found in 6 directories. Contains the following:
            ['blue_duckling', 'green_duckling', 'momma_txt', 'yellow_duckling']
     Configuration #2 was found in 1 directories. Contains the following:
            ['baby_swan-imposter.jpg']
     Configuration #3 was found in 1 directories. Contains the following:
            ['green_duckling', 'green_duckling', 'momma_txt', 'yellow_duckling']
```
We can now see more specifics about the different duck families. We now see that while 7 momma ducks have 3 ducklings, one of them has two green ducklings instead of one each of blue, green, and yellow.

Continue scrolling through 'summary.txt' until you get to the file size measure and then green duckling. You can see that there are 7 ducklings with the same file size, but one of the ducklings has a size of zero.
