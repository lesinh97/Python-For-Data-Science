import pandas as pd

# Data paths
file_paths = {
    "chicago": "C:\\Users\\ASUS\\Downloads\\all-project-files\\chicago.csv",
    "new_york_city": "C:\\Users\\ASUS\\Downloads\\all-project-files\\new_york_city.csv",
    "washington": "C:\\Users\\ASUS\\Downloads\\all-project-files\\washington.csv"
}


def load_data(city):
    """Load data from CSV file."""
    if city not in file_paths:
        raise ValueError("Invalid city name")
    return pd.read_csv(file_paths[city])


def common_times(df):
    """Calculate the most common month, day of week, and hour."""
    df['Start Time'] = pd.to_datetime(df['Start Time'], dayfirst=True)
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()
    df['Hour of Day'] = df['Start Time'].dt.hour

    return (
        df['Month'].mode()[0],
        df['Day of Week'].mode()[0],
        df['Hour of Day'].mode()[0]
    )


def popular_stations_and_trip(df):
    """Find the most common start station, end station, and trip."""
    common_start_station = df['Start Station'].mode()[0]
    common_end_station = df['End Station'].mode()[0]
    df['Trip'] = df['Start Station'] + " to " + df['End Station']
    common_trip = df['Trip'].mode()[0]

    return common_start_station, common_end_station, common_trip


def trip_duration(df):
    """Calculate total and average trip duration."""
    return df['Trip Duration'].sum(), df['Trip Duration'].mean()


def user_info(df, city):
    """Gather user info, including user type counts, and optionally gender and birth year stats."""
    user_types_count = df['User Type'].value_counts()
    user_types_count.name = "User Type"

    gender_count = None
    earliest_birth_year = None
    most_recent_birth_year = None
    most_common_birth_year = None

    if city in ['chicago', 'new_york_city']:
        gender_count = df['Gender'].value_counts()
        gender_count.name = "Gender"
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])

    return user_types_count, gender_count, earliest_birth_year, most_recent_birth_year, most_common_birth_year


def display_results(city, data):
    """Format and print results."""
    formatted_city = city.replace('_', ' ').title()
    print(f"City: {formatted_city}")
    for key, value in data.items():
        if value is not None:
            print(f"{key}: {value}")
    print("-" * 10)


# Main processing loop
for city in file_paths.keys():
    try:
        df = load_data(city)
        common_times_data = common_times(df)
        stations_and_trip_data = popular_stations_and_trip(df)
        trip_duration_data = trip_duration(df)
        user_info_data = user_info(df, city)

        display_results(city, {
            "Most Common Month": common_times_data[0],
            "Most Common Day of Week": common_times_data[1],
            "Most Common Hour of Day": common_times_data[2],
            "Most Common Start Station": stations_and_trip_data[0],
            "Most Common End Station": stations_and_trip_data[1],
            "Most Common Trip": stations_and_trip_data[2],
            "Total Travel Time": f"{trip_duration_data[0]} seconds",
            "Average Travel Time": f"{trip_duration_data[1]} seconds",
            "User Type Counts": user_info_data[0],
            "Gender Counts": user_info_data[1],
            "Earliest Birth Year": user_info_data[2],
            "Most Recent Birth Year": user_info_data[3],
            "Most Common Birth Year": user_info_data[4]
        })
    except ValueError as e:
        print(e)
