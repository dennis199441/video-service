# auth-service

## User authentication:
Implemented jwt authentication

## API access control
Implemented role-based authorization

Default role: Admin

The following example shows that only users with Admin or Operator roles can access `func()`
```python
@role_required(["Admin", "Operator"])
def func():
    ...
```

### Run without Docker
```
1. virtualenv env

2. source env/bin/activate

3. pip3 install -r requirements.txt

4. python3 main.py runserver
```

### Test with Docker
The following command will generate a html report under `htmlcov`
```
python3 main.py test
```


### Build
```bash
docker-compose build
```

### Run
```bash
docker-compose up -d
```

### Stop
```bash
docker-compose down
```
