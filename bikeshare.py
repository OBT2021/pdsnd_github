import time
import pandas as pd
import numpy as np

LENGTH_LINE = 40

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

DAY_DATA = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    cities = ('chicago', 'new york city', 'washington')
    while True:
        city = input('Which city do you want to analyze: Chicago, New York City, Washington:\n')
        if city.lower() in cities:
            break
        else:
            print('Please type one of the following available city\n')

    # get user input for month (all, january, february, ... , june)

    while True:
        month = input('\nWhat month do I filter by: January, February, March, April, May, June, July, August, September, October, November, December or all if you do not it to be filtered by a particular month :\n')
        if month.lower() in MONTH_DATA:
            break
        else:
            print('Sorry, you missed something, Please enter a specific month or all\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        day = input('\nWhat day do I filter by: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or all if you do not want it filtered by a particular day :\n')
        if day.lower() in DAY_DATA:
            break
        else:
            print('Sorry, you missed something, Please enter a specific day or all\n')
    print('-'*LENGTH_LINE)
    return city, month, day




def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
# load data file into a dataframe
    try:
        df = pd.read_csv(CITY_DATA[city.lower()])
    except FileNotFoundError:
        print(f"Error: The file for {city} is not found. Please check the file path.")
        return pd.DataFrame()
    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()
 # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
# extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
# filter by month if applicable
    if month != 'all':
# use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1
        
# filter by month to create the new dataframe
    df = df[df['month'] == month]

# filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if 'month' in df.columns:
        common_month = df['month'].mode()[0]
        print('Most Common Month:', common_month)
    else:
        print("Month data is not available in the dataset.")

    # display the most common day of week
    if 'day_of_week' in df.columns:
        common_day = df['day_of_week'].mode()[0]
        print('Most Common Day of Week:', common_day)
    else:
        print("Day of week data is not available in the dataset.")

    # display the most common start hour
    if 'hour' in df.columns:
        common_start_hour = df['hour'].mode()[0]
        print('Most Common Hour:', common_start_hour)
    else:
        print("Hour data is not available in the dataset.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * LENGTH_LINE)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    commonly_used_start_station = df['Start Station'].mode()[0]
    print('Most Commonly Used Start Station:', commonly_used_start_station)

    # display most commonly used end station
    commonly_used_end_station = df['End Station'].mode()[0]
    print('Most Commonly Used End Station:', commonly_used_end_station)

    # display most frequent combination of start station and end station trip
    if not df.empty:
        most_frequent_combination = (df.groupby(['Start Station', 'End Station']).size().idxmax())
    else:
        print("No data available to calculate the most frequent combination.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * LENGTH_LINE)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f'The total travel time for filtered data is: {total_travel_time}')


    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f'The mean travel time for filtered data is: {mean_travel_time}')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*LENGTH_LINE)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f'The user types for filtered data is: {user_types}')

    # Display counts of gender
    if city.lower() in ['chicago', 'new york city']:
        gender = df['Gender'].value_counts()
        print(f'The count of gender for filtered data is: {gender}')


        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print(f'The earliest birth year for filtered data is: {earliest_birth_year}')
        print(f'The most recent birth year for filtered data is: {most_recent_birth_year}')
        print(f'The most common birth year for filtered data is: {most_common_birth_year}')
    else:
        print("\nGender and birth year data are not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*LENGTH_LINE)

def display_data(df):
    """Displays raw data on user request.
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    print(df.head())
    start_loc = 0
    while True:
        view_data = input('\nWould you like to continue? Enter yes or no.\n')
        if view_data.lower() != 'yes':
            break
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        while True:
            view_raw_data = input('\nWould you like to view first five row of raw data? Enter yes or no.\n')
            if view_raw_data.lower() != 'yes':
                break
            display_data(df)
            break


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
