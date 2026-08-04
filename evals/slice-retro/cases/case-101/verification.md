# Verification evidence

```
$ pytest media/test_thumbnails.py -v
media/test_thumbnails.py::test_creates_200x200_thumbnail PASSED

1 passed in 0.09s
```

Single test, single 800x600 JPEG fixture image. No other formats, sizes,
aspect ratios, corrupt files, or non-RGB color modes (e.g. CMYK, palette
GIF) were exercised.
