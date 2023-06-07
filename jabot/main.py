from .third_party.chatgpt import ChatGPT
from .third_party.indeed import Indeed
from .third_party.gmail import Gmail

from .jobs import Jobs
from .applications import Applications

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter, PathCompleter

from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from rich import print

from time import sleep

import pandas as pd
import os


class TUI:

    def __init__(self) -> None:
        self.console = Console()

        self.chatgpt = ChatGPT()
        self.indeed = Indeed()
        self.gmail = Gmail()

        self.jobs = Jobs(self.chatgpt, self.indeed)
        self.applications = Applications(self.chatgpt, self.gmail)

        self.loaded_jobs_df = None
        self.loaded_applications_df = None

        self.console.print(Markdown("# Welcome to the Job Application Bot!"))


    # --- functions --- #
    def get_jobs(self):
        self.console.print(Markdown("---"))
        self.console.print("Main > Jobs > Get Jobs", style="yellow", justify="center")
        print("")
        role = prompt("Enter a job role: ")
        location = prompt("Enter a job location: ")
        print("")

        with Live(auto_refresh=True) as live:
            try:
                live.update("[bold green]⏳ Fetching jobs from Indeed...[/bold green]")
                self.jobs.fetch(role, location)

                live.update("[bold green]⏳ Processing jobs...[/bold green]")
                self.jobs.process(live)

                live.update("[bold green]⏳ Saving results...[/bold green]")
                self.jobs.save()

                live.update("[bold green]\n⌛ Done![/bold green]")

                print("[bold white u]\nFound following jobs: [/bold white u]")
                for index, job in self.jobs.df.iterrows():
                    sleep(0.2)
                    print("")
                    print(f"[bold white]{index+1}.[/bold white]")
                    print(f"[bold yellow]What:[/bold yellow] {job['Title']}")
                    print(f"[bold yellow]Where:[/bold yellow] {job['Location']}")
                    print(f"[bold yellow]At:[/bold yellow] {job['Company']}")
                    print(f"[bold yellow]Summary:[/bold yellow] {job['Summary']}")

            except Exception as e:
                live.update(f"[bold red]❌ {str(e)}[/bold red]")


    def write_applications(self):
        self.console.print(Markdown("---"))
        self.console.print("Main > Applications > Write Applications", style="yellow", justify="center")
        print("")
        resume_path = (r'' + 
            prompt("Enter a the path to your resume (has to be PDF): ", 
                completer=PathCompleter(
                    file_filter=lambda filename : filename.endswith('.pdf') or os.path.isdir(filename)
                )
            )
        )


        language = prompt("Enter which language to write the applicaiton in: ")
        while True:
            confirm = prompt("Do you want to prepend/append text to each cover letter? (yes or no): ")
            if confirm == "yes":
                pre = prompt("Text to prepend (Esc+Enter when you're done):\n ", multiline=True) + "\n"
                post = "\n" + prompt("Text to append (Esc+Enter when you're done):\n ", multiline=True) 
                break
            elif confirm == "no":
                pre = ""
                post = ""
                break
            else:
                print("[bold red]❌ Answer 'yes' or 'no' please[/bold red]")

        print("")
        with Live(auto_refresh=True) as live:
            try:
                live.update("[bold green]⏳ Fetching resume...[/bold green]")
                self.applications.get_resume(resume_path)

                live.update("[bold green]⏳ Writing applications...[/bold green]")
                self.applications.write(language, pre, post, live)

                live.update("[bold green]⏳ Saving results...[/bold green]")
                self.applications.save()

                live.update("[bold green]⌛ Done![/bold green]")

                print("[bold white u]\nWrote applications for following jobs:\n[/bold white u]")
                for index, application in self.applications.df.iterrows():
                    sleep(0.2)
                    print(f"[bold white]{index+1}. [/bold white]{application['Title']}[bold yellow] At [/bold yellow]{application['Company']}")
                print("")

            except Exception as e:
                live.update(f"[bold red]❌ {str(e)}[/bold red]")
                

    def send_applications(self):
        self.console.print(Markdown("---"))
        self.console.print(f"Main > Applications > Send Applications", style="yellow", justify="center")
        try:
            self.loaded_applications_df = pd.read_csv("applications.csv")
        except FileNotFoundError:
            print(f"[bold red]❌ No applications found![/bold red]")

        with Live(auto_refresh=True) as live:
            try:
                for index, application in self.loaded_applications_df.iterrows():
                    live.start()
                    if '@' not in str(application['Email']):
                        live.update(f"\n[bold red]❌ {application['Title']} missing email address, skipping...[/bold red]")
                        sleep(2)
                        continue
                    live.update(
                        ""
                        f"[bold white]\n{index+1}/{len(self.loaded_applications_df.index)}[/bold white]"
                        f"[bold yellow u]\nTo:[/bold yellow u] {application['Email']}\n"
                        f"[bold yellow u]Subject:[/bold yellow u] {application['Subject']}\n"
                        f"[bold yellow u]\nContent:\n\n[/bold yellow u][italic]{application['Cover Letter']}[/italic]\n"
                    )
                    live.stop()
                    while True:
                        confirm = input("Do you want to send this application? (yes or no): ")
                        if confirm == "yes":
                            live.start()
                            live.update("[bold green]⏳ Sending application...[/bold green]")
                            self.applications.send(application)
                            live.update("[bold green]⌛ Done![/bold green]")
                            sleep(2)
                            break
                        elif confirm == "no":
                            break
                        else:
                            print("[bold red]❌ Answer 'yes' or 'no' please[/bold red]")
            except Exception as e:
                live.update(f"[bold red]❌ {str(e)}[/bold red]")

    def print_job_info(self, index):
        try:
            job = self.loaded_jobs_df.iloc[index]
            self.console.print(Markdown("---"))
            self.console.print(f"Main > Jobs > View Jobs > Job {index+1}.", style="yellow", justify="center")
            print(f"[bold yellow u]Title:[/bold yellow u] {job['Title']}")
            print(f"[bold yellow u]Company:[/bold yellow u] {job['Company']}")
            print(f"[bold yellow u]Location:[/bold yellow u] {job['Location']}")
            print(f"[bold yellow u]Person:[/bold yellow u] {job['Person']}")
            print(f"[bold yellow u]Phone:[/bold yellow u] {job['Phone']}")
            print(f"[bold yellow u]Email:[/bold yellow u] {job['Email']}")
            print(f"[bold yellow u]\nDescription:\n\n[/bold yellow u]{job['Description']}")
        except Exception as e:
            print(f"[bold red]❌ {str(e)}[/bold red]")


    def print_application_info(self, index):
        try:
            application = self.loaded_applications_df.iloc[index]
            self.console.print(Markdown("---"))
            self.console.print(f"Main > Applications > View Applications > Application {index+1}.", style="yellow", justify="center")
            print(f"[bold yellow u]\nTitle:[/bold yellow u] {application['Title']}")
            print(f"[bold yellow u]Company:[/bold yellow u] {application['Company']}")
            print(f"[bold yellow u]Email:[/bold yellow u] {application['Email']}")
            print(f"[bold yellow u]\nCover Letter:\n\n[/bold yellow u]{application['Cover Letter']}")
        except Exception as e:
            print(f"[bold red]❌ {str(e)}[/bold red]")


    def login_chatgpt(self):
        self.console.print(Markdown("---"))
        self.console.print("Main > Login > Login ChatGPT", style="yellow", justify="center")
        print("")

        print("[bold yellow]Please log in, then press enter to continue.[/bold yellow]")

        self.chatgpt.start(headless=False)
        input("")
        self.chatgpt.stop()


    def login_gmail(self):
        self.console.print(Markdown("---"))
        self.console.print("Main > Login > Login Gmail", style="yellow", justify="center")
        print("")

        print("[bold yellow]Please log in, then press enter to continue.[/bold yellow]")

        self.gmail.start(headless=False)
        input("")
        self.gmail.stop()


    # --- menus --- #
    def menu(self, options):
        print("[bold yellow]Select An Option:[/bold yellow]")
        options["x Exit"] = (exit, [])

        for option in options:
            print(f"[bold white]{option}[/bold white]")
        
        options = {key[2:]: value for key, value in options.items()}
        completer = WordCompleter(options.keys(), ignore_case=True)

        while True:
            user_input = prompt("\nPlease select an option: ", completer=completer)
            if user_input in options:

                if user_input == "Back":
                    return "Back"
                
                func = options[user_input][0]
                args = options[user_input][1]

                func(*args)
                break
            else:
                print("[bold red]❌ Invalid option, please select from the menu[/bold red]")


    def view_jobs_menu(self):
        while True:
            self.console.print(Markdown("---"))
            self.console.print("Main > Jobs > View Jobs", style="yellow", justify="center")
            options = {}

            try:
                self.loaded_jobs_df = pd.read_csv("jobs.csv")
                for index, job in self.loaded_jobs_df.iterrows():
                    key = "- " + str(index+1) + ". " + job["Title"]
                    options[key] = (self.print_job_info, [index])
            except FileNotFoundError:
                pass

            options["< Back"] = ""
            if self.menu(options) == "Back":
                break


    def jobs_menu(self):
        while True:
            self.console.print(Markdown("---"))
            self.console.print("Main > Jobs", style="yellow", justify="center")
            options = {
                '- Get Jobs From Indeed': (self.get_jobs, []),
                '> View Jobs': (self.view_jobs_menu, []),
                '< Back': ""
            }
            if self.menu(options) == "Back":
                break


    def view_applications_menu(self):
        while True:
            self.console.print(Markdown("---"))
            self.console.print("Main > Jobs > View Applications", style="yellow", justify="center")
            print("")
            print("[italic bright_black][bold]Note:[/bold] If you want to make changes to the applictions, please edit the [bold]applications.csv[/bold] file.\nBe carful with the formatting though.[/italic bright_black]")
            print("")
            options = {}

            try:
                self.loaded_applications_df = pd.read_csv("applications.csv")
                for index, application in self.loaded_applications_df.iterrows():
                    key = "- " + str(index+1) + ". " + application["Title"]
                    options[key] = (self.print_application_info, [index])
            except FileNotFoundError:
                pass

            options["< Back"] = ""
            if self.menu(options) == "Back":
                break


    def applications_menu(self):
        while True:
            self.console.print(Markdown("---"))
            self.console.print("Main > Applications", style="yellow", justify="center")
            options = {
                '- Write Applications': (self.write_applications, []),
                '- Send Applications': (self.send_applications, []),
                '> View Applications': (self.view_applications_menu, []),
                '< Back': ""
            }
            if self.menu(options) == "Back":
                break


    def login_menu(self):
        while True:
            self.console.print(Markdown("---"))
            self.console.print("Main > Login", style="yellow", justify="center")
            options = {
                '- Login to ChatGPT': (self.login_chatgpt, []),
                '- Login to Gmail': (self.login_gmail, []),
                '< Back': ""
            }
            if self.menu(options) == "Back":
                break


    def main_menu(self):
        while True:
            self.console.print(Markdown("---"))
            self.console.print("Main", style="yellow", justify="center")
            options = {
                '> Jobs': (self.jobs_menu, []),
                '> Applications': (self.applications_menu, []),
                '> Login': (self.login_menu, [])
            }
            self.menu(options)

def main():
    t = TUI()
    t.main_menu()


if __name__ == "__main__":
    main()
