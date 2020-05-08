# dizzy - Reverse challenge

First of all we run `$ strings` on our file and we see this: 
> $Info: This file is packed with the UPX executable packer http://upx.sf.net $  

That means we need to `unpack` our binary.
```sh
$ upx -d ./dizzy
```

```sh
Ultimate Packer for eXecutables
                          Copyright (C) 1996 - 2018
UPX 3.95        Markus Oberhumer, Laszlo Molnar & John Reiser   Aug 26th 2018

        File size         Ratio      Format      Name
   --------------------   ------   -----------   -----------
    893104 <-    343652   38.48%   linux/amd64   dizzy

Unpacked 1 file.
```
Now we can open it with `ghidra`. 
`main` looks like this:
```c
undefined8 main(void)

{
  uint uStack12;
  
  uStack12 = 0;
  puts(&UNK_0049b0ce);
  puts(&UNK_0049b0e8);
  puts(&UNK_0049b120);
  __isoc99_scanf(&UNK_0049b154,&uStack12);
  sub_1312((ulong)uStack12);
  return 0;
}
```
That means it takes our input via `scanf` and calls `sub_1312`.  `
```c
void sub_1312(int param_1)

{
  char local_17;
  char local_16;
  char local_15;
  char cStack20;
  char cStack19;
  char cStack18;
  char cStack17;
  char cStack16;
  char cStack15;
  char cStack14;
  char cStack13;
  undefined4 local_c;
  
  if (param_1 == 0) {
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  system("clear");
  puts("You managed to get here, gj mate!\n");
  puts("Now it\'s time to validate the flag and get to know my name: \n");
  __isoc99_scanf(&DAT_0049b076,&local_17);
  local_c = 0;
  if (local_17 == '1') {
    local_c = 2;
    if ((((((local_15 == '4') && (local_c = 5, cStack18 == 't')) && (local_c = 1, local_16 == '_'))
         && ((local_c = 4, cStack19 == '_' && (local_c = 3, cStack20 == 'm')))) &&
        ((local_c = 6, cStack17 == 'h' &&
         ((local_c = 10, cStack13 == '$' && (local_c = 7, cStack16 == '4')))))) &&
       ((local_c = 8, cStack15 == 'n' && (local_c = 9, cStack14 == '0')))) {
      puts("Congratulation! You got the right flag! You have patience..\n");
    }
    return;
  }
  puts("Almost got it..\n");
                    /* WARNING: Subroutine does not return */
  exit(1);
}
```
After we pass the first test, we need to provide a flag to be validated. Our flag is stored in `local_17`.  
We can see that in order to get the `Congrats` message, all the above comparisons must be true.  
So, we can either do this inside `gdb` or the easiest way is to just take each "comparison" and rearrange it according to the vatiables.  
> char local_17; // 1
  char local_16; // _
  char local_15; // 4
  char cStack20; // m
  char cStack19; // _
  char cStack18; // t
  char cStack17; // h
  char cStack16; // 4
  char cStack15; // n
  char cStack14; // 0
  char cStack13; // $
  
 **Flag: UNIWA{1_4m_th4n0$}**
  
  
