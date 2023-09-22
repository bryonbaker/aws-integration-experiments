import test_module as fm
import time

def main():
    print("Running  test")
    pi = 3.141592654

    print("Calling print_val()")
    
    t = 5
    print(f"Going to sleep for {t} minutes")
    time.sleep(t*60)
    
    
    fm.print_val(pi)
    
    print("FINISHED")

if __name__ == "__main__":
    main()