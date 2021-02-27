crtxplore
---------
Certificate Explore - find subdomains using Certificate Transparency logs.

> :information_source: This tool is slightly improved version of [UnaPibaGeek/ctfr](https://github.com/UnaPibaGeek/ctfr). 

#### Usage 
```
crtxplore.py [-h] -d DOMAIN [-ew] [-ee] [-t TIMEOUT] [-o OUTPUT_FILE_PATH]
```

#### Arguments:  

| arg | Name | Description |
| --- | ---- | ----------- |
| `-d` | domain | Target domain (required) |
| `-ew` | exclude_wildcard | Exclude wildcard subdomains (eg. _*.uber.com_) |
| `-ee` | exclude_expired | Exclude expired certificates |
| `-t` | timeout | Timeout |
| `-o` | output | Output file path |  

#### Example output
```
> python crtxplore.py -d uber.com -ew -t 5          
automate.sandbox.cpe.uber.com
prj.usuppliers.uber.com
cn-slow2.uber.com
accessibility.uber.com
brand.uber.com
dca1-resilient.corp.uber.com
cn-slow1.uber.com
investor.uber.com
prod2.uber.com
jira.uber.com
dca1-dc07.corp.uber.com
bizblog.uber.com
stapler.uber.com
...
```