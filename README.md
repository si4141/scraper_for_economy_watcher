# DataReader for Economy Watcher Survey

Data reader for Economy Watcher Survey provided by Cabinet Office of Japan.
Data returned as pandas.DataFrame.
It can get only data provided [here](http://www5.cao.go.jp/keizai3/watcher-e/index-e.html) now, but is under developing to expand available data range.

# Dependency

Developed in python 3.7.

# Install


# Usage

```python
from econ_watcher_reader import EconomyWatcherReader
reader = EconomyWatcherReader()
data = reader.get_data(kind_='current', start=datetime.datetime(2018, 1, 1), end=datetime.datetime(2018, 5, 1))
```

If you want data about future,

```python
reader = EconomyWatcherReader()
data = reader.get_data(kind_='future', start=datetime.datetime(2018, 1, 1), end=datetime.datetime(2018, 5, 1))
```

# Licence

MIT License

# Authors

Yuta Sugiura

# References

Data Sorce

- [Cabinet Office](http://www.cao.go.jp)
- [Economy Watcher Survey](http://www5.cao.go.jp/keizai3/watcher/watcher_menu.html)
