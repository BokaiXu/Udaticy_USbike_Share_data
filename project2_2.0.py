import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities=['chicago', 'new york city', 'washington']
months=['January','February', 'March','April', 'May','June','All']
days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','All']

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
    while True:
        city = input('Which city do you want to see? chicago, new york city or washington?').lower()
        if city not in cities:
            print('Invalid input.\nPlease type in name without capital.')
            print('-'*40)
        else:
            break
    print('-'*40)
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Which month do you want to see?\nPlease type in January, February, March, April, May, June or All.').title()
        if month not in months:
            print('Invalid input. Please try again.')
            print('-'*40)
        else:
            break
    print('-'*40)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Which day do you want to see?\nPlease type in Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All.').title()
        if day not in days:
            print('Invalid input. Please try again.')
            print('-'*40)
        else:
            break
    print('-'*40)

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
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    # filter by month
    if month != 'All':
        month_num = months.index(month)+1
        df = df[df['month'] == month_num]
    # filter by day_of_week
    if day != 'All':
        day_num = days.index(day)
        df = df[df['day_of_week'] == day_num]
    return df

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    month_common = df['month'].mode()[0]
    print('most common month: {}'.format(months[month_common-1]))
    # display the most common day of week
    day_common = df['day_of_week'].mode()[0]
    print('most common day in a week: {}'.format(days[day_common]))
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    hour_common = df['hour'].mode()[0]
    print('most common start hour: {}:00'.format(hour_common))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    print('Most commonly used start station: {}'.format(df['Start Station'].mode()[0]))
    # display most commonly used end station
    print('Most commonly used end station: {}'.format(df['End Station'].mode()[0]))
    # display most frequent combination of start station and end station trip
    df['combine'] = df['Start Station'] + ' to ' + df['End Station']
    print('Most commonly combined start and end station: {}.'.format(df['combine'].mode()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    total = round(df['Trip Duration'].sum(),1)
    print('Total travel time: {} s'.format(total))
    # display mean travel time
    avg = round(df['Trip Duration'].mean(),1)
    print('Mean travel time: {} s'.format(avg))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """
    Displays statistics on bikeshare users.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    print(df['User Type'].value_counts())
    print('-'*40)
    # Display counts of gender
    if 'Gender' in df:
        print(df['Gender'].value_counts())
    else:
        print('Gender is info not available.')
    print('-'*40)
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('Earliest year of birth: {}'.format(int(df['Birth Year'].min())))
        print('Most recent year of birth: {}'.format(int(df['Birth Year'].max())))
        print('Most common year of birth: {}'.format(int(df['Birth Year'].mode()[0])))
    else:
        print('Birth Year info is not available.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """
    Ask users whether they want to see the raw data.
    Show every 5 rows of raw data and ask again.
    """
    i = 0
    # Convert the user input to lower case using lower() function
    raw =input('Do you want to see the raw data? Yes/No').lower()
    pd.set_option('display.max_columns', 200)
    while True:
        if raw == 'no':
            break
        elif raw == 'yes':
            # Appropriately subset/slice your dataframe to display next five rows
            print(df[i:i+5])
            raw = input('Do you want to see the raw data? Yes/No').lower()
            i += 5
        else:
            print('Invalid input. Please try again.')
            print('-'*40)
            raw = input('Do you want to see the raw data? Yes/No').lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() == 'no':
                print('-'*40)
                print('Thank you for using this system.\nHave a nice day.')
                break
            elif restart.lower() == 'yes':
                print('-'*40)
                return main()
            else:
                print('Invalid input. Please try again.')
        break
        print('-'*40)

if __name__ == "__main__":
	main()
