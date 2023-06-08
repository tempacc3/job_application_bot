# Welcome to The Job Application Bot, a.k.a JABot!

A Python termnial program that fetches jobs, writes and sends job applications!

I made this program as a demonstration of process automation capability in conjunction with me, Jonathan Tekin, applying for automation engineering jobs.

Thus, the Job Application Bot is in itself a job application. Call it a meta-job-application.

## Prerequisites

* Python 3.7
* Git

## Installation

Create and activate a python virtual environment

```
python3 -m venv venv
venv/Scripts/activate
```

Install JABot and it's dependencies directly from github with pip:

```
pip install git+https://github.com/tkin-jm/job_application_bot
```

Now you can run the program using:

```
jabot
```

## Usage

### Navigation

Navigate menus by typing in an option. Use the up or down arrows to autocomplete.

### Login

*Before using **JABot**, make sure you log in to ChatGPT and Gmail.*

* Navigate to `Main > Login` and select one of the login options. 

*A browser window will be opened directing you to the login pages of OpenAi or Google.*

* Simply login as usual then go back to JABot and press enter. 

*The authentication is persistent meaning you do not need to login again when you restart **JABot**.*

### Finding Jobs

* Under `Main > Jobs` select `Get Jobs From Indeed`. 

* Enter a job role and location. 

*The first 18 jobs found on Indeed will be scraped and proccessed by ChatGPT.*
*The processing will extract releveant information such as email, phone etc. and also write a summary for the description.*

*`View Jobs`, found in the same submenu, lets you view what was collected.*

### Writing applications

* Under `Main > Applications` select `Write applications`. 

*Make sure you have jobs saved from previous fetchings.*

* Enter a the full path to your resume. 

*There is autocomplete to make it more convenient.*

* Next enter the language to write the applications in. 

* Lastly you can choose to prepend/append text to each application which can be useful for adding personal information, discretion notes or whatever.

*`View Applications`, found in the same submenu, lets you view what was written.*

*If you want to make changes to the applicaitons you do that by editing the `applications.csv` file generate by `Write applications`. **Be very careful with the formatting though**.*

### Sending applications

* Under `Main > Applications` select `Send applications`. 

*Before selecting make sure you have applications saved and that you have logged into Gmail.*

*This option will send the written applications to whatever email address was found when processing the job description.*
*Some job descriptions lack an email address, applications written for these will be skipped. If you want to manually add an email address (or make other changes) to an application you do that by editing the `applications.csv` file generate by `Write applications`.*

* **JABot** will present each application and prompt you to confirm if you want to send it or not.

*In the email, **JABot** attaches the resume previosly entered during the `Write applications` process.*


## Demo

[Youtube video demonstrating the program](https://www.youtube.com/watch?v=-09kPe11OK4)

## Notes

This program uses Playwright to interact with third party functionality, this is very inefficient and often against terms of service. It does, however, bring with it some very big pros.
For a demonstrative program like this, those pros definitely outweighed the cons.

With ChatGPT, interacting through a browser instead of OpenAI's API circumvents the subscription cost of the API making this program free for everyone. 
With Indeed, interacting through a browser is the only alternative since they do not expose an API.
With Gmail, getting access to their API required having to get the program approved which involved an entire application process. It seemed a bit overkill.

Thus, I was stuck with the current solution and all the flakyness it brings.

There is alot of improvment to be made with the writing of the appliation in regards to the prompts. Currently it just uses the resume and job description to generate cover letters which works okay. They can probably become alot more tailored adn accurate by incorporating more user input. This is however more of a proof of conceåts and as such I feel the current state is sufficient.

## License

This project is licensed under the MIT License - see the LICENSE file for details.


