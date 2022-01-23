import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
CITIES = list(CITY_DATA.keys())
MONTHS_LIST = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
DAYS_LIST = ['monday','tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday','all']
#print(CITIES)

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while city.lower() not in CITIES: #check that an actual city (or all) is entered - manages case differences
        city=input('Please enter one of the 3 defined cities (chicago, new york city, washington): ')

    city = city.title()
    print("You have chosen {}".format(city))
    city = city.lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = ''
    while month.lower() not in MONTHS_LIST: #check that an actual month (or all) is entered - manages case differences
        month=input("Enter a month to filter the data on (e.g. january, february, ... , june) or type all: ")

    month = month.title()
    print("You have chosen {}".format(month))
    month = month.lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day.lower() not in DAYS_LIST: #check that an actual day (or all) is entered - manages case differences
        day = input("Enter a day to filter the data on (e.g. monday, tuesday, ... sunday) or type all: ")

    day = day.title()
    print("You have chosen {}".format(day))
    day = day.lower()

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
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    df['month_name'] = df['Start Time'].dt.month_name()
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        day = day.title()
        df = df[df['day_of_week']==day] # this is the tricky filter stuff

    return df

def show_data(df): #give the option to see the data and step through it at 5 rows at a time
    continue_list = ['y','yes']
    row_count = df.shape[0]
    print('Your filter has returned {} rows of data'.format(row_count))
    see_data = input('Do you want to see the first 5 rows of the raw data? Type y to see it or anything else to go straight to the analysis: ')
    if see_data in continue_list:
        print(df.head())
        row_count=5
        while see_data in continue_list:
            see_data=input('Do you want see 5 more rows of data? Type y to see it or anything else to not see any more data: ')
            print(df[row_count:row_count+5])
            row_count = row_count + 5

    else:
        print('We will go straight to the statistics then\n\n')


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month_name'].mode()[0]
    print('The most common month of travel is: {}'.format(common_month))

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common day of travel is: {}'.format(common_day))

    # TO DO: display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('The most common hour of travel is: {} \n'.format(common_hour))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('The most common Start Station of travel is: {}'.format(common_start))

    # TO DO: display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('The most common End Station of travel is: {}'.format(common_end))

    # TO DO: display most frequent combination of start station and end station trip
    common_trip = df['trip'].mode()[0]
    print('The most common trip is: {}'.format(common_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    tot_travel_time = round(df['Trip Duration'].sum()/60/60/24,2) #convert seconds to days
    print('The total trip time is {} days'.format(tot_travel_time))

    # TO DO: display mean travel time
    mean_travel_time = round(df['Trip Duration'].mean()/60,2) #convert seconds to minutes
    print('The mean trip time is {} minutes'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    # TO DO: Display counts of user types
    print('The User Type breakdown is:\n')

    user_counts = df['User Type'].value_counts()
    print(user_counts)


    # TO DO: Display counts of gender
    #is_gender = df['Gender'].sum()
    #if is_gender != 0:
    try:
        print('\n\nThe Gender breakdown is:\n')
        gender_counts = df['Gender'].value_counts()
        print(gender_counts)
    #print(is_gender)

    #else:
    except:
        print("There is no Gender data available.\n")


    # TO DO: Display earliest, most recent, and most common year of birth
    #if df['Birth Year'].count() > 0:
    try: #handle exceptions thrown due to no data
        print('\n\nSome data on the users birth year is:\n')
        earliest_birth_year = int(df['Birth Year'].min())
        recent_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode()[0])
        print('The earliest birth year is: {}'.format(earliest_birth_year))
        print('The most recent birth year is: {}'.format(recent_birth_year))
        print('The most common birth year is: {}'.format(common_birth_year))


    #else:
    except:
        print("There is no birth year data available.\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        show_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
