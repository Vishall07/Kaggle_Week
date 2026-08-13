# Kaggle Week - Painting Optimization Challenge

A Kaggle Week competition project focused on optimizing the arrangement of paintings to maximize tag overlap scoring.

## Project Overview

This project tackles a painting arrangement optimization problem where:
- Each painting is classified as either a **Landscape (L)** or **Portrait (P)**
- Each painting has associated **tags** describing its content
- **Portraits are merged in pairs** to combine their tags
- The goal is to **reorder paintings to maximize tag overlap** between consecutive paintings

### Scoring Function

The score is calculated based on the intersection and differences of tag sets between consecutive paintings:

```
score = Σ min(|A ∩ B|, |A - B|, |B - A|)
```

For each consecutive pair of paintings, we calculate:
- Intersection of their tag sets
- Difference A - B
- Difference B - A
- Take the minimum of these three values

This encourages paintings with significant tag overlap to be placed adjacent to each other.

## Project Structure

```
Kaggle_Week/
├── Data/                          # Input data files
│   ├── 0_example.txt             # Example dataset
│   ├── 1_binary_landscapes.txt   # Test dataset 1
│   ├── 10_computable_moments.txt # Test dataset 2
│   ├── 11_randomizing_paintings.txt # Test dataset 3
│   └── 110_oily_portraits.txt    # Test dataset 4
├── output/                        # Output solution files
│   ├── 0_example.txt
│   ├── 1_binary_landscapes.txt
│   ├── 10_computable_moments.txt
│   ├── 11_randomizing_paintings.txt
│   └── 110_oily_portraits.txt
├── notebooks/                     # Jupyter notebooks for experimentation
│   ├── 0_example.ipynb
│   ├── 1_binary_landscapes.ipynb
│   ├── 10_computable_moments.ipynb
│   ├── 11_randomizing_paintings.ipynb
│   ├── clean_one.ipynb
│   └── scoring_function.ipynb
├── python code/                   # Main implementation
│   ├── main_script.py            # Core optimization algorithm
│   └── test_score.py             # Scoring verification script
├── version_1/                     # Previous version
├── Version_2/                     # Alternative version
├── KCW2025.pdf                   # Problem specification
├── Kaggle Week Groups 2025a.xlsx # Team/group information
└── README.md                      # This file
```

## Input Data Format

Each input file follows this format:

```
<number_of_paintings>
<type> <num_tags> <tag1> <tag2> ... <tagN>
...
```

**Example (0_example.txt):**
```
4
L 3 animals fear war
P 2 smile woman
P 2 woman pearl
L 3 fear raft survivors
```

- **L**: Landscape painting
- **P**: Portrait painting
- The number following the type indicates the count of tags

## Output Data Format

The output file contains the reordered painting indices:

```
<number_of_items>
<index1> [<index2>]
...
```

For portrait pairs, both indices are listed on the same line. For landscape paintings, only one index is listed.

**Example output:**
```
3
1 2
0
3
```

## Algorithms & Approach

### Main Algorithm: Greedy Reordering with Chunking

The solution uses a **chunked greedy algorithm** to handle large datasets efficiently:

1. **Data Preprocessing**:
   - Parse input paintings and their tags
   - Merge portrait pairs (P type) to combine their tags
   - Keep landscape paintings (L type) separate

2. **Greedy Reordering** (applied per chunk):
   - Start with the painting that has maximum tag overlap with others
   - Iteratively select the next unpicked painting that maximizes tag overlap with the current painting
   - Time complexity: O(n²) per chunk

3. **Chunking Strategy**:
   - Process dataset in chunks of 1,000 paintings
   - Apply greedy reordering to each chunk independently
   - Concatenate results

This approach balances solution quality with computational efficiency for large datasets.

## Files Description

### Core Python Scripts

- **main_script.py**: 
  - Reads input data from text files
  - Implements the greedy reordering algorithm
  - Handles portrait merging
  - Generates output solutions
  - Main function processes dataset by index (0-4)

- **test_score.py**:
  - Calculates the score for generated solutions
  - Validates output against input data
  - Verifies tag overlap calculations
  - Runs scoring for all datasets

### Jupyter Notebooks

- **0_example.ipynb** through **110_oily_portraits.ipynb**: Experimentation and analysis notebooks for each dataset
- **scoring_function.ipynb**: Deep dive into scoring function implementation
- **clean_one.ipynb**: Cleaned-up analysis notebook

## How to Run

### Prerequisites

```bash
pip install pandas
```

### Generate Solutions

Run the main script to generate solutions for all datasets:

```bash
python "python code/main_script.py"
```

To process a specific dataset (0-4):
- Modify the `main(0)` call at the bottom to `main(n)` where n is the dataset index

### Calculate Scores

Verify the solutions by calculating scores:

```bash
python "python code/test_score.py"
```

This will output the score for each generated solution file.

## Algorithm Details

### Greedy Reordering Algorithm

```python
def greedy_reorder(df):
    # Find starting point: painting with max total tag overlap
    start = max(df.index, 
                key=lambda i: sum(len(df.loc[i, 'Tags'] & df.loc[j, 'Tags']) 
                                 for j in df.index if i != j))
    
    # Build order by always picking the next best match
    current = start
    for remaining paintings:
        next_index = max(remaining, 
                        key=lambda i: len(df.loc[current, 'Tags'] & df.loc[i, 'Tags']))
        current = next_index
```

### Portrait Merging

Portraits (type 'P') are merged in pairs to combine their tags:
- Pair 1: P[0] + P[1]
- Pair 2: P[2] + P[3]
- And so on...
- The combined tag set is the union of both paintings' tags

This reduces the problem size and can improve scoring by combining related artworks.

## Performance Notes

- Processing time scales with dataset size (tracked in main_script.py)
- Chunking strategy helps manage memory and computation for large datasets
- Current implementation optimizes for reasonable runtime vs. solution quality

## Team Information

See `Kaggle Week Groups 2025a.xlsx` for team/group composition.

## Challenge Specification

See `KCW2025.pdf` for the official problem statement and competition details.

## Future Improvements

Potential optimizations:
- Implement simulated annealing or other metaheuristics
- Use dynamic programming for optimal substructure solutions
- Experiment with different chunk sizes
- Implement inter-chunk optimization
- Apply machine learning techniques for tag similarity learning
