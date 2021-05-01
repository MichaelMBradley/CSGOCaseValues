# CSGOCaseValues

***PLEASE* DO NOT BUY CASES TO MAKE MONEY. IF YOU LOOK AT THE DATA PRESENTED AND STILL BELIEVE THAT YOU HAVE A CHANCE THEN IT'S YOUR OWN FAULT IF YOU LOSE ALL OF YOUR MONEY. THIS PROJECT IS PURELY FOR MY OWN INTEREST.**

**GAMBLING IS ADDICTIVE. IF YOU BELIEVE YOU HAVE A GAMBLING ISSUE, PLEASE SEEK HELP. IF YOU DON'T BELIEVE YOU HAVE A GAMBLING ADDICTION, A LITTLE INTROSPECTION NEVER HURT ANYONE.**

## About

Estimating expected value of each case in CSGO, using data scraped from CSGOStash. In the future, I hope to use a different source, either reading directly from Steam or through some API.

## Example

When reading the sample data the output is:

```text
EV      (Value  Price)  Name
0.8657  ( 6.10   7.05)  CS:GO Weapon Case 3
0.7453  ( 7.21   9.68)  CS:GO Weapon Case 2
0.7176  ( 2.33   3.25)  Revolver Case
0.6865  ( 5.57   8.11)  eSports 2013 Winter Case      
0.6834  ( 2.41   3.52)  Operation Wildfire Case       
0.6755  ( 2.76   4.08)  Operation Broken Fang Case    
0.6647  ( 2.32   3.49)  Chroma 2 Case
0.6463  ( 2.49   3.85)  Fracture Case
0.6259  ( 2.55   4.08)  Operation Vanguard Weapon Case
0.6107  ( 2.07   3.39)  Shadow Case
0.6065  ( 2.63   4.34)  Shattered Web Case
0.6008  ( 2.11   3.51)  Gamma Case
0.5963  ( 2.50   4.20)  Chroma Case
0.5918  ( 2.05   3.46)  Falchion Case
0.5853  ( 2.50   4.27)  Operation Phoenix Weapon Case
0.5785  ( 1.90   3.28)  Chroma 3 Case
0.5748  ( 1.86   3.23)  Prisma 2 Case
0.5651  ( 7.20  12.74)  Operation Hydra Case
0.5642  ( 2.22   3.93)  Spectrum Case
0.5560  ( 3.86   6.95)  eSports 2014 Summer Case
0.5509  ( 1.78   3.23)  Prisma Case
0.5377  ( 1.75   3.26)  Horizon Case
0.5317  ( 1.88   3.54)  Gamma 2 Case
0.5260  ( 4.27   8.11)  Winter Offensive Weapon Case
0.5151  ( 1.69   3.29)  CS20 Case
0.5122  ( 1.76   3.44)  Spectrum 2 Case
0.5015  ( 1.62   3.24)  Danger Zone Case
0.4918  (26.99  54.88)  CS:GO Weapon Case
0.4759  ( 1.67   3.51)  Clutch Case
0.4589  ( 3.87   8.43)  Huntsman Weapon Case
0.4572  ( 2.55   5.58)  Operation Breakout Weapon Case
0.4341  ( 2.09   4.81)  Glove Case
0.3698  (16.72  45.22)  Operation Bravo Case
0.2369  ( 8.06  34.04)  eSports 2013 Case
```

The sample data was recorded on 2021/04/09, and this output can be generated with:

```python
printsortedcaselist(analysis())
```
