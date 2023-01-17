## Настройка dotenv

[dotenv](https://pypi.org/project/python-dotenv/)

`pip install python-dotenv`

```python


from pathlib import Path
import os
from dotenv import load_dotenv
from django.contrib.messages import constants as messages

# Loading ENV
env_path = Path('.') / '.env'

#env_path = '.test.env'
load_dotenv(dotenv_path=env_path)
```

