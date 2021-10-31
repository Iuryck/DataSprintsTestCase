# DataSprints Technical Test Case

**This repository is for the recruitment test case for the Data Scientist Jr position at DataSprints**

# Cloud

Link to Clone from Saturn Cloud (need to contact me to authorize sharing through username):
https://app.community.saturnenterprise.io/dash/resource?sourceId=af18c1c821c1473da255dd304a700870&resourceType=Jupyter%20Server


# Requirements

These are the installs needed to reproduce the code in this repository :

pandas==1.3.4

numpy==1.20

plotly==5.3.1

datashader==0.13.0

dash==2.0.0

python==3.8.12

# Getting started

First you will need to clone the repository

```
git clone https://github.com/Iuryck/DataSprintsTestCase.git
```

Next, you need to add the data from the test case into the same folder with these code files (Trips data, vendors data, etc). After that, you can run **Load_Data.py** to load the files and create the **Trips_and_Vendors.db** file so you can run each code according to the tasks it solves. Or you can just run the Jupyter Notebook and it will do everything. And you're all set!


# Notes

For the live data streaming and data plot, I was able to do both fake JSON data stream and do a live plot of a metric in real time. **But** the plot was done within a Dash app, which runs on a local IP which you need to open on a browser page to visualize. In other words, **the plot does not appear in analysis.html**. To see the plot you will need to run the Bonus_3.py code locally, and then follow the Ip address to the plot. I hope this is not much of a problem.
