import pandas as pd
import cv2
import matplotlib.pyplot as plt
import argparse
import os


def create_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("annotation_path", type = str, help = "Path to annotation")
    parser.add_argument("width", type = int, help = "Max width")
    parser.add_argument("height", type = int, help = "Max height")
    args = parser.parse_args()
    return args

def create_df(annotation_path: str) -> pd.DataFrame:
    if os.path.isfile(annotation_path):
        df = pd.read_csv(annotation_path)
        return df
    else:
        raise Exception(f"File {annotation_path} not found.")

def add_image_shape(df):
    height, width, channels = [], [], []
    for path in df["relative path"]:
        if os.path.isfile(path):
            img = cv2.imread(path)
            height.append(img.shape[0])
            width.append(img.shape[1])
            channels.append(img.shape[2])
        else:
            raise Exception(f"File {path} not found.")
    df["height"] = height
    df["width"] = width
    df["channels"] = channels
    return df

def statistic(df):
    stats = df[["height", "width", "channels"]].describe()
    return stats

def filter_by_width_and_height(df: pd.DataFrame, max_w: int, max_h: int) -> pd.DataFrame:
    filtered_df = df[(df['width'] <= max_w) & (df['height'] <= max_h)]
    return filtered_df

def add_area(df):
    if 'width' in df.columns:
        df['area'] = df['width'] * df['height']
        return df
    else:
        raise Exception(f"Column 'width' and 'height' does not exist in DataFrame")

def filter_by_area(df):
    if 'area' in df.columns:
        df_sorted = df.sort_values(by='area')
        return df_sorted
    else:
        raise Exception(f"Column 'area' does not exist in DataFrame")

def create_histogram(df):
    plt.hist(df['area'], bins=df.shape[0], color='black')
    plt.title('image area distribution')
    plt.xlabel('area(px)')
    plt.ylabel('frequency')
    plt.show()

def main():
    try:
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        args = create_parse()
        df = create_df(args.annotation_path)
        print(df.head())
        add_image_shape(df)
        print(df, "\n")
        print(statistic(df))
        print(filter_by_width_and_height(df, args.width, args.height))
        print(filter_by_area(add_area(df)))
        create_histogram(df)
    except Exception as exc:
        print(exc)

if __name__ == '__main__':
    main()