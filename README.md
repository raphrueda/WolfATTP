# WolfATTP
Algorithmic Trading Testing Platform made by for SENG3011

# About
This platform takes a stock history file as input and attempts to analyse the data. Several trading strategies have been added to the platform to apply to the tick file. The idea is that we can simulate profit/loss and patterns of different trading strategies and try to find the weaknesses and strengths of each.

My contribution lies in the Java frontend developed using the JavaFX library. The frontend is resposible for first visually representing the tick file data, sending this data to the trading strategies (written using various languages) and then displaying the results of those independent modules back in the Java platform. 

Please note: This project had a limited timeline and was developed to be a prototype for a presentation demo. And so, there are many optimisations that could be made, bugs that could be squashed and features that could be completed. If testing, please follow the instructions below to ensure a smooth execution.

# Instructions
Developed for Linux and OSX

1. Open Wolf.jar

2. Open the WolfATTP/GermanCompanies.csv tick file and click Load. This step may take up to a minute depending on the machine. The company profile tab should now be filled with the tick data. You can sort by company and use the drag n drop navigation box to narrow in on a specific time span.

==NOTE==
From here on out, the application will not behave as expected for WINDOWS users
==NOTE==

3. Input a start and end year for the simulation. Choose a strategy from the preset list and fill in the parameters. Multiple parameters are accepted and are input as comma separated values. Click run when ready. This may take up to a minute depending on the machine.

4a. An excel spreadsheet or csv file will be generated on demand containing the strategy output if user's prefer that medium.

4b. The tab will automatically switch to strategy profiles. Here, you may select one of the run strategies, a company of interest and an initial investment. Click Run to see the profit/loss made from this transaction.

# Preview

![alt tag](https://puu.sh/qSsX2/ffc0be4dc9.png)

![alt tag](https://puu.sh/qSt2I/d1f5f348f5.png)

![alt tag](https://puu.sh/qSt58/ab6debad29.png)
