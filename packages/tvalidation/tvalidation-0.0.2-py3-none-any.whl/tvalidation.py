import subprocess
import json

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

def validate_output_in_json(path):
    command = ["terraform", "validate", "-json"]
    result = subprocess.run(command, cwd=path, capture_output=True, text=True)
    output_json = json.loads(result.stdout)
    print(json.dumps(output_json, indent=4))
