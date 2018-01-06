Google Service Accounts

A Service Account is “an account that belongs to your application instead of to an individual end user”.

You can setup a Service Account by following the steps explained in this link (pay attention to the CONSOLE section of it).

REMARK: Make sure to save the JSON secret key file for the Service Account created. You won’t be able to obtain this file again if you lose it.

Before using the Service Account for your application, make sure you enable the Google APIs you’ll be using (for example: Google Drive API and Google Sheets API for the report-generator in the example folder). You can do this via the Google Developers Console page.


Why use a Service Account instead of a personal work account or a team account?

First of all, as Google say, this account belongs to the application instead of the end user.
Using a personal work account raised questions like:
What will happen when the person that created the folder/files using their account leaves the company? Will the files get deleted along with their account? Or will they live as shared documents for the whole brandwatch.com domain, but not be owned by anyone in particular, in which case they won’t be able to get deleted by anyone else. We will most definitely forget to transfer ownership of the files created with this person’s account and get into the above problems.

Using this type of account, your application will be prompted for a browser link to authenticate yourself. We can’t afford having such a step on our Linux servers and we also don’t want to be prompted for such steps. Read the following for more clarification on this.

The sample will attempt to open a new window or tab in your default browser. If this fails, copy the URL from the console and manually open it in your browser.
If you are not already logged into your Google account, you will be prompted to log in. If you are logged into multiple Google accounts, you will be asked to select one account to use for the authorization.
Click the Accept button.
The sample will proceed automatically, and you may close the window/tab.

Applications, like report-generator, that connect to different Google APIs from the same script seem to only work properly if you run each sample code offered by Google individually, (so for each different scope), and not combine functionalities in a single script (by functionalities I mean connecting to different scopes as we need to do for the report-generator in order to access the correct API endpoints:
SHEET_SCOPE = 'https://www.googleapis.com/auth/spreadsheets'
DRIVE_SCOPE = 'https://www.googleapis.com/auth/drive'

I assume the team account will behave as a normal personal work account.

Because of the above, the best option to access Google’s API is via a Service Account.
