import pandas as pd
import time

def read_file(path = ''):
    with open(path, 'r') as file:
        lines = file.read().strip().split('\n')
    lines = lines[1:]
    return lines


def convert_lines_to_df(lines):
    parsed = []
    index = 0
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
    df = df.sort_values(by='Type', ascending=False)
    return df

def merge_potraits_in_one_frame(df):
    df_p = df[df['Type'] == 'P'].copy()
    df_l = df[df['Type'] == 'L'].copy()
    merged = []
    for i in range(0, len(df_p), 2):
        if i + 1 < len(df_p):
            idx1, idx2 = df_p.iloc[i]['index'], df_p.iloc[i+1]['index']
            tags1, tags2 = df_p.iloc[i]['Tags'], df_p.iloc[i+1]['Tags']
            tags3 = tags1.union(tags2)
            merged.append({
                "index": f"{idx1} {idx2}",
                "Type" : "P",
                "Tags": tags3,
                "Num_Tags" : len(tags3)
            })

    merged_df = pd.DataFrame(merged)
    combined_df = pd.concat([merged_df, df_l], ignore_index=True)
    combined_df = combined_df.sort_values(by='Num_Tags', ascending=False)  
    print(combined_df)
    return combined_df


def create_output_file(combined_df, path):
    output = combined_df['index']  
    len_output = len(output)

    with open(path, "w") as f:
        f.write(str(len_output) + "\n")
        for line in output.values:
            f.write(str(line)+'\n')


def calculate_frequency(items, n , output_chunk = 2):
    frequency = {}
    for item in items:
        frequency[item] = frequency.get(item, 0) + 1
    sorted_items = sorted(frequency.items(), key=lambda x: (abs(x[1] - n), -x[1]))
    closest_keys = [key for key, _ in sorted_items[:output_chunk]]
    return closest_keys

def get_candidate_indices(current_index, memo, df):
    set_data = df.iloc[current_index]["Tags"]
    res = []
    for tag in set_data:
        rows = memo[tag]
        res += rows
    n = len(set_data) // 2
    res = calculate_frequency(res, n)
    return res


def reorder_df_with_candidates(df, memo):
    df = df.copy().reset_index(drop=True)
    result = []
    unvisited = set(range(len(df)))
    current_index = 0
    unvisited.remove(current_index)
    result.append(df.loc[current_index])

    while unvisited:
        print(len(result))
        curr_tags = df.loc[current_index, 'Tags']
        candidates = set(get_candidate_indices(current_index, memo, df)) & unvisited
        if not candidates:
            candidates = unvisited

        min_cost = float('inf')
        next_index = None

        for i in candidates:
            next_tags = df.loc[i, 'Tags']
            common = curr_tags & next_tags
            uncommon1 = (curr_tags - next_tags) 
            uncommon2 = (next_tags - curr_tags)
            cost = max(len(common), len(uncommon1), len(uncommon2))

            if cost < min_cost:
                min_cost = cost
                next_index = i

        if next_index is not None:
            unvisited.remove(next_index)
            result.append(df.loc[next_index])
            current_index = next_index

    return pd.DataFrame(result).reset_index(drop=True)

def main(file_number = 0):
    start_time = time.time()
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


    lines = read_file(input_paths[file_number])
    df = convert_lines_to_df(lines)
    combined_df = merge_potraits_in_one_frame(df)

    memo = {}
    for index, row in combined_df.iterrows():
        tag_str = row['Tags'] 
        for tag in tag_str:
            if(tag in memo):
                memo[tag].append(index)
            else:
                memo[tag] = [index]
    
    combined_df = reorder_df_with_candidates(combined_df, memo)

    end_time = time.time()
    print(f"Processing took {end_time - start_time:.2f} seconds")
    create_output_file(combined_df, output_paths[file_number])


if __name__=="__main__":
    main(3)
    # for i in range(5):
    #     main(i)


