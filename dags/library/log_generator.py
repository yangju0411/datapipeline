from faker import Faker
import random
import concurrent.futures
from datetime import timedelta
from dateutil.parser import parse
import os

directory_list = ['/a', '/b', '/c', '/d', '/e', '/f', '/g', '/h', '/i', '/j', '/k', '/l', '/m', '/n', '/o', '/p', '/q', '/r', '/s', '/t', '/u',
'/v', '/w', '/x', '/y', '/z']
html_list =  ['/a.html', '/b.html', '/c.html']
jpg_list = ['/d.jpg', '/e.jpg', '/f.jpg']
mp4_list = ['/g.mp4', '/h.mp4', '/i.mp4']

threads = []
pool = concurrent.futures.ThreadPoolExecutor()
def generate_iu():
  faker = Faker()
  return faker.ipv4_public(), faker.user_agent()
for _ in range(1000):
    threads.append(pool.submit(generate_iu))    
iu_list = [p.result() for p in concurrent.futures.as_completed(threads)]

def generate_path(depth = 2):
    """
    Parameters
    ----------
    depth : TYPE, optional
        DESCRIPTION. The default is 2.
    Returns
    -------
    TYPE
        DESCRIPTION.
    """
    path = []
    for _ in range(random.randrange(depth + 1)):
        path.append(directory_list[random.randrange(0, 26)])
    
    file = ((html_list, jpg_list, mp4_list)[random.randrange(0, 3)])[random.randrange(0, 3)]
    path.append(file)
    
    return "".join(path), random.randrange(100, 7000)



def generate_log(date):
    """
    generate web log line
    Parameters
    ----------
    date : str
        Date the log was created
    Returns
    -------
    log : str
        web log format: {ip_address} - - {date} "{method} {path}" 200 {size} "{user_agent}"
    """
    path, size = generate_path()
    method = ["GET", "POST"][random.gauss(0.4, 0.1) > 0.6]
    ip_address, user_agent = iu_list[random.randrange(len(iu_list))]

    log = f'{ip_address} - - [{date}] "{method} {path}" 200 {size} "{user_agent}"'
    return log


def generate_file(start, end, inc, prmt, path, filename):
    """
    generate web log file

    Parameters
    ----------
    start : str
        Start time of logs
    end : str
        End time of logs
    inc : int
        Incremental of timedelta(seconds)
        Control the number of lines
    prmt: int
        Number of log populations to generate
    path: str
        Path of log file
    filename: str
        Name of log file
    """
    start = parse(start)
    end = parse(end)
    pool = concurrent.futures.ThreadPoolExecutor()

    threads = []
    log_list = []
    td = timedelta(seconds = inc)

    for _ in range(prmt):
        threads.append(pool.submit(generate_log, "****"))

    for p in concurrent.futures.as_completed(threads):
        log_list.append(p.result())

    try:
        os.makedirs(path)
    except:
        None
    with open(os.path.join(path, filename), "w") as log_file:
        now = start
        while now <= end:
            log_file.write(log_list[random.randrange(prmt)].replace("****", now.strftime("%Y-%m-%d %H:%M:%S")))
            log_file.write("\n")
            now += td