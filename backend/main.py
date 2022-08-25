import threading
from grabber import main as grabber_main
from server import main as server_main

# Main entry point of the application
if __name__ == "__main__":
    # Start the grabber
    print("Sunalyzer: starting grabber thread")
    grabber_thread = threading.Thread(target=grabber_main)
    grabber_thread.start()

    # Start the server
    print("Sunalyzer: starting server thread")
    server_thread = threading.Thread(target=server_main)
    server_thread.start()

    # Wait for threads to finish
    grabber_thread.join()
    print("Sunalyzer: grabber thread exited")
    server_thread.join()
    print("Sunalyzer: server thread exited")

    # The end
    print("Sunalyzer: DONE. Everything was shut down gracefully")
