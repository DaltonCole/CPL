# V.I.L.E. Path Following Tool

This tool is designed to assist V.I.L.E. agents with giving directions to Carmen Sandiego, when she finds herself trapped in dangerous places including but not limited to:

* Ancient temples
* Abandoned mines
* IKEA

One wrong step could mean curtains for her.
Figuratively, or perhaps [literally](http://www.ikea.com/us/en/search/?query=curtains).

Documentation for its behavior can be found publicly here: http://cpl.mwisely.xyz
To verify that the code works properly, compare its output against provided samples.

**Note: Follow the design specifications EXACTLY.**
Not doing so will hurt your grade.

**Note: the following commands will work on campus machines.**
**If you use your own machine or editors, you are on your own.**

## Setup Go 1.6

~~~shell
$ bash setup.sh
$ ./go/bin/go version
go version go1.6 linux/amd64
~~~

## Check and Correct Style

~~~shell
$ ./go/bin/go fmt main.go
~~~~

This will run the `go fmt` tool to properly format your Go code.

## Run the Program

Build and run with `go run`

~~~shell
$ ./go/bin/go run main.go test.map
~~~

Or build an executable.
Don't forget to recompile!

~~~shell
$ ./go/bin/go build main.go
$ ./main test.map
~~~

**DO NOT** commit compiled files to your git repository.
