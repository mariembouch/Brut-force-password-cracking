import socket
import time
import threading

def main():
    target_password = "A234"  # Password to find (you can set it here)
    num_workers = 3  # Number of worker threads

    stop_event = threading.Event()  # Event to signal workers to stop searching
    result_event = threading.Event()  # Event to signal password found

    results = []
    worker_sockets = []

    # Create a socket server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("192.168.0.25", 12345)  # Replace with your server IP and port
    server_socket.bind(server_address)
    server_socket.listen(num_workers)

    character_sets = [
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ]
    start_time = time.time()
    threads = []

    # Accept connections from workers
    for _ in range(num_workers):
        worker_socket, _ = server_socket.accept()
        worker_sockets.append(worker_socket)

    # Assign character sets to workers and send initial data
    for i, (worker_socket, character_set) in enumerate(zip(worker_sockets, character_sets)):
        print(f"Worker {i + 1} is testing password with character set: {character_set}")

        # Send data to the worker
        data = f"{target_password},{character_set}"
        worker_socket.send(data.encode('utf-8'))

        # Start worker threads
        thread = threading.Thread(target=worker_thread, args=(worker_socket, results, stop_event, result_event, worker_sockets))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    found = result_event.is_set()

    # Close the server socket after processing
    server_socket.close()

    end_time = time.time()
    elapsed_time = end_time - start_time

    if found:
        print(f"Password found: {target_password}")
        stop_event.set()  # Signal all workers to stop
    else:
        print("Password not found.")

    print(f"Time elapsed: {elapsed_time} seconds")

def worker_thread(worker_socket, results, stop_event, result_event, worker_sockets):
    try:
        while not stop_event.is_set():
            data = worker_socket.recv(1024)  # Adjust the buffer size as needed

            if not data:
                print("No data received from the worker.")
                return

            data_str = data.decode('utf-8')
            result = data_str

            results.append(result)

            if result == "Password found":
                stop_event.set()
                result_event.set()

                # Notify all workers to stop
                for ws in worker_sockets:
                    ws.send("stop".encode('utf-8'))
                break
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
