import openai
class result:
    def __init__(self):
        self.result = ""
        self.variables = {}
    def assignResult(self,result):
        self.result = result
    def assignVariables(self,variables):
        badlst = []
        if "VARIABLES" in variables:
            for key,value in variables["VARIABLES"].items():
                if "<" in str(value):
                    badlst.append(key)
        for item in badlst:
            del variables["VARIABLES"][item]
        self.variables = variables
    def display(self):
        print(f"\u001b[34mResult:\n\u001b[96m{self.result}")
        print("\u001b[34mVariables:\u001b[96m")
        if "VARIABLES" in self.variables:
            for key,value in self.variables["VARIABLES"].items():
                print(f"\u001b[36m[{key}]: \u001b[96m{value}")
            del self.variables["VARIABLES"]
        for key,value in self.variables.items():
            print(f"\u001b[36m[{key}]: \u001b[96m{value}")
    
def init(key):
    openai.api_key = key
def instruction(lines):
    string = " ".join(lines)
    return {"INSTRUCTION":string}
def format(lines):
    string = "\n".join(lines)
    return {"FORMAT":string}
def logic(lines):
    varDict = {}
    lines = "\n".join(lines)
    exec(lines,varDict)
    return {"VARIABLES":varDict}
def rules(lines):
    exceptions,manditory="",""
    for var in lines[1:]:
        start,var=var.replace("'","").split("=[")
        if "EXCLUDE" in start:
            exceptions = var.replace("]","").split(",")
        if "INCLUDE" in start:
            manditory = var.replace("]","").split(",")
    if exceptions != "" and manditory != "":
        return {"EXCEPTIONS":exceptions,"MANDITORY":manditory}
    elif exceptions != "":
        return {"EXCEPTIONS":exceptions}
    elif manditory != "":
        return {"MANDITORY":manditory}
def llm(lines):
    dict = {}
    for var in lines[1:]:
        start,var=var.replace("'","").split("[")
        if "TEMP" in start:
            dict["TEMP"]=var.replace("]","")
        elif "LLM" in start:
            dict["LLM"] = var.replace("]","")
    return dict
def compose(templateList):
    data,varStr = {},""
    temperature_ = 0.7
    for data_dict in templateList:
        for key, value in data_dict.items():
            data[key] = value
    try:
        instruction_ = data["INSTRUCTION"]
        format_ = data["FORMAT"]
        if "EXCEPTIONS" in data:
            exceptions_ = "\n".join(data["EXCEPTIONS"])
        else:
            exceptions_ = "No themes/items cannot be used for this task"
        if "TEMPERATURE" in data:
            temperature_ = data["TEMPERATURE"]
        if "MANDITORY" in data:
            manditory_ = "\n".join(data["MANDITORY"])
        else:
            manditory_ = "No themes/items are manditory for this task"
        if "VARIABLES" in data:
            num = 0
            for key,value in data["VARIABLES"].items():
                if num > 0 and "<" not in str(value):
                    varStr += f"[{key}] = {value}\n"
                num = num + 1
    except Exception as e: return f"ERROR: One or more required elements were not provided\nERROR MESSAGE: {e}",None
    messages_ = [{"role":"system","content":"You will be given instructions, a format to complete them in and themes/items to not include in your answer as well as some themes/items you have to include and variables to keep in mind in the format. Complete the instructions, filling in the format given."}, {"role": "user","content": f"INSTRUCTIONS: {instruction_}\nVARIABLES:\n{varStr}\nFORMAT: {format_}\nDO NOT USE: {exceptions_}\nUSE:\n{manditory_}"}]
    try:
        summary = openai.ChatCompletion.create(model=str(data["LLM"]),messages=messages_,temperature=float(temperature_),max_tokens=250,n=1,stop=None,timeout=20)
        for i in summary['choices']: result_=i['message']['content']
        return result_,data
    except Exception as e: return f"API Error: {e}",data
def run(inputStr):
    vars = []
    functionBlocks = inputStr.strip().split('}')[:-1]
    for block in functionBlocks:
        block = block.strip().lstrip('{').strip()
        parts = block.split('{')
        functionName = parts[0].strip()
        codeList = [line.strip() for line in parts[1].split('\n')]
        vars.append(eval(f"{functionName}({codeList})"))
    return vars
def func(funcname):
    def wrapper(*args, **kwargs):
        inputStr = funcname(*args, **kwargs)
        vars = run(inputStr)
        result_,variables_=compose(vars)
        Result = result()
        Result.assignResult(result_)
        Result.assignVariables(variables_)
        return Result
    return wrapper
def script(name):
    try:
        with open(f"scripts/{name}","r") as f:
            text = f.read()
            result_,variables_=compose(run(text))
            Result = result()
            Result.assignResult(result_)
            Result.assignVariables(variables_)
            return Result
    except:
        print("ERROR: Script not found! Is the specified script in the 'scripts' folder?")
        exit(404)