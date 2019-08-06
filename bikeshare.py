import time
import pandas as pd
import numpy as np

# global variable for function load_data.
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# global variable for the index of the months list to get the corresponding month as integer
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - number of the month to filter by, or 7 in case of no month filter
        (str) day - name of the day of week to filter by, or \'all\' to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        print('Would you like to see data for Chicago, New York City, or Washington?')
        city = input()

        if city.lower() in ['chicago','new york city','washington']:
            print('The city you would like to see is ' + city.title() + '. If correct type \'yes\'!')
            answer = input().lower()

            if answer == 'yes':
                city = city.lower()
                break
        else:
            print('The city \"' + city + '\" you entered is not available.')

    # get user input for month (all, january, february, ... , june)
    while True:
        print('Which month would you like to explore - January, February, March, April, May, June, or \'all\'?')
        month = input()

        if month.lower() in MONTHS:

            if month.lower() == 'all':
                print('You would like to see all month available. If correct type \'yes\'!')
            else:
                print('The month you would like to see is ' + month.title() + '. If correct type \'yes\'!')

            answer = input().lower()

            if answer == 'yes':
                month = MONTHS.index(month.lower()) + 1
                break
        else:
            print('The month \"' + month + '\" you entered is not available.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    # ask the user for a weekday till he entered "yes".
    while True:
        print('Which weekday would you like to explore - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or \'all\'?')
        day = input()
        if day.lower() in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:

            if day.lower() == 'all':
                print('You would like to see all weekdays available. If correct type \'yes\'!')
            else:
                print('The day you would like to see is ' + day.title() + '. If correct type \'yes\'!')

            answer = input().lower()

            if answer == 'yes':
                day = day.lower()
                break
        else:
            print('The day \'' + day + '\' you entered is not available.')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - number of the month to filter by, or 7 in case of no month filter
        (str) day - name of the day of week to filter by, or \'all\' to apply no day filter

    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(city.replace(' ', '_') + '.csv')
    # convert Start Time to datetime values
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Start Month'] = df['Start Time'].dt.month
    df['Start Day'] = df['Start Time'].dt.weekday_name
    df['Start Hour'] = df['Start Time'].dt.hour

    # convert End Time to datetime values
    df['End Time'] = pd.to_datetime(df['End Time'])

    # if the user selected 'all' months, 'all' is set to 7
    if month != 7:
        df = df[df['Start Month'] == month]
    if day != 'all':
        df = df[df['Start Day'] == day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel.
        Args:
            (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
            (str) month - number of the month to filter by, or 7 in case of no month filter
            (str) day - name of the day of week to filter by, or \'all\' to apply no day filter

        Returns:
            df - Pandas DataFrame containing city data filtered by month and day
     """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print('What is the most common start month, weekday, and hour?')
    # display the most common month and the number of  occurrences
    if month == 7:
        peak_month = df['Start Month'].mode()[0]
        num_peak_month = df['Start Month'].value_counts()[peak_month]
        print('Most common Start Month: ' + MONTHS[peak_month-1].title() + ', Count: ' + str(num_peak_month) )
    else:
        print('Most common Start Month: ' + str(MONTHS[month-1]).title() + ' (user selection)')

    # display the most common weekday and the number of  occurrences
    if day == 'all':
        peak_weekday = df['Start Day'].mode()[0]
        num_peak_weekday = df['Start Day'].value_counts()[peak_weekday]
        print('Most common Start Day: ' + peak_weekday + ', Count: ' + str(num_peak_weekday))
    else:
        print('Most common Start Month: ' + day.title() + ' (user selection)')

    # display the most common start hour and the number of  occurrences
    peak_hour = df['Start Hour'].mode()[0]
    num_peak_hour = df['Start Hour'].value_counts()[peak_hour]
    print('Most common Start Hour: ' + str(peak_hour) + ', Count: ' + str(num_peak_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
        Args:
            (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station and the number of  occurrences
    popular_start = df['Start Station'].mode()[0]
    num_popular_start = df['Start Station'].value_counts()[popular_start]

    # display most commonly used end station and the number of  occurrences
    popular_end = df['End Station'].mode()[0]
    num_popular_end = df['End Station'].value_counts()[popular_end]

    # display most frequent combination of start station and end station trip and the number of  occurrences
    # https://stackoverflow.com/questions/19560044/how-to-concatenate-element-wise-two-lists-in-python
    df['Trip'] = ['From {} to {}'.format(s,e) for s, e in zip(df['Start Station'], df['End Station'])]
    popular_trip = df['Trip'].mode()[0]
    num_popular_trip = df['Trip'].value_counts()[popular_trip]

    # display results of computation
    print('What are the most popular stations?')
    print('Start Station: {}, Count: {}\nEnd Station: {}, Count: {}\n'.format(popular_start, num_popular_start, popular_end, num_popular_end))
    print('What is the most popular combination of Start and End Station?')
    print('Trip : {}, Count: {}'.format(popular_trip, num_popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
       Args:
            (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time in minutes
    total_time = df['Trip Duration'].sum()/60

    # display mean travel time in minutes
    avg_time = (df['Trip Duration'].sum()/len(df['Trip Duration']))/60

    print('What is the total and average travel time?')
    print('Total travel time: {} minutes'.format(total_time))
    print('Average travel time: {} minutes\n'.format(round(avg_time,2)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users.
        Args:
            (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
            (str) city - name of the city to analyze
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('What is the frequency of user types?')
    print('Number of Subscribers: {}\nNumber of Customers: {}\nNumber of Dependent: {}\n'.format(user_types.get('Subscriber'), user_types.get('Customer'), user_types.get('Dependent')))

    # Display counts of gender
    # Display earliest, most recent, and most common year of birth
    print('What is the frequency of gender and birth year?')
    if city != 'washington':

        gender = df['Gender'].value_counts()
        nan_gender = df['Gender'].isnull().sum()
        print('Number of Females: {}\nNumber of Males: {}\nNumber of missing entries (NaN): {}\n'.format(gender.get('Female'), gender.get('Male'), nan_gender))

        min_ybirth = int(df['Birth Year'].min())
        max_ybirth = int(df['Birth Year'].max())
        mode_ybirth =  int(df['Birth Year'].mode()[0])
        print('Earliest Birth Year: {}\nLatest Birth Year: {}\nMost common Birth Year: {}'.format(min_ybirth, max_ybirth, mode_ybirth))
    else:
        print('For Washington is no Gender and Birth Year data available!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df, city, month):
    """Asks the user if he wants to explore the raw bikeshare data.
       Displays 5 rows of raw bikeshare data at a time,
       then ask the user if they would like to see 5 more rows of the data.
       The script runs through the raw data until the user enters 'no'.
       Args:
          (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
          (str) city - name of the city to analyze
     """

    colnames = [0,1,2,3,4,5,6,7,8]
    if city == 'washington':
        colnames = [0,1,2,3,4,5,6]

    print('\nWould you like to explore raw bikeshare data? Enter \'yes\' or \'no\'.')
    raw = input()

    for index in range(5,len(df),5):
        if raw == 'yes':
            print(df.iloc[index-5:index, colnames].to_string())
        else:
            break

        print('\nWould you like to explore more raw bikeshare data? Enter \'yes\' or \'no\'.')
        raw = input()

    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        raw_data(df, city, month)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
