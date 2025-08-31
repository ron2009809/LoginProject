# counter = 0
# def add_to_counter():
#     global counter
#     for number in range (100000):
#         counter = counter + 1
#
# for i in range (5):
#     add_to_counter()
#
# print("Final counter value (no threading): ", counter)
import threading
import time

counter = 0
lock = threading.Lock()
results = [0,0,0,0,0]
def add_to_counter(thread_number):
    global counter
    for number in range(100000000):
        counter = counter + 1
    results[thread_number] = counter

threads = []

start_time = time.time()

for thread_number in range(5):
    new_thread = threading.Thread(target = add_to_counter, args=(thread_number,))
    new_thread.start()
    threads.append(new_thread)

for thread in threads:
    thread.join()

end_time = time.time()

print("Final counter value:", counter);
print("Execution time:", end_time - start_time, "seconds");