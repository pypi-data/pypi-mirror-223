# spirits

make and compose spirits images

> `pip install spirits`

```bash
# make spirits
spirits scatter example/pypi_logo.png 3 3 # default output dir: ./output
spirits scatter example/pypi_logo.png 3 3 --output-dir example/output

# compose spirits
spirits gather example/compose-4.png example/output/0-0.png example/output/0-1.png example/output/1-0.png example/output/1-1.png  --row 2 --column 2
spirits gather example/compose.png --file example/images.list --row 3 --column  3
```

