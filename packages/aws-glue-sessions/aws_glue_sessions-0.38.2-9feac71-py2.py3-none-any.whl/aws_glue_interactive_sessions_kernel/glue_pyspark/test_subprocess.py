

if __name__ == "__main__":
    import sys
    import subprocess
    print("Hello world")
    arg1= sys.argv[1]
    arg2 = sys.argv[2]
    subprocess.run(['python3', 'script1.py', arg1, arg2])


