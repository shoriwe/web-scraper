# web_scrap

## Descripcion

Esta script mapear un sitio web y es capaz de descargarlo, puede escribir un archivo .json para guardar el mapeo realizado,
tambien es capaz de amalizar hasta sierto alcance el sitio web por medio de una variable llamada profundidad.

## Uso
```python
url = 'https://en.wikipedia.org/wiki/Roy_Clark'
descargar = True
profundidad = 2
archivo = clark.json
s = Scraper()
s.lineal(url,profundidad,descargar,archivo)
```
