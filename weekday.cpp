// Created by Erin Lukow on 10/22/21.
// Calculate the day of the week for a given date

#include <iostream>
#include <string>
using namespace std;


void getDate(string& month, int& day, int& year);
// Prompts user for the month, day, and year in that order.
// Month must be in word form with the first letter capitalized.
// Day must be an integer value from 1 to 31.
// Year must be an integer value from 1 to 3000.

bool isLeap(int year);
// Determines if the year entered by the user is a leap year
// to help determine if the Leap Year Offset should be applied.

string calcWeekday(string& m, int& d, int& y);
// Precondition: user input for date is a valid month, day and year.
// Postcondition: Returns the day of the week for a specific date.


int main()
{
    string month;
    int day, year;
    
    getDate (month, day, year);
    calcWeekday(month, day, year);
    
    
    if ((month != "January") && (month != "February") && (month != "March") && (month != "April") && (month != "May") && (month != "June") && (month != "July") && (month != "August") && (month != "September") && (month != "October") && (month != "November") && (month != "December"))
    {
        cout << "Invalid month!\n";
        return (-1);
    }
    if (1 > day || day > 31)
    {
        cout << "Invalid day!\n";
        return (-1);
    }
    if (1 > year || year > 3000)
    {
        cout << "Invalid year!\n";
        return (-1);
    }
    else
        cout << month << " " << day << ", "
             << year << " was a " << calcWeekday(month, day, year) << "!\n";
    
    return 0;
 
   
}

void getDate(string& month, int& day, int& year)
{
    //User Input
    cout << "Provide a month: ";
    getline(cin, month);
    
    
    cout << "Provide a day: ";
    cin >> day;
    
    
    cout << "Provide a year: ";
    cin >> year;
    
        
}

bool isLeap(int year)
{
    if (year % 400 == 0)
        return true;
    if (year % 4 == 0)
        return true;
    if (year % 100 ==0)
        return false;
    else
        return false;
}


string calcWeekday(string& month, int& day, int& year)
{
    int monthCode =0, centCode = 0, yearCode = 0, dayCode = 0;
    
    
    //Calculate Month Code including Leap Year Offset
    if ((month == "January") && (isLeap(year) == true))
        monthCode = 0;
        else if ((month == "January") || (month == "October"))
                 monthCode = 1;
    else if ((month == "February") && (isLeap(year)== true))
        monthCode = 3;
        else if ((month == "February") || (month == "March") || (month == "November"))
            monthCode = 4;
    else if ((month == "April") || (month == "July"))
        monthCode = 0;
    else if (month == "May")
        monthCode = 2;
    else if (month == "June")
        monthCode = 5;
    else if (month == "August")
        monthCode = 3;
    else
        monthCode = 6;
    
    

    //Calculate Century Code
    int century = (year / 100) % 4;

    switch(century)
    {
        case 0:
            centCode = -2;
            break;
        case 1:
            centCode = 3;
            break;
        case 2:
            centCode = 1;
            break;
        case 3:
            centCode = -1;
            break;
    }

    //Calculate Year Code
    yearCode = ((year % 100) / 4) + (year % 100);
    
    //Calculate Day Code
    dayCode = (centCode + day + yearCode + monthCode) % 7;
    
    //Determine Weekday
    string weekday;
    
    switch(dayCode)
    {
        case 0:
            weekday = "Sunday";
            break;
        case 1:
        case (-6):
            weekday = "Monday";
            break;
        case 2:
        case (-5):
            weekday = "Tuesday";
            break;
        case 3:
        case (-4):
            weekday = "Wednesday";
            break;
        case 4:
        case (-3):
            weekday = "Thursday";
            break;
        case 5:
        case (-2):
            weekday = "Friday";
            break;
        case 6:
        case (-1):
            weekday = "Saturday";
            break;
            
    }
    
    return (weekday);
    
    }
        
    
    
    
    
   
    
    
    

    
    
        
        
        
             
             

                                                

                                        
    
        
    
    
                
            
    
        
        
        
                                    

  
