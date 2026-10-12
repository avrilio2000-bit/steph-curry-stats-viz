Stephen Curry Career Playoff Scoring Analysis (2013–2023)

A Python data analysis project evaluating Stephen Curry's postseason scoring performance against rival NBA franchises using Pandas and Matplotlib.

Project Output
[Steph Curry Playoff Scoring](steph_curry_playoffs.png)

What it does
- Reads postseason game data from Kaggle (`Stephen Curry Postseason Stats.csv`)
- Filters out teams he faced fewer than 4 times (minimum 1 full playoff series)
- Uses `pandas` to group by team and calculate average points per game
- Uses `matplotlib` + `Pillow` to handle transparency and attach the `.gif` logos along the bottom

Tools Used
* Python
* Pandas (Data Cleaning & Aggregation)
* Matplotlib & Pillow (Data Visualization & Image Processing)
* Kaggle Dataset (14 Seasons of Game Logs)
