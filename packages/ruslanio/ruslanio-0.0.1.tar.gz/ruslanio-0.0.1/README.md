# My personal tools for my projects

* `from ruslanio import imread` - like `cv2.imread` but reads RGB and supports `pathlib.Path`
* `ruslanio.beam_search` - multi-purpose beam search
* `ruslanio.cacher` - LRU cache supports async functions and Redis

## Installation

```bash
pip install -U git+https://github.com/hocop/ruslanio.git
```

Or

```bash
git clone https://github.com/hocop/ruslanio
cd ruslanio
./setup.sh
```
