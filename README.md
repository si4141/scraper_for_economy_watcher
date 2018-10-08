# scraper_for_economy_watcher

Data reader for Economy Wacher Survey provided by Cabinet Office of Japan.
Data return as pandas.DataFrame.
It can get only current data provided [here](http://www5.cao.go.jp/keizai3/watcher-e/index-e.html) now, but is under developing to expand available data range.

# Dependency
Comming soon.
Developping in python 3.7.

# Usage
```python
reader = EconomyWatcherReader()
data = reader.get_data(kind_='current', start=datetime.datetime(2018, 1, 1), end=datetime.datetime(2018, 5, 1))
```

# Licence
MIT License

# Authors
Yuta Sugiura

# References
Comming soon
