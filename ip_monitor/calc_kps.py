import time

time_interval_in_seconds = .5

def run(connections, logwriter):
    logwriter.write('error', 'calc_kps running')
    while True:
        time.sleep(time_interval_in_seconds)
    
        for connection in connections:        
            kps = connection.data_temp / time_interval_in_seconds / 1000
            connection.kps = kps
            connection.data_temp = 0
