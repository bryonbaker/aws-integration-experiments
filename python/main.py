import test_module as fm

def main():
    print("Running  test")
    pi = 3.141592654

    print("Calling print_val()")
    
    fm.print_val(pi)
    
    print("FINISHED")

if __name__ == "__main__":
    main()