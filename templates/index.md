woodstock
=========
This is some introductory text.

Foo Processor
-------------
Last updated: {value foo/timestamp}

* bar: {value foo/bar}
* thing: {value foo/thing}

Plots
-----
### Time range ###

{plot foo/bar/1..99}

Series: foo/bar/1..99

Data: {value foo/bar/1..99}

### Cut ###

{plot foo/bar?foo.baz=11}

Series: foo/bar?foo.baz=11

Data: {value foo/bar?foo.baz=11}

