# Drop Python 3.9 support and add 3.14 support

Remove Python 3.9 support, add 3.14 support to all packages, and make 3.12 the 
default Python version.

I have installed Python 3.14.10 on the local system at @c:\dev\python3.14.10

I suggest we do it in dependency order:

umbrella -> core -> workflow -> data -> knowledge -> analysis -> discovery -> whatif -> research -> zenodo-sync

I would also suggest we first do the bare minimum to support 3.14 on each repo,
and then have a second refactoring round optimising the code to take account
of no longer having to support 3.9. This include being more deliberate about
the tooling (e.g. mypy) and dependency (e.g. pandas) versions, and not
including 3.9 "workarounds". All documentation should correctly refer to 
support for 3.10 to 3.14.

After completing this, I would then manually release each package on 
production PyPI with a 0.x.0 (no dev) version number