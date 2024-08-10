import pandas as pd

# Data path
file_paths = {
    "chicago": "C:\\Users\\ASUS\\Downloads\\all-project-files\\chicago.csv",
    "new_york_city": "C:\\Users\\ASUS\\Downloads\\all-project-files\\new_york_city.csv",
    "washington": "C:\\Users\\ASUS\\Downloads\\all-project-files\\washington.csv"
}


def load_data(city):
    if city not in file_paths:
        raise ValueError("Invalid city name")
    return pd.read_csv(file_paths[city])


def common_times(city):
    # Load data
    df = load_data(city)

    # Convert 'Start Time' to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'], dayfirst=True)

    # Extract month, day of week, and hour of day from 'Start Time'
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()
    df['Hour of day'] = df['Start Time'].dt.hour

    # Find the most common month, day of week, and hour
    common_month = df['Month'].mode()[0]
    common_day_of_week = df['Day of Week'].mode()[0]
    common_hour = df['Hour of day'].mode()[0]

    return common_month, common_day_of_week, common_hour


# Get results for cities
results = {}
for city in file_paths.keys():
    try:
        results[city] = common_times(city)
    except ValueError as e:
        print(e)

# Show results
for city, (month, day, hour) in results.items():
    formatted_city = city.replace('_', ' ').title()
    print(f"City: {formatted_city}")
    print(f"Most Common Month: {month}")
    print(f"Most Common Day of Week: {day}")
    print(f"Most Common Hour of Day: {hour}")
    print("-" * 10)


def popular_stations_and_trip(df):
    common_start_station = df['Start Station'].mode()[0]
    common_end_station = df['End Station'].mode()[0]

    # Create a new column for the combination of start and end stations
    df['Trip'] = df['Start Station'] + " to " + df['End Station']

    # Find the most common trip from start to end
    common_trip = df['Trip'].mode()[0]

    return common_start_station, common_end_station, common_trip


# Get results for cities
results = {}
for city, file_path in file_paths.items():
    df = pd.read_csv(file_path)
    results[city] = popular_stations_and_trip(df)

# Show results
for city, (start_station, end_station, trip) in results.items():
    formatted_city = city.replace('_', ' ').title()
    print(f"City: {formatted_city}")
    print(f"Most Common Start Station: {start_station}")
    print(f"Most Common End Station: {end_station}")
    print(f"Most Common Trip: {trip}")
    print("-" * 10)


def trip_duration(df):
    # Calculate total travel time and average travel time and average travel time
    total_travel_time = df['Trip Duration'].sum()
    average_travel_time = df['Trip Duration'].mean()

    return total_travel_time, average_travel_time


# Get results for cities
results = {}
for city, file_path in file_paths.items():
    df = pd.read_csv(file_path)
    results[city] = trip_duration_stats(df)

# Show results
for city, (total_time, avg_time) in results.items():
    formatted_city = city.replace('_', ' ').title()
    print(f"City: {formatted_city}")
    print(f"Total Travel Time: {total_time} seconds")
    print(f"Average Travel Time: {avg_time} seconds")
    print("-" * 10)


def user_info(df, city):
    # Count of each user type and set name to "User Type"
    user_types_count = df['User Type'].value_counts()
    user_types_count.name = "User Type"

    # Initialize gender counts and birth year statistics
    gender_count = None
    earliest_birth_year = None
    most_recent_birth_year = None
    most_common_birth_year = None

    # Gender count and birth year stats only for NYC and Chicago
    if city in ['chicago', 'new_york_city']:
        gender_count = df['Gender'].value_counts()
        gender_count.name = "Gender"

        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])

    return user_types_count, gender_count, earliest_birth_year, most_recent_birth_year, most_common_birth_year


# Get results for cities
results = {}
for city, file_path in file_paths.items():
    df = pd.read_csv(file_path)
    results[city] = user_info(df, city)

# Show results
for city, (user_types, gender_count, earliest, recent, common) in results.items():
    formatted_city = city.replace('_', ' ').title()
    print(f"City: {formatted_city}")
    print("User Type Counts:")
    print(user_types)

    if gender_count is not None:
        print("\nGender Counts:")
        print(gender_count)

    if earliest is not None:
        print(f"\nEarliest Birth Year: {earliest}")
        print(f"Most Recent Birth Year: {recent}")
        print(f"Most Common Birth Year: {common}")

    print("-" * 10)
