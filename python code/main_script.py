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

# Greedy algorithm
def greedy_reorder(df):
    used = set()
    order = []
    
    # Start with the row with max total tag overlap with others
    start = max(df.index, key=lambda i: sum(len(df.loc[i, 'Tags'] & df.loc[j, 'Tags']) for j in df.index if i != j))
    current = start
    used.add(current)
    order.append(current)

    while len(used) < len(df):
        next_index = max(
            (i for i in df.index if i not in used),
            key=lambda i: len(df.loc[current, 'Tags'] & df.loc[i, 'Tags']),
            default=None
        )
        if next_index is None:
            break
        used.add(next_index)
        order.append(next_index)
        current = next_index
    
    return df.loc[order].reset_index(drop=True)



def main(file_number = 0):
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

    # # Run greedy reordering
    # combined_df = greedy_reorder(combined_df)
    # print(combined_df)

    chunk_size = 1000
    chunks = [combined_df[i:i+chunk_size] for i in range(0, len(combined_df), chunk_size)]
    start_time = time.time()
    processed_chunks = []

    for chunk in chunks:
        reordered_chunk = greedy_reorder(chunk)
        processed_chunks.append(reordered_chunk)

    final_df = pd.concat(processed_chunks, ignore_index=True)
    end_time = time.time()
    print(f"Processing took {end_time - start_time:.2f} seconds")
    create_output_file(final_df, output_paths[file_number])


if __name__=="__main__":
    main(0)


#1478