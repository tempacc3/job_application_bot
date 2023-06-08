from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFSyntaxError
import pandas as pd
from time import sleep

class Applications:

    def __init__(self, chatgpt, gmail) -> None:
        self.chatgpt = chatgpt
        self.gmail = gmail

        self.resume_path = None
        self.resume = None

        self.df = pd.DataFrame(
            columns=[
                "Title",
                "Company",
                "Email",
                "Subject",
                "Cover Letter",
                "Resume Path"
            ]
        )

    def get_resume(self, resume_path: str):
        try:
           self.resume = extract_text(resume_path)
        except FileNotFoundError:
             raise FileNotFoundError("Can't find resume!")
        except PDFSyntaxError:
            raise PDFSyntaxError("Resume has to be PDF!")
        self.resume_path = resume_path


    def write(self, language, pre, post, live = None):
        try:
            jobs = pd.read_csv("jobs.csv")
        except FileNotFoundError:
            raise FileNotFoundError("No saved jobs found!")
        if not self.resume:
            raise Exception("No resume loaded.")

        self.chatgpt.start()
        self.df = self.df[0:0]
        for index, job in jobs.iterrows():

            if live:
                live.update(f"[bold green]⏳ Writing application for '[/bold green][bold white]{job['Title']}[/bold white][bold green]'...[/bold green]")

            try:

                command = self.chatgpt.ask(
                    f"Translate this sentence to {language}:\n\n"
                    f"'Write a cover letter in {language} for the following job description. Use my resume. Do not use placeholders'"
                )

                self.chatgpt.ask(
                    "This is my resume:\n\n"
                    + self.resume
                )

                cover_letter = self.chatgpt.ask(
                    command + "\n\n"
                    + job["Description"]
                )
                subject = self.chatgpt.ask(
                    f"Write an email subject in {language} to accompany the cover letter"
                )

                cover_letter = pre + cover_letter + post
                self.chatgpt.new_conversation()

            except PermissionError as e:
                raise e

            except Exception as e:
                if live:
                    live.update(f"[bold red]❌ Failed to write appliation for [bold white]{job['Title']}[/bold white]: {str(e)}[/bold red]")
                    sleep(4)
                continue

            self.df.loc[len(self.df)] = [
                job["Title"],
                job["Company"],
                job["Email"],
                subject,
                cover_letter,
                self.resume_path
            ]

        self.chatgpt.stop()


    def save(self):
        if self.df.empty:
            raise AssertionError("No cover letters have been written")
        self.df.to_csv("applications.csv")


    def send(self, application):
        self.gmail.start()
        try:
            self.gmail.send(application)
        except Exception as e:
            self.gmail.stop()
            raise e
        self.gmail.stop()
