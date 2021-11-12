import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')    

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
  
    df_race = df.loc[:, ['race']]
    race_count = df_race['race'].value_counts()
    # What is the average age of men?

    average_age_men = round((df[df.sex == 'Male'].age.mean()), 1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round(((df[df.education == 'Bachelors'].education.count()/ df['education'].count()) * 100), 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?
    degrees = ['Bachelors', 'Masters', 'Doctorate']
    no_degrees = [i for i in df['education'] if i not in degrees]
    
    df_education = df.loc[:, ['education', 'salary']]
    df1_education =  df_education[(df_education['education'].isin(degrees))]
    df2_education = df1_education.groupby(['education']).salary.agg(['count'])

    df1_education_rich = df_education[(df_education['education'].isin(degrees)) & (df_education['salary'] == '>50K')] 
    df2_education_rich = df1_education_rich.groupby(['education']).salary.agg(['count'])
    df3_education_rich = df2_education_rich['count'].sum()

    df1_no_education = df_education[(df_education['education'].isin(no_degrees))]
    df2_no_education = df1_no_education.groupby(['education']).salary.agg(['count'])

    df1_no_education_rich = df_education[(df_education['education'].isin(no_degrees)) & (df_education['salary'] == '>50K')]
    df2_no_education_rich = df1_no_education_rich.groupby(['education']).salary.agg(['count'])
    df3_no_education_rich = df2_no_education_rich['count'].sum()

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = df2_education['count'].sum()
    lower_education = df2_no_education['count'].sum()

    # percentage with salary >50K
    higher_education_rich = round(( df3_education_rich / higher_education * 100), 1)
    lower_education_rich = round((df3_no_education_rich / lower_education * 100), 1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?

    df_min_hours = df.loc[:, ['hours-per-week', 'salary']]

    min_work_hours = df_min_hours['hours-per-week'].min()

    df1_min_hours = df_min_hours[(df_min_hours['hours-per-week'] == min_work_hours) & (df_min_hours['salary'] == '>50K')]
    df2_min_hours = df1_min_hours.groupby(['hours-per-week']).salary.agg(['count'])

    df1_min_hours1 = df_min_hours[(df_min_hours['hours-per-week'] == min_work_hours)]
    df2_min_hours1 = df1_min_hours1.groupby(['hours-per-week']).salary.agg(['count'])
    df3_min_hours1 = df2_min_hours1['count'].sum()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = df2_min_hours['count'].sum()

    rich_percentage = round(((num_min_workers) / (df3_min_hours1) * 100), 1)

    # What country has the highest percentage of people that earn >50K?
    df_country = df.loc[: , ['native-country', 'salary']]
    df1_country = df_country.groupby(['native-country']).salary.agg(['count'])
    df1_country = df1_country.rename(columns = {'count':'salary'})

    df1_country_rich = df_country[(df_country['salary'] == '>50K')]
    df2_country_rich = df1_country_rich.groupby(['native-country']).salary.agg(['count'])
    df2_country_rich = df2_country_rich.rename(columns = {'count': '>50K'})
  
    df_rich = pd.concat([df1_country, df2_country_rich], axis=1).fillna(0)
    df_rich['percentage'] = round(((df_rich['>50K'] / df_rich['salary'])* 100), 1)
    highest_earning_country_percentage = df_rich['percentage'].max()
    highest_earning_country = df_rich['percentage'].idxmax()

    # Identify the most popular occupation for those who earn >50K in India.
    df1_occ = df.loc[:, ['native-country','occupation', 'salary']]
    df2_occ = df1_occ.loc[(df1_occ['native-country'] == 'India') & (df1_occ['salary'] == '>50K')]
    df3_occ = df2_occ.groupby(['occupation']).salary.agg(['count'])

    top_IN_occupation = df3_occ['count'].idxmax()

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }

print(calculate_demographic_data())
