# HTTP_server
Python 3.6, prefork, asyncio

## nginx

sudo ab -n 10000 -c 100  http://localhost:8081/httptest/wikipedia_russia.html

This is ApacheBench, Version 2.3 <$Revision: 1807734 $>

Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/

Licensed to The Apache Software Foundation, http://www.apache.org/



Benchmarking localhost (be patient)

Completed 1000 requests

Completed 2000 requests

Completed 3000 requests

Completed 4000 requests

Completed 5000 requests

Completed 6000 requests

Completed 7000 requests

Completed 8000 requests

Completed 9000 requests

Completed 10000 requests

Finished 10000 requests


Server Software:        nginx/1.12.2

Server Hostname:        localhost

Server Port:            8081

Document Path:          /httptest/wikipedia_russia.html

Document Length:        954824 bytes

Concurrency Level:      100

Time taken for tests:   3.436 seconds

Complete requests:      10000

Failed requests:        0

Total transferred:      9550620000 bytes

HTML transferred:       9548240000 bytes

Requests per second:    2909.98 [#/sec] (mean)

Time per request:       34.365 [ms] (mean)

Time per request:       0.344 [ms] (mean, across all concurrent requests)

Transfer rate:          2714070.19 [Kbytes/sec] received



Connection Times (ms)

              min  mean[+/-sd] median   max

Connect:        0    2   1.1      1       7

Processing:     6   33   3.4     32      53

Waiting:        0    3   2.3      2      23

Total:         10   34   3.4     34      53



Percentage of the requests served within a certain time (ms)

  50%     34

  66%     35

  75%     36

  80%     36

  90%     38

  95%     39

  98%     43

  99%     46

 100%     53 (longest request)

## this server

sudo ab -n 10000 -c 100  http://localhost:8080/httptest/wikipedia_russia.html

This is ApacheBench, Version 2.3 <$Revision: 1807734 $>

Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/

Licensed to The Apache Software Foundation, http://www.apache.org/



Benchmarking localhost (be patient)

Completed 1000 requests

Completed 2000 requests

Completed 3000 requests

Completed 4000 requests

Completed 5000 requests

Completed 6000 requests

Completed 7000 requests

Completed 8000 requests

Completed 9000 requests

Completed 10000 requests

Finished 10000 requests





Server Software:        Andrey

Server Hostname:        localhost

Server Port:            8080



Document Path:          /httptest/wikipedia_russia.html

Document Length:        954824 bytes



Concurrency Level:      100

Time taken for tests:   7.468 seconds

Complete requests:      10000

Failed requests:        0

Total transferred:      9549790000 bytes

HTML transferred:       9548240000 bytes

Requests per second:    1339.06 [#/sec] (mean)

Time per request:       74.679 [ms] (mean)

Time per request:       0.747 [ms] (mean, across all concurrent requests)

Transfer rate:          1248799.78 [Kbytes/sec] received



Connection Times (ms)

              min  mean[+/-sd] median   max

Connect:        0    1   2.5      0     138

Processing:     9   74  32.4     70     240

Waiting:        1   43  22.4     40     207


Total:          9   74  32.4     70     240


Percentage of the requests served within a certain time (ms)

  50%     70

  66%     80

  75%     88

  80%     92

  90%    105

  95%    126

  98%    188

  99%    203

 100%    240 (longest request)

