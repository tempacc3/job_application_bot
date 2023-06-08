import re
import pandas as pd
from time import sleep

class Jobs:

    def __init__(self, chatgpt, indeed) -> None:
        self.chatgpt = chatgpt
        self.indeed = indeed

        self.jobs_data = None

        self.df = pd.DataFrame(
            columns=[
                "Title",
                "Company",
                "Location",
                "Person",
                "Phone",
                "Email",
                "Summary",
                "Description"
            ]
        )


    def fetch(self, role: str, location: str):
        self.jobs_data = self.indeed.fetch_jobs(role, location)


    def process(self, live = None):
        if not self.jobs_data:
            raise AssertionError("No jobs have been fetched")

        self.chatgpt.start()
        self.df = self.df[0:0]
        for job_data in self.jobs_data:
            if live:
                live.update(f"[bold green]⏳ Processing '[/bold green][bold white]{job_data['job_title']}[/bold white][bold green]'...[/bold green]")
            try:
                self._process_job_data(job_data)

            except PermissionError as e:
                raise e
            
            except Exception as e:
                if live:
                    live.update(f"[bold red]❌ Failed to process [bold white]{job_data['job_title']}[/bold white]: {str(e)}[/bold red]")
                    sleep(4)
                continue
            
        self.chatgpt.stop()
    

    def save(self):
        if self.df.empty:
            raise AssertionError("No jobs have been processed")
        self.df.to_csv(f"jobs.csv")


    def jobs(self):
        if self.df.empty:
            raise AssertionError("No jobs have been processed")
        return self.df


    def _process_job_data(self, job_data: str):

        description = job_data["job_description"]
        
        response = self.chatgpt.ask(
            "From the following text fill in these data points, if no data can be extracted fill it with 'None'. Make the sumamry very short\n"
            "Person:\n"
            "Phone:\n"
            "Email:\n"
            "Summary:\n\n"
            + description
        )

        person_match = re.search(r'Person:\s(.+)', response)
        phone_match = re.search(r'Phone:\s(.+)', response)
        email_match = re.search(r'Email:\s(.+)', response)
        summary_match = re.search(r'Summary:\s(.+)', response)

        person = person_match.group(1) if person_match else "None"
        phone = phone_match.group(1) if phone_match else "None"
        email = email_match.group(1) if email_match else "None"
        summary = summary_match.group(1) if summary_match else "None"

        title = job_data["job_title"]
        location = job_data["job_location"]
        company_name = job_data["company_name"]

        self.df.loc[len(self.df)] = [
            title,
            company_name,
            location,
            person,
            phone,
            email,
            summary,
            description
        ]

