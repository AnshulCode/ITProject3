#Project3

cookie authenitcation which runs or port 8070

## example curl command to use
```bash
curl -d "username=srinivas&password=nicetry" \
  -c cookies.txt -b cookies.txt http://127.0.0.1:8070/
```

## other info about testing
create new cookies files each time you do the curl command use -d if you want to enter enitiy data, it is optional