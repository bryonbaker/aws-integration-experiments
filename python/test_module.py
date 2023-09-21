def print_val( x ):
    print(f"The value of x is {x}")

    y = x / 0   # Error here

    return

def main():
    print("Running the failing_module.py test")
    pi = 3.141592654
    print_val(pi)

if __name__ == "__main__":
    main()