# Images

A collection of MatPlotLib renders of data collected with this code.

Before reading this material, it is important to remember that an expected value is an *average*. If you open 10 cases each with an expected value of 0.7, it would not at all be surprising to lose much more than 30% of your money, as for many cases knives/gloves make up a significant portion of the expected value and it is unlikely that you would get one so quickly. If a case has an expected value of 0.7 (which is very high for a case!), I expect that you may have to open thousands before the expected value prediction becomes accurate.

For example, imagine a game in which every time you play a round you lose $1000. However, there is a one in a billion change that you win $10 trillion. Theoretically speaking, this game has an expected value of approximately 10, meaning that if you played forever you could expect to win 10 times the amount that you put in. However, in practice all that would happen is that you would quickly go bankrupt as you would lose all of your money long before winning the big prize. In much the same way, even if there is a case with an expected value grater than 1, don't realistically expect to make money off of it without investing thousands, if not tens of thousands (and at that point the increased supply of skins you'd create would drive down prices, likely ultimately putting the expected value back below 1 which would make you lose money).

***DON'T BUY CASES***

## Expected value

![plotcases(readhistoricaldata())](https://raw.githubusercontent.com/MichaelMBradley/CSGOCaseValues/master/img/expectedvalue.png)

Here are presented the expected values of each case in CS:GO. You'll notice that every single value is below 1, and that most hover around the 0.5 mark. This means that there is no case that will make you money, and most cases will make you lose half of your money.

Generated on 2021-04-30 with:

```python
plotcases(readhistoricaldata())
```

## Relative pricing

![plotRelativePrices(prices, skinfo, skins)](https://raw.githubusercontent.com/MichaelMBradley/CSGOCaseValues/master/img/relativepricing.png)

This image displays the relative average prices of the different wears as a multiple of the average price of the battle-scarred non-StatTrak skin. The subplots are divided by the rarity of the skins in question. Interestingly, the prices of well-worn skins are (in general) higher than the prices of field-tested skins.

Generated using the sample data on 2021-04-30 with:

```python
cases, skins, skinfo, prices, caseCost = readinfo()
plotRelativePrices(prices, skinfo, skins)
```

## Expected value from a drop

![plotcases(groups(readhistoricaldata(), ["Drops"]), value=lambda case: case.EVD, area=None)](https://raw.githubusercontent.com/MichaelMBradley/CSGOCaseValues/master/img/expectedvaluedrop.png)

Now, you may be wondering about how well you could fare by opening case that you recieved in game, so the only cost is that of the key. For the above image, the CS:GO Weapons Case and the Operation Bravo case have such a large expected value from a drop that it is hard to make out the rest of the values, so I've produced a trimmed version below.

![plotcases(groups(readhistoricaldata(), ["Drops"]), value=lambda case: case.EVD, area=(0, 2.5))](https://raw.githubusercontent.com/MichaelMBradley/CSGOCaseValues/master/img/expectedvaluedroptrim.png)

In this trimmed image, you can more clearly see the lower expected values for dropped cases. Again, it is important to remember that an expected value is an average, and in practice is not representative of what you would get by opening a case or two.

Generated on 2021-04-30 with:

```python
plotcases(groups(readhistoricaldata(), ["Drops"]), value=lambda case: case.EVD, area=None)
```

and

```python
plotcases(groups(readhistoricaldata(), ["Drops"]), value=lambda case: case.EVD, area=(0, 2.5))
```

## Probability of opening a profitable skin

![plotcases(groups(readhistoricaldata(), ["Drops"]), value=lambda case: case.prob, area=(0, 0.25))](https://raw.githubusercontent.com/MichaelMBradley/CSGOCaseValues/master/img/probprofit.png)

Here, you can see the probability than any given skin you open from each case will be worth than the cost of the case. This is not the same as they expected value, as this does not take into account how much more or less the skin will be worth compared to the cost of opening, only whether or not it will be more. I would argue that this presents a slightly more realistic visualization of what the average person just opening a few cases can expect. Note that all but four cases have a probability of instant profit of under 10%.

Generated on 2021-04-30 with:

```python
plotcases(groups(readhistoricaldata(), ["Drops"]), value=lambda case: case.prob, area=(0, 0.25))
```

## Probability of opening a profitable skin from a drop

![plotcases(groups(readhistoricaldata(), ["Drops"]), value=lambda case: case.probdrop, area=(0, 1.1))](https://raw.githubusercontent.com/MichaelMBradley/CSGOCaseValues/master/img/probdropprofit.png)

***THE FOLLOWING TEXT ONLY APPLIES TO CASES THAT ARE DROPPED IN GAME. IF YOU BUY CASES, THE COMMENTS MADE BELOW DO NOT APPLY***

This is a very similar metric to the image above, however this graph represents the chance of profitting off of a dropped case, so the only cost is that of the key. By this graph, if you are dropped a CS:GO Weapon Case, other than that, you're still out of luck.

Generated on 2021-04-30 with:

```python
plotcases(groups(readhistoricaldata(), ["Drops"]), value=lambda case: case.probdrop, area=(0, 1.1))
```
