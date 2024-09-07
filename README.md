# diskspaced

This is a Python based CLI utility to find what is taking space on your disk. It's originally designed to export into a format that [GrandPerspective](https://grandperspectiv.sourceforge.net/) can render, but the exports can be XML (for GrandPerspective) or JSON. 

Simply install via pip (or package management tool of your choice), then run:

```bash
diskspaced --folder-path / --output-path output.xml --format grandperspective
```

This will run through your disk and write out the results. Running with sudo gives the most accurate results. 

Note: Windows is not supported by this tool. 

### Required options

* `--folder-path` - The root folder to start off with. Usually set to `/`
* `--output-path` - The file to write the output to.
* `--format` - The output file format. Currently JSON or GrandPerspective. (`json` and `grandperspective` respectively)

### Other options

* `--pretty-print` - Set this to pretty print the output (if supported by the format) - Note that this is a post processing step rather than an inline step.
* `--print-after-n-files N` - Printing every file processed would make the entire process take several orders of magnitude longer. Instead, if you'd like to see output, you can set this flag, and give a value `N` and it will print every `N`th file.
* `--alphabetical` - This ensures that the output order is alphabetical (i.e. stable). This is only really useful if you plan on diffing outputs. 
