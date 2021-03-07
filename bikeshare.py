import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities= {'c': 'chicago', 'n': 'new york city', 'w': 'washington'}
months= ['january', 'february', 'march', 'april','may', 'june', 'all']
days= ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

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
        city_selection= input("Please, type the letter of your city\n (C) for Chicago\n (N) for New York\n (W) for Washington\n").lower()
        try:
            if city_selection in cities:
                city= cities[city_selection]
                break
        except KeyboardInterrupt:
            print("No value, try again")
        else:
            print("Invalid selection, try again")

    # get user input for month (all, january, february, ... , june)
    while True:
        month_selection= input("Which month you interested in: January, February, March, April, May, June, or All?\n").lower()
        try:
            if month_selection in months:
                month= month_selection
                break
        except KeyboardInterrupt:
            print("No value, try again")
        else:
            print("Invalid selection, try again")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_selection= input("Which day: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or All?\n").lower()
        try:
            if day_selection in days:
                day= day_selection
                break
        except KeyboardInterrupt:
            print("No value, try again")
        else:
            print("Invalid selection, try again")


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
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour']= df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        month= months.index(month) +1
        df = df[df['month'] == month]
    else:
        df = df


   # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    else:
        df= df
    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month is {}".format(df['month'].mode()[0]))

    # display the most common day of week
    print("The most common day is {}".format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    print("The most common hour is {}".format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most common Start Station is {}".format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print("The most common End Station is {}".format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    df['combination']= df['Start Station'] + ' : ' + df['End Station']
    print("The most common combination of Start and End Station is {}".format(df['combination'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The Total Travel Time is {}".format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The Mean Travel Time is {}".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())

        # Display counts of gender
    if city == 'washington':
        print("Gender is not available in Washington data")
    else:
        print(df['Gender'].value_counts())


    # Display earliest, most recent, and most common year of birth

    if city == 'washington':
        print("Birth Year is not available in Washington data")

    else:
        earliest_year= int(df['Birth Year'].min())
        recent_year= int(df['Birth Year'].max())
        common_year= int(df['Birth Year'].mode()[0])
        print("\nThe earliest year of birth is {}\nThe recent year of birth is {}\nThe common year of birth is {}\n".format(earliest_year, recent_year, common_year))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(city):
    raw = input('\nWould you like to see some raw data? Enter yes or no.\n').lower()

    while raw == 'yes':
        try:
            for chunk in pd.read_csv(CITY_DATA[city], chunksize= 5):
                print(chunk)
                raw = input('\nWould you like to see more raw data? Enter yes or no.\n').lower()
                if raw != 'yes':
                    break
            break
                    

        except KeyboardInterrupt:
            print('Thank you')

        else:
            break

def main():
    while True:
        filtered_values= get_filters()
        city, month, day= filtered_values
        df= load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()




