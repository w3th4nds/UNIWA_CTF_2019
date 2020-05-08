# dizzy - Reverse challenge

First of all we run `$ strings` on our file and we see this: 
> $Info: This file is packed with the UPX executable packer http://upx.sf.net $  

That means we need to `unpack` our binary.
```sh
$ upx -d ./dizzy
```

> Ultimate Packer for eXecutables
                          Copyright (C) 1996 - 2018
UPX 3.95        Markus Oberhumer, Laszlo Molnar & John Reiser   Aug 26th 2018

        File size         Ratio      Format      Name
   --------------------   ------   -----------   -----------
    893104 <-    343652   38.48%   linux/amd64   dizzy

Unpacked 1 file.
