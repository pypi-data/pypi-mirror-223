# Include code 
A pandoc filter to include remote files in markdown documents (mainly for github code).

# Usage
The filter looks for the class `.include-code` in the code blocks classes.

````
```{.code-include .cpp}
https://raw.githubusercontent.com/KevinSpaghetti/Raytracer/master/Output/ColorBufferFormat.h
```
```````

The link in the body of the code block will be replaced with the contents of the file.  
After the filter has replaced the link with the contents of the file the `.include-code` tag is removed.