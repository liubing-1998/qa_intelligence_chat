import os

log_name = "test"

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(PROJECT_ROOT, log_name) + ".log"
print(PROJECT_ROOT)
print(log_path)

if __name__ == '__main__':

    pass
