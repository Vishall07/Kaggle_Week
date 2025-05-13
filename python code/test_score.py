import pandas as pd


def get_input_data(path = "../Data/0_example.txt"):
    with open(path, 'r') as file:
        lines = file.read().strip().split('\n')
    lines = lines[1:]
    return lines

def get_output_data(path = "../output/0_example.txt"):
    with open(path, 'r') as file:
        lines = file.read().strip().split('\n')
    lines = lines[1:]
    return lines

def input_lines_to_df(lines):
    index = 0
    parsed = []
    for line in lines:
        parts = line.strip().split()
        painting_type = parts[0]
        num_tags = int(parts[1])
        tags = set(parts[2:]) 
        parsed.append({
            "index" : index,
            "Type": painting_type,
            "Num_Tags": num_tags,
            "Tags": tags
        })
        index += 1
    df = pd.DataFrame(parsed)
    return df

def output_lines_to_df(lines):
    parsed = []
    for line in lines:
        parts = line.strip().split()
        if(len(parts)==1):
            parsed.append({"one" : parts[0], "two" : None})
        else:
            parsed.append({"one" : parts[0], "two" : parts[1]})
    df = pd.DataFrame(parsed)
    return df

# scoring_function()
input_paths = [
    "./Kaggle_Week/Data/0_example.txt",
    "./Kaggle_Week/Data/1_binary_landscapes.txt",
    "./Kaggle_Week/Data/10_computable_moments.txt",
    "./Kaggle_Week/Data/11_randomizing_paintings.txt",
    "./Kaggle_Week/Data/110_oily_portraits.txt"
    ]

output_paths = [
        "./Kaggle_Week/output/0_example.txt",
        "./Kaggle_Week/output/1_binary_landscapes.txt",
        "./Kaggle_Week/output/10_computable_moments.txt",
        "./Kaggle_Week/output/11_randomizing_paintings.txt",
        "./Kaggle_Week/output/110_oily_portraits.txt"
    ]

def get_score(input_path, output_path):
    input_data = get_input_data(input_path)
    output_data = get_output_data(output_path)
    input_df = input_lines_to_df(input_data)
    output_df = output_lines_to_df(output_data)

    res = []
    for i in range(len(output_df)):
        first_paint = int(output_df.iloc[i]['one'])
        set_one = input_df.iloc[first_paint]['Tags']
        if(output_df.iloc[i]['two'] != None):
            second_paint = int(output_df.iloc[i]['two'])
            set_two = input_df.iloc[second_paint]['Tags']
            set_one = set_one.union(set_two)
        res.append({"tags" : set_one.copy()})
    df = pd.DataFrame(res)

    score = 0
    for i in range(len(df)-1):
        cur_set = df.iloc[i]['tags']
        next_set = df.iloc[i+1]['tags']
        score += min(len(cur_set & next_set), len(cur_set - next_set), len(next_set - cur_set))
    print(score)

if __name__=="__main__":
    for i in range(len(input_paths)):
        get_score(input_paths[i], output_paths[i])