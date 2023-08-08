import subprocess

def validate(path):
    p = subprocess.Popen(["terraform", "validate"], cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = p.communicate()
    Errors = str(errors)
    if Errors == "b''":
        print("Terraform validation is successful.")
    else:
        Errors = errors.decode()
        print("Terraform validation failed.")
        print(Errors)