Manually extract USN:J

1. `fls -r -m C: \\.\C: | grep Usn`
```
0|C:/$Extend/$UsnJrnl:$J|91468-128-7|r/rr-xr-xr-x|0|0|18374796840|1364946756|1364946756|1364946756|1364946756
```
2. `icat \\.\C: 91468-128-7 > j.bin`
