import pandas as pd
import sys
import argparse

def main(params):
    if params.input:
        in_fname = params.input 
        out_fname = params.output
        try:
            df = pd.read_parquet(f"{in_fname}")
            df.to_csv(f"{out_fname}", index=False)
            print("Conversion complete.")
            sys.exit(0)
        except Exception as e:  # Catch specific exceptions if possible
            print(f"Error: {e}")
            sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Use to convert parquet to CSV")
    parser.add_argument('-i', '--input', help='Path to the Parquet file')
    parser.add_argument('-o', '--output', help='Output CSV file name')
    
    args = parser.parse_args()
    print(f'Args: {args}')

    main(args)
