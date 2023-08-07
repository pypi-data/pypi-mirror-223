from setuptools import setup, find_packages

name = "rwai"
version = "0.1.1"
description = "Фановый ИИ основаный на Ваших словах"
long_description = """
RWAI (Random Words AI) - это фановый искусственный интеллект, который генерирует случайные ответы 
на основе ваших слов. Просто отправьте ему сообщение, и он вернет вам случайные слова из 
сохраненного списка. RWAI может использоваться для забавных разговоров, создания случайных 
фраз или просто для удивления ваших друзей.

Установка:
```py
pip install rwai_ru
```

# Пример использования:
```py
from RWai import rwai
response = rwai.send("привет!")
print(response)
```
"""
author = "barlin41k"
author_email = "sasaigrypocta@gmail.com"
install_requires = [
    "barladb"
]
packages = find_packages()
keywords = ["rwai", "randomword", "randomai"]
license = "MIT"

setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=author,
    author_email=author_email,
    packages=packages,
    install_requires=install_requires,
    keywords=keywords,
    license=license,
)