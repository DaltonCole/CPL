# V.I.L.E. Expense Report Processor

This tool is designed to assist Carmen Sandiego with the arduous task of processing aggregated expense reports for V.I.L.E. agents.

Documentation for its behavior can be found publicly here: http://cpl.mwisely.xyz
To verify that the code works properly, compare its output against provided samples.

**Note: Follow the design specifications EXACTLY.**
Not doing so will hurt your grade.

**Note: the following commands will work on campus machines.**
**If you use your own machine or editors, you are on your own.**

## Setup Go 1.6

~~~shell
$ bash setup.sh
$ GOROOT="$(pwd)/go" ./go/bin/go version
go version go1.6 linux/amd64
~~~

## Check and Correct Style

~~~shell
$ GOROOT="$(pwd)/go" ./go/bin/go fmt main.go
~~~~

This will run the `go fmt` tool to properly format your Go code.

## Run the Program

Build and run with `go run`

~~~shell
# Listing files one-at-a-time
$ GOROOT="$(pwd)/go" ./go/bin/go run main.go Alice.dat Bob.dat

# Using a glob
$ GOROOT="$(pwd)/go" ./go/bin/go run main.go *.dat
~~~

Or build an executable.
Don't forget to recompile!

~~~shell
$ GOROOT="$(pwd)/go" ./go/bin/go build main.go
$ ./main dataDir/*.dat
~~~

**DO NOT** commit compiled files to your git repository.
