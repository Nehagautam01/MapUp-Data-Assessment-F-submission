import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    df = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    df.values[[range(df.shape[0])]*2] = 0

    return df


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    df['car_type'] = pd.cut(df['car'], bins=[-1, 15, 25, 100], labels=['low', 'medium', 'high'])
    type_counts = df['car_type'].value_counts().to_dict()
    return dict(sorted(type_counts.items()))


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    mean_bus_value = df['bus'].mean()
    twice_mean_bus_value = mean_bus_value * 2
    bus_indexes = df[df['bus'] > twice_mean_bus_value].index.tolist()
    return sorted(bus_indexes)


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    # the average truck value per route
    avg_truck_by_route = df.groupby('route')['truck'].mean()

    # Filter routes where average truck value is greater than 7
    filtered_routes = avg_truck_by_route[avg_truck_by_route > 7].index.tolist()

    # Sorted the filtered routes and return them
    return sorted(filtered_routes)
    

def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

        Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    modified_df = matrix.copy()

    modified_df = modified_df.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    modified_df = modified_df.round(1)

    return modified_df


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    required_start_time = pd.Timestamp("00:00:00")
    required_end_time = pd.Timestamp("23:59:59")

    df["start_time"] = pd.to_datetime(df[["startDay", "startTime"]])
    df["end_time"] = pd.to_datetime(df[["endDay", "endTime"]])

    df["duration"] = df["end_time"] - df["start_time"]
    df["weekly_coverage"] = (df["endDay"] - df["startDay"] + 1).abs()

    incorrect_timestamps = (
        (df["duration"] < pd.Timedelta(days=1))
        | (df["duration"] != pd.Timedelta(hours=23, minutes=59, seconds=59))
        | (df["weekly_coverage"] != 7)
    )

    incorrect_timestamps |= (
        (df["start_time"].isna()) | (df["end_time"].isna())
    )

    incorrect_timestamps = pd.Series(
        incorrect_timestamps, index=df[["id", "id_2"]].set_index(["id", "id_2"]), name="incorrect_timestamps"
    )

    return incorrect_timestamps
