# cgrputil
[![image](https://img.shields.io/pypi/v/py-package-template.svg)](https://pypi.org/project/cgrputil/)
[![Downloads](https://pepy.tech/badge/cgrputil)](https://pepy.tech/project/cgrputil)

**cgrputil** is python library to calculate cpu utilisation of code over specific time interval inside docker container. 

Usage of the library can vary, Eg. Think about the use case where you want to know how much specific function consume a cpu over specific time and on the basis of that you want to bill the client or draw charts to understand the growing trend of function.

I was struggling with the same problem, & searched all over internet. But i didnt get anything solid,
& all of the docs, the repos i viewed, code i read, almost pointed to docker repo which had calculation formula.
So seeing the problem & number of resources available for such typical problem i decided to create the library.
I wanted solution which is very easy to use and focus on giving end result, so i tried it making as simple as i could.
I hope this helps :) .

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install cgrputil.

```bash
pip install cgrputil
```

## Usage

```python
import cgrputil

'''
Class instantiation expects default param, which will be return in case of any failure 
while reading, calculating cpu usage. We suggest to send this value as maxm number of 
cores allocated to container.
This value can be pass in two ways either passing it while class instantiation, which is in 
example below i.e 3 or setting it inside env variable `RES_CPU_LIMIT`. 
Library will fist check for the value pass and then for the env variable, on of them is mandatory
else exception will be raised.
'''
cpu = cgrputil.cpuutilisation(3)


#From this point, it will calculate the cpu utilisation
cpu.start_time()

activity_you_want_to_calculate_cpu_usage()

#Until this point cpu usage will be calculated 
cpu.end_time()

'''
This will return the aprox cpu cores used while executing in between start time and end time.
Return format is float. So if it returns 2.3 that means above function have consumed 2.3 cores
out of all the cores available on the host or you can say 2.3 cores out of 3 
cores (3 assuming maximum cores allocated to container).

Function returns two values, first is list of errs or exception occured while calculating cpu usage.
Second the actual usage value. If the errs list is not empty it will most likely to return the 
default value passed while initiating the class. Ex. cpu = cgrputil.cpuutilisation(3) which is 3 here.
'''
errs, cores_used = cpu.get_core_utilisation()
if errs is not None:
    for err in errs:
        print(err)
    print('Utilisation : ', cores_used)        
else:
    print('Utilisation : ', cores_used)  
```

## Contributing
Pull requests are welcome. For any changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
